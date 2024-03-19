<template>
  <div>
    <button @click="updateObservation">Update observation</button>
  </div>
  <p v-if="message">{{ message }}</p>
</template>

<script>
export default {
  name: 'ObservationUpdater',
  props: {
    observationId: String,
    code: String
  },
  data() {
    return {
      message: ""
      // observationId: "",
      // iNaturalistUrl: ""
    };
  },
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
  methods: {
    async updateObservation() {

      // const params = new URLSearchParams(window.location.search)
      // this.observationId = params.get('state')
      // const code = params.get('code')
      // console.log('Observation id is "' + this.observationId + '"')
      // this.iNaturalistUrl = 'https://inaturalist.nz/observations/' + this.observationId

      // const message = ref('')

      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('auth-code', this.code)
        url.searchParams.set('state', this.observationId)
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
        // const data = await response.json()
        // console.log(data)
        // Handle the API response data here
      } catch (error) {
        this.message = "Error updating observation, please report to support@econet.nz. " + error
        console.error('Error fetching data:', error)
        // Handle error if any
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

