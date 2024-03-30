<script setup>
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import AlertBox from './AlertBox';
import Fieldset from 'primevue/fieldset'
</script>

<template>
    <Fieldset v-if="controlled" legend="Control Details" :toggleable="true" class="p-0 m-0">
      <div v-if="controlled" class="flex align-items-center gap-2 p-0 m-0" >
        <label for="howTreated" class="font-medium text-900 w-6rem">Control Method</label>
        <Dropdown v-model="howTreated" :options="controlMethods" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" :virtualScrollerOptions="{ itemSize: 24 }" />
      </div>
    </Fieldset>

    <Fieldset v-if="controlled || alive" legend="Weed Details" :toggleable="true" class="p-0 m-0">
    <div class="flex align-items-center mb-3" :class="{ 'p-error': !locationDetailsValid }">
      <label for="locationDetails" class="font-medium text-900 w-6rem">Location Details:</label>
      <input type="text" id="locationDetails" v-model="location_details" class="p-3 border-1 border-300 border-round w-full">
      <span v-if="!locationDetailsValid">Location details are required.</span>
    </div>
    <div v-if="controlled || alive" class="flex align-items-center gap-2">
      <label for="areaInput" class="font-medium text-900 w-6rem">Area (m²):</label>
      <input type="number" id="areaInput" v-model="area_m2" class="p-3 border-1 border-300 border-round w-full">
    </div>
    </Fieldset>
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
export default {
  name: 'ObservationReader',
  props: {
    code: String,
    observationId: String,
    controlled: Boolean,
    alive: Boolean,
    dead: Boolean
  },

  data() {
    return {
      area_m2: "",
      location_details: "",
      message: "",
      howTreated: "",
      controlMethods: [
        { name: 'Cut and paste', code: 'Cut and paint' },
        { name: 'Drill and fill', code: 'Drill and fill' },
        { name: 'Scrape and paste', code: 'Scrape stem and paste' },
        { name: 'Pulled or dug', code: 'Pulled or dug' },
        { name: 'Ringbark', code: 'Ringbark' },
        { name: 'Spray leaves', code: 'Spray leaves' },
        { name: 'Cut but roots remain', code: 'Cut but roots remain' },
        { name: "Don't know", code: "Don't know" },
      ]
    };
  },

  computed: {
    locationDetailsValid() {
      return this.location_details.trim() !== '';
    },
    allFieldsValid() {
      // Check the validity of all relevant fields for each scope
      if (this.controlled || this.alive) {
        return this.locationDetailsValid /* && Add other validation checks here */; 
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
      
      console.log (json.results[0].ofvs.filter(ofv => ofv.field_id === 12414)[0].value)
      var ofvs = json.results[0].ofvs
      this.area_m2 = ofvs.filter(ofv => ofv.field_id === 12414)[0].value
      this.location_details = ofvs.filter(ofv => ofv.field_id === 5453)[0].value
      
    } catch (error) {
      this.message = "Error reading observation, please report to support@econet.nz. " + error
      console.error('Error fetching data:', error)
    }
  },

  methods: {      
    async updateObservation() {
      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('auth-code', this.code)
        url.searchParams.set('state', this.observationId)
        const jsonBody = JSON.stringify({
            observationId: this.observationId,
            area_m2: this.area_m2
          })
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
</style>

