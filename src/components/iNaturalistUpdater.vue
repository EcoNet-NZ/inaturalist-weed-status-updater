<script setup>
import AlertBox from './AlertBox';
import Button from 'primevue/button';
import Calendar from 'primevue/calendar';
import Dropdown from 'primevue/dropdown';
import Fieldset from 'primevue/fieldset';
import InputText from 'primevue/inputtext';
import ProgressSpinner from 'primevue/progressspinner';
import RadioButton from 'primevue/radiobutton';
</script>

<template>
    <Fieldset v-if="controlled" legend="Control Details" :toggleable="true" class="p-0 m-0 mb-3">
      <div class="flex align-items-center gap-2">
        <label class="font-medium text-900 w-6rem mb-3 label-align">Controlled?</label>
        <div class="inline-flex">
          <div class="field-radiobutton">
            <RadioButton v-model="fullyControlled" value="fully" inputId="fully" name="fullyControlled" />
            <label for="fully" class="ml-2 label-align">Fully</label>
          </div>
          <div class="field-radiobutton">
            <RadioButton v-model="fullyControlled" value="partially" inputId="partially" name="fullyControlled" />
            <label for="partially" class="ml-2 label-align">Partially</label>
          </div>
        </div>
      </div>

      <div class="flex align-items-center gap-2 mb-3" :class="{ 'p-error': !controlMethodValid }" >
        <label for="controlMethod" class="font-medium text-900 w-6rem" >Control Method</label>
        <Dropdown v-model="controlMethod" :options="controlMethods" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" /> 
        <span v-if="!controlMethodValid">Control Method is required.</span>
      </div>

      <div class="flex align-items-center gap-2 mb-3" :class="{ 'p-error': !treatmentSubstanceValid }">
        <label for="treatmentSubstance" class="font-medium text-900 w-6rem" >Treatment Substance</label>
        <Dropdown v-model="treatmentSubstance" :options="treatmentSubstances" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
        <span v-if="!treatmentSubstanceValid">Treatment Substance is required.</span>
      </div>

      <div class="flex align-items-center gap-2">
        <label for="treatmentDetails" class="font-medium text-900 w-6rem">Treatment Details</label>
        <InputText type="text" id="treatmentDetails" v-model="treatmentDetails" class="p-3 border-1 border-300 border-round w-full"/>
      </div>
    </Fieldset>

    <Fieldset v-if="controlled || alive" legend="Weed Details" :toggleable="true" class="p-0 m-0">
      <div class="flex align-items-center gap-2 mb-3">
        <label for="locationDetails" class="font-medium text-900 w-6rem">Location Details</label>
        <InputText type="text" id="locationDetails" v-model="locationDetails" class="p-3 border-1 border-300 border-round w-full"/>
      </div>

      <div v-if="controlled || alive" class="flex align-items-center gap-2 mb-3">
        <label for="area" class="font-medium text-900 w-6rem">Area (m²)</label>
        <InputText type="number" id="area" v-model="area" class="p-3 border-1 border-300 border-round w-full"/>
      </div>

      <div v-if="controlled || alive" class="flex align-items-center gap-2 mb-3">
        <label for="height" class="font-medium text-900 w-6rem">Height (m)</label>
        <InputText type="number" id="height" v-model="height" class="p-3 border-1 border-300 border-round w-full"/>
      </div>

      <div class="flex align-items-center gap-2 mb-3" >
        <label for="phenology" class="font-medium text-900 w-6rem" >Stage</label>
        <Dropdown v-model="phenology" :options="phenologies" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
      </div>

      <div class="flex align-items-center gap-2 mb-3" >
        <label for="siteDifficulty" class="font-medium text-900 w-6rem" >Site Difficulty</label>
        <Dropdown v-model="siteDifficulty" :options="siteDifficulties" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
      </div>

      <div class="flex align-items-center gap-2" >
        <label for="effort" class="font-medium text-900 w-6rem" >Likely Effort</label>
        <Dropdown v-model="effort" :options="efforts" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
      </div>

    </Fieldset>

    <div v-if="controlled || alive" class="flex flex-column gap-3 mt-3">
      <div class="pb-4 flex align-items-center gap-2">
        <label for="follow-up-date" class="font-medium text-900 w-6rem">Follow-up Month</label>
        <Calendar id="follow-up-date" v-model="followUpDate" dateFormat="mm/yy" view="month" :minDate="today" class="w-full pl-3" />
      </div>
    </div>

    <div v-if="dead" class="flex align-items-center gap-2">
      <p>No further details needed. Press button below to update.</p>
    </div>
    
    <ProgressSpinner v-if="isLoading" />

    <div class="flex flex-column">
      <Button @click="updateObservation" label="Update Observation" :disabled="isButtonDisabled" class="p-3 border-1 border-300 border-round bg-primary text-white font-medium" />
    </div>
    
    <div v-if="message" class="flex flex-column">
      <AlertBox :type="result">{{ message }}</AlertBox>
    </div>
</template>

<script>
const dayjs = require('dayjs')

// Observation Field Ids can be found by searching for the observation field at https://www.inaturalist.org/observation_fields
// Click on the field and the URL contains the field id, ie https://www.inaturalist.org/observation_fields/<field id>
const OBSERVATION_FIELD_ID = {
  treated: 15709,
  dateControlled: 6508,
  howTreated: 15710,
  treatmentSubstance: 15662,
  treatmentDetails: 15712,

  locationDetails: 5453,
  area: 12414,
  height: 587,
  phenology: 1759,
  siteDifficulty: 15708,
  effort: 15661,

  statusUpdate: 15795,
  dateOfStatusUpdate: 15796,

  followUpDate: 14309
}
const ALIVE_FIELD_VALUE = 'Alive / Regrowth'
const DEAD_FIELD_VALUE = 'Dead / Not Present' 

export default {
  name: 'ObservationReader',
  props: {
    code: String,
    observationId: String,
    dateControlled: String,
    dateOfStatusUpdate: String,
    controlled: Boolean,
    alive: Boolean,
    dead: Boolean
  },

  data() {
    return {
      message: '',
      result: '',

      fullyControlled: 'fully',
      initialTreated: '',

      controlMethod: '',
      treatmentSubstance: '',
      treatmentDetails: '',
      initialControlMethod: '',
      initialTreatmentSubstance: '',
      initialTreatmentDetails: '',

      locationDetails: '',
      area: '',
      height: '',
      phenology: '',
      siteDifficulty: '',
      effort: '',
      initialLocationDetails: '',
      initialArea: '',
      initialHeight: '',
      initialPhenology: '',
      initialSiteDifficulty: '',
      initialEffort: '',
      
      followUpDate: null,
      initialFollowUpDate: null,

      isLoading: false,

      today: new Date(),

      controlMethods: [
        { name: 'Cut and paste',        code: 'Cut and paint' },
        { name: 'Drill and fill',       code: 'Drill and fill' },
        { name: 'Scrape and paste',     code: 'Scrape stem and paste' },
        { name: 'Pulled or dug',        code: 'Pulled or dug' },
        { name: 'Ringbark',             code: 'Ringbark' },
        { name: 'Spray leaves',         code: 'Spray leaves' },
        { name: 'Cut but roots remain', code: 'Cut but roots remain' },
        { name: "Don't know",           code: "Don't know" },
      ],
      treatmentSubstances: [
        { name: 'None',                        code: 'None' },
        { name: 'CutNPaste Original Gel',      code: 'CutNPaste Original Gel' },
        { name: 'CutNPaste Bamboo Buster Gel', code: 'CutNPaste Bamboo Buster Gel' },
        { name: 'CutNPaste Glimax',            code: 'CutNPaste Glimax' },
        { name: 'CutNPaste MetGel',            code: 'CutNPaste MetGel' },
        { name: 'CutNPaste Picloram Gel',      code: 'CutNPaste Picloram Gel' },
        { name: 'Dow Vigilant II',             code: 'Dow Vigilant II' },
        { name: 'Weed Weapon Invade Gel',      code: 'Weed Weapon Invade Gel' },
        { name: 'Weed Weapon Stump-Stop-Gel',  code: 'Weed Weapon Stump-Stop-Gel' },
        { name: 'Other',                       code: 'OTHER-TREATMENT' },
      ],
      phenologies: [
        // { name: 'Not recorded',         code: 'not recorded' },
        { name: 'Vegetative only',      code: 'vegetative only' },
        { name: 'Flower buds',          code: 'flower buds' },
        { name: 'Flowers',              code: 'flowers' },
        { name: 'Immature fruit',       code: 'immature fruit' },
        { name: 'Mature fruit',         code: 'mature fruit' },
        { name: 'Seed dispersed',       code: 'seed dispersed' },
      ],
      siteDifficulties: [
        { name: 'Easy (for most people)',                         code: '1 Easy (for most people)' },
        { name: 'Moderate',                                       code: '2 Moderate' },
        { name: 'Challenging (may be rough or steep)',            code: '3 Challenging (may be rough or steep)' },
        { name: 'Advanced (beyond most abilities)',               code: '4 Advanced (beyond most abilities)' },
        { name: 'Professional skills required (eg rope access)',  code: '5 Professional skills required (eg rope access)' },
      ],
      efforts: [
        { name: 'Up to one person hour',  code: '1 = Up to one person hour' },
        { name: 'Two person hours',       code: '2 = Two person hours' },
        { name: 'Three person hours',     code: '3 = Three person hours' },
        { name: 'Four person hours',      code: '4 = Four person hours' },
        { name: 'Five+ person hours',     code: '5 = Five+ person hours' },
      ],
    };
  },

  computed: {
    controlMethodValid() {
      return this.controlMethod && this.controlMethod.trim() !== '';
    },
    treatmentSubstanceValid() {
      return this.treatmentSubstance && this.treatmentSubstance.trim() !== '';
    },
    allFieldsValid() {
      if (this.controlled && !this.dateControlled) {
        return false
      }
      if ((this.alive || this.dead) && !this.dateOfStatusUpdate) {
        return false
      }
      if (this.controlled) {
        return this.controlMethodValid && this.treatmentSubstanceValid
      }
      return true
    },
    isButtonDisabled() {
      return !!this.message || !this.allFieldsValid || this.isLoading
    },
  },

  created: async function() {
    try {
      const url = new URL('https://api.inaturalist.org/v1/observations/' + this.observationId)
      console.log(url)
      var response
      try {
        this.isLoading = true
        response = await fetch(url)
      } finally {
        this.isLoading = false
      }
      
      if (!response.ok) {
        console.log(response)
        console.log(response.status)
        console.log(response.ok)
        throw new Error('Network response was not ok')
      }
      const json = await response.json()
      
      var ofvs = json.results[0].ofvs
      this.initialTreated = this.getFieldValue(ofvs, 'treated')
      this.controlMethod = this.getFieldValue(ofvs, 'howTreated')
      this.treatmentSubstance = this.getFieldValue(ofvs, 'treatmentSubstance')
      this.treatmentDetails = this.getFieldValue(ofvs, 'treatmentDetails')
      
      this.locationDetails = this.getFieldValue(ofvs, 'locationDetails')
      this.area = this.getFieldValue(ofvs, 'area')
      this.height = this.getFieldValue(ofvs, 'height')
      this.phenology = this.getFieldValue(ofvs, 'phenology')
      this.siteDifficulty = this.getFieldValue(ofvs, 'siteDifficulty')
      this.effort = this.getFieldValue(ofvs, 'effort')

      var fud = this.getFieldValue(ofvs, 'followUpDate')
      if (fud && fud != '(undef.)') this.followUpDate = fud

      this.initialControlMethod = this.controlMethod
      this.initialTreatmentSubstance = this.treatmentSubstance
      this.initialTreatmentDetails = this.treatmentDetails
      
      this.initialLocationDetails = this.locationDetails
      this.initialArea = this.area
      this.initialHeight = this.height
      this.initialPhenology = this.phenology
      this.initialSiteDifficulty = this.siteDifficulty
      this.initialEffort = this.effort

      this.initialFollowUpDate = this.followUpDate
      
    } catch (error) {
      this.message = "Error reading observation, please report to kiaora@ombfree.nz. " + error
      this.result = 'error'
      console.error('Error fetching data:', error)
    }
  },

  methods: {
    getFieldValue(ofvs, fieldName) {
      var arr = ofvs.filter(ofv => ofv.field_id === OBSERVATION_FIELD_ID[fieldName])
      if (arr.length === 0)
        return null
      return arr[0].value
    },
    
    createJsonBody() {
      var fields = {observationId: this.observationId}

      if (this.controlled || this.alive) {
        if (this.locationDetails    != this.initialLocationDetails)     fields[OBSERVATION_FIELD_ID['locationDetails']] = this.locationDetails
        if (this.area               != this.initialArea)                fields[OBSERVATION_FIELD_ID['area']] = this.area
        if (this.height             != this.initialHeight)              fields[OBSERVATION_FIELD_ID['height']] = this.height
        if (this.phenology          != this.initialPhenology)           fields[OBSERVATION_FIELD_ID['phenology']] = this.phenology
        if (this.siteDifficulty     != this.initialSiteDifficulty)      fields[OBSERVATION_FIELD_ID['siteDifficulty']] = this.siteDifficulty
        if (this.effort             != this.initialEffort)              fields[OBSERVATION_FIELD_ID['effort']] = this.effort
        if (this.followUpDate       != this.initialFollowUpDate)        fields[OBSERVATION_FIELD_ID['followUpDate']] = this.monthOnly(this.followUpDate)
      }
      if (this.controlled) {
        var treated = this.fullyControlled == 'fully' ? 'Yes' : (this.fullyControlled == 'partially' ? 'Partially' : 'No')
        if (treated                 != this.initialTreated)             fields[OBSERVATION_FIELD_ID['treated']] = treated
        if (this.dateControlled)      fields[OBSERVATION_FIELD_ID['dateControlled']] = this.dateControlled
        if (this.controlMethod      != this.initialControlMethod)       fields[OBSERVATION_FIELD_ID['howTreated']] = this.controlMethod
        if (this.treatmentSubstance != this.initialTreatmentSubstance)  fields[OBSERVATION_FIELD_ID['treatmentSubstance']] = this.treatmentSubstance
        if (this.treatmentDetails   != this.initialTreatmentDetails)    fields[OBSERVATION_FIELD_ID['treatmentDetails']] = this.treatmentDetails
      } else {
        if (this.dateOfStatusUpdate)  fields[OBSERVATION_FIELD_ID['dateOfStatusUpdate']] = this.dateOfStatusUpdate
        if (this.alive)               fields[OBSERVATION_FIELD_ID['statusUpdate']] = ALIVE_FIELD_VALUE
        if (this.dead)                fields[OBSERVATION_FIELD_ID['statusUpdate']] = DEAD_FIELD_VALUE
      }
      console.log('Fields:' + fields)
      var jsonBody = JSON.stringify(fields)
      console.log('Body: ' + jsonBody)
      return jsonBody
    },

    async updateObservation() {
      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('auth-code', this.code)
        url.searchParams.set('state', this.observationId)
        var jsonBody = this.createJsonBody()
        console.log(url)
        console.log('Sending body ' + jsonBody)
        
        var response
        try {
          this.isLoading = true
          this.$emit('update-requested')
          response = await fetch(url, {
              method: "POST",
              headers: {
              //   'Accept': 'application/json',
                'Content-Type': 'application/json'
              },
              body: jsonBody
            }
          )
        } finally {
          this.isLoading = false
        }
        
        const text = await response.text()
        console.log(text)

        if (!response.ok) {
          console.log(response)
          console.log(response.status)
          console.log(response.ok)
          throw new Error('Network response was not ok')
        }
        
        this.message = "iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
        this.result = 'success'
      } catch (error) {
        this.message = "Error updating observation, please report to kiaora@ombfree.nz. " + error
        this.result = 'error'
        console.error('Error fetching data:', error)
      }
    },
    monthOnly(date) {
      return dayjs(date).format('YYYY-MM')
    }
  }
}
</script>

<style scoped>
.p-error {
  border: 1px solid red;
}
.p-error span {
  color: red;
  font-size: 0.8rem;
}
.inline-flex {
  display: inline-flex;
  align-items: center;
}

.inline-flex > div {
  margin-right: 1rem;
}

.label-align {
  line-height: 1.5;
}
</style>

