<script setup>
import Button from 'primevue/button';
import Dropdown from 'primevue/dropdown';
import AlertBox from './AlertBox';

</script>

<template>
                <!-- <label for="name" class="font-medium text-900 w-6rem">Name</label>
                <InputText id="name" v-model="name" class="p-3 border-1 border-300 border-round w-full" /> -->

    <div v-if="controlled" class="flex align-items-center gap-2">
      <label for="howTreated" class="font-medium text-900 w-6rem">Control Method</label>
      <Dropdown v-model="howTreated" :options="controlMethods" optionLabel="name" optionValue="code" class="p-2 border-1 border-300 border-round w-full" :virtualScrollerOptions="{ itemSize: 24 }" />
    </div>

    <div v-if="controlled || alive" class="flex align-items-center gap-2">
      <label for="locationDetails" class="font-medium text-900 w-6rem">Location Details:</label>
      <input type="text" id="locationDetails" v-model="location_details" class="p-3 border-1 border-300 border-round w-full">
    </div>
    <div v-if="controlled || alive" class="flex align-items-center gap-2">
      <label for="areaInput" class="font-medium text-900 w-6rem">Area (m²):</label>
      <input type="number" id="areaInput" v-model="area_m2" class="p-3 border-1 border-300 border-round w-full">
    </div>
    <div v-if="controlled || alive" class="flex align-items-center gap-2">
      <label for="areaInput" class="font-medium text-900 w-6rem">Area (m²):</label>
      <input type="number" id="areaInput" v-model="area_m2" class="p-3 border-1 border-300 border-round w-full">
    </div>
    <div v-if="dead" class="flex align-items-center gap-2">
      <p>No further details needed. Press button below to update.</p>
    </div>
    <div class="flex flex-column gap-3">
      <Button @click="updateObservation" label="Update Observation" class="p-3 border-1 border-300 border-round bg-primary text-white font-medium" />
    </div>
    <div v-if="message" class="flex flex-column gap-3">
      <AlertBox>{{ message }}</AlertBox>
    </div>
</template>

<script>
// var jmespath = require('jmespath');

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
      // observationId: "",
      // iNaturalistUrl: ""
    };
  },
  created: async function() {
  // created: async function() {
  //   try {
  //       const url = new URL('/api/update', window.location.href)
  //       url.searchParams.set('auth-code', this.code)
  //       url.searchParams.set('state', this.observationId)
  //       console.log(url)
  //       const response = await fetch(url, {
  //           method: "POST"
  //         }
  //       )
        
  //       if (!response.ok) {
  //         console.log(response)
  //         console.log(response.status)
  //         console.log(response.ok)
  //         throw new Error('Network response was not ok')
  //       }
  //       const text = await response.text()
  //       console.log(text)
        
  //       this.message = "Success!! iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
  //       // const data = await response.json()
  //       // console.log(data)
  //       // Handle the API response data here
  //     } catch (error) {
  //       this.message = "Error updating observation, please report to support@econet.nz. " + error
  //       console.error('Error fetching data:', error)
  //       // Handle error if any
  //     }
  // }
  // methods: {
  //   async getObservation() {

      // const params = new URLSearchParams(window.location.search)
      // this.observationId = params.get('state')
      // const code = params.get('code')
      // console.log('Observation id is "' + this.observationId + '"')
      // this.iNaturalistUrl = 'https://inaturalist.nz/observations/' + this.observationId

      // const message = ref('')

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
        console.log(json)
        // const value = jmespath.search(json, "results[0][?field_id=1759].value")
        // console.log(value)
        
        console.log (json.results[0].ofvs.filter(ofv => ofv.field_id === 12414)[0].value)
        var ofvs = json.results[0].ofvs
        this.area_m2 = ofvs.filter(ofv => ofv.field_id === 12414)[0].value
        this.location_details = ofvs.filter(ofv => ofv.field_id === 5453)[0].value
        
        // this.message = "Success!! iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
        // const data = await response.json()
        // console.log(data)
        // Handle the API response data here
      } catch (error) {
        this.message = "Error updating observation, please report to support@econet.nz. " + error
        console.error('Error fetching data:', error)
        // Handle error if any
      }
    },
    methods: {      
    // }
    async updateObservation() {
      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('auth-code', this.code)
        url.searchParams.set('state', btoa(this.observationId))
        console.log(url)
        const response = await fetch(url, {
            method: "POST"
          }
        )
        
        if (!response.ok) {
          console.log(response)
          console.log(response.status)
          console.log(response.ok)
          throw new Error('Network response was not ok')
        }
        const text = await response.text()
        console.log(text)
        
        this.message = "Success!! iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
      } catch (error) {
        this.message = "Error updating observation, please report to support@econet.nz. " + error
        console.error('Error fetching data:', error)
      }
    }
  }
}
</script>

<!-- <style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
button {
  padding: 12px 32px;
  font-size: 16px;
  border-radius: 8px;
}
</style> -->

