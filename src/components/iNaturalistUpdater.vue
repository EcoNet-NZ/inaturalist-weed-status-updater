<script setup>
import AlertBox from './AlertBox';
import Button from 'primevue/button';
import Calendar from 'primevue/calendar';
import Dropdown from 'primevue/dropdown';
import Fieldset from 'primevue/fieldset';
import RadioButton from 'primevue/radiobutton';
</script>

<template>
    <Fieldset v-if="controlled" legend="Control Details" :toggleable="true" class="p-0 m-0">
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
      <input type="text" id="treatmentDetails" v-model="treatmentDetails" class="p-3 border-1 border-300 border-round w-full">
      </div>
    </Fieldset>

    <Fieldset v-if="controlled || alive" legend="Weed Details" :toggleable="true" class="p-0 m-0">
      <div class="flex align-items-center gap-2 mb-3">
        <label for="locationDetails" class="font-medium text-900 w-6rem">Location Details</label>
        <input type="text" id="locationDetails" v-model="locationDetails" class="p-3 border-1 border-300 border-round w-full">
      </div>

      <div v-if="controlled || alive" class="flex align-items-center gap-2 mb-3">
        <label for="area" class="font-medium text-900 w-6rem">Area (m²)</label>
        <input type="number" id="area" v-model="area" class="p-3 border-1 border-300 border-round w-full">
      </div>

      <div v-if="controlled || alive" class="flex align-items-center gap-2 mb-3">
        <label for="height" class="font-medium text-900 w-6rem">Height (m)</label>
        <input type="number" id="height" v-model="height" class="p-3 border-1 border-300 border-round w-full">
      </div>

      <div class="flex align-items-center gap-2 mb-3" >
        <label for="phenology" class="font-medium text-900 w-6rem" >Stage</label>
        <Dropdown v-model="phenology" :options="phenologies" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
      </div>

      <div class="flex align-items-center gap-2 mb-3" >
        <label for="siteDifficulty" class="font-medium text-900 w-6rem" >Site Difficulty</label>
        <Dropdown v-model="siteDifficulty" :options="siteDifficulties" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
      </div>

      <div class="flex align-items-center gap-2 mb-3" >
        <label for="effort" class="font-medium text-900 w-6rem" >Likely Effort</label>
        <Dropdown v-model="effort" :options="efforts" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" />
      </div>

    </Fieldset>

    <div class="flex flex-column gap-3">
      <div class="pb-4 flex align-items-center gap-2">
        <label for="follow-up-date" class="font-medium text-900 w-6rem">Follow-up Date</label>
        <Calendar id="follow-up-date" v-model="followUpDate" dateFormat="mm/yy" view="month" :minDate="today" class="w-full pl-3" />
      </div>
    </div>

    <div v-if="dead" class="flex align-items-center gap-2">
      <p>No further details needed. Press button below to update.</p>
    </div>
    
    <div class="flex flex-column gap-3">
      <Button @click="updateObservation" label="Update Observation" :disabled="!allFieldsValid" class="p-3 border-1 border-300 border-round bg-primary text-white font-medium" />
    </div>
    
    <div v-if="message" class="flex flex-column gap-3">
      <AlertBox>{{ message }}</AlertBox>
    </div>
</template>

<script>
const dayjs = require('dayjs')

// Observation Field Ids can be found by searching for the observation field at https://www.inaturalist.org/observation_fields
// Click on the field and the URL contains the field id, ie https://www.inaturalist.org/observation_fields/<field id>
const OBSERVATION_FIELD_ID = {
  area: 12414,
  locationDetails: 5453,
  dateControlled: 6508,
  dateOfStatusUpdate: 15796
}

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

      fullyControlled: 'fully',
      controlMethod: '',
      treatmentSubstance: '',
      treatmentDetails: '',

      locationDetails: '',
      area: '',
      height: '',
      phenology: '',
      siteDifficulty: '',
      effort: '',

      followUpDate: null,

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
        { name: 'Not recorded',         code: 'not recorded' },
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
      return this.controlMethod.trim() !== '';
    },
    treatmentSubstanceValid() {
      return this.treatmentSubstance.trim() !== '';
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
  },

  created: async function() {
    try {
      const url = new URL('https://api.inaturalist.org/v1/observations/' + this.observationId)
      console.log(url)
      const response = await fetch(url)
      
      if (!response.ok) {
        console.log(response)
        console.log(response.status)
        console.log(response.ok)
        throw new Error('Network response was not ok')
      }
      const json = await response.json()
      
      // console.log (json.results[0].ofvs.filter(ofv => ofv.field_id === 12414)[0].value)
      var ofvs = json.results[0].ofvs
      this.area = ofvs.filter(ofv => ofv.field_id === OBSERVATION_FIELD_ID['area'])[0].value
      this.locationDetails = ofvs.filter(ofv => ofv.field_id === OBSERVATION_FIELD_ID['locationDetails'])[0].value
      
    } catch (error) {
      this.message = "Error reading observation, please report to support@econet.nz. " + error
      console.error('Error fetching data:', error)
    }
  },

  methods: {      
    createJsonBody() {
      var jsonBody = JSON.stringify({
          observationId: this.observationId,
        })
      if (this.controlled || this.alive) {
        jsonBody += JSON.stringify({
          [OBSERVATION_FIELD_ID['area']]: this.area,
        })
      }
      if (this.controlled) {
        jsonBody += JSON.stringify({
          [OBSERVATION_FIELD_ID['dateControlled']]: this.dateControlled,
        })
      } else {
        jsonBody += JSON.stringify({
          [OBSERVATION_FIELD_ID['dateOfStatusUpdate']]: this.dateOfStatusUpdate
        })
      }
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
        const response = await fetch(url, {
            method: "POST",
            headers: {
            //   'Accept': 'application/json',
              'Content-Type': 'application/json'
            },
            body: jsonBody
          }
        )
        
        const text = await response.text()
        console.log(text)

        if (!response.ok) {
          console.log(response)
          console.log(response.status)
          console.log(response.ok)
          throw new Error('Network response was not ok')
        }
        
        this.message = "Success!! iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
      } catch (error) {
        this.message = "Error updating observation, please report to support@econet.nz. " + error
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

