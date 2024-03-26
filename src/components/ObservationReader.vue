<template>
  <div>
    <label for="areaInput">Area m2:</label>
    <input type="number" id="areaInput" v-model="area_m2">
  </div>
</template>

<script>
// var jmespath = require('jmespath');

export default {
  name: 'ObservationReader',
  props: {
    observationId: String
  },
  data() {
    return {
      area_m2: "",
      message: ""
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
        this.area_m2 = json.results[0].ofvs.filter(ofv => ofv.field_id === 12414)[0].value
        
        this.message = "Success!! iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
        // const data = await response.json()
        // console.log(data)
        // Handle the API response data here
      } catch (error) {
        this.message = "Error updating observation, please report to support@econet.nz. " + error
        console.error('Error fetching data:', error)
        // Handle error if any
      }
    // }
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

