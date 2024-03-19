<script setup>
  // import { ref } from 'vue'

  // const params = new URLSearchParams(window.location.search)
  // const observationId = ref(params.get('state'))
  // console.log('Observation id is "' + observationId.value + '"')
  // const iNaturalistUrl = 'https://inaturalist.nz/observations/' + observationId.value
</script>

<template>
  <p>Updating iNaturalist observation <a :href="iNaturalistUrl">{{ observationId }}</a></p>
  <div>
    <button @click="updateObservation">Update observation</button>
  </div>
  <p v-if="message">{{ message }}</p>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'App',
  // props: {
  //   msg: String,
  // },
  data() {
    return {
      message: "",
      // observationId: "",
      // code: "",
      // iNaturalistUrl: ""
    };
  },
  setup() {
    const params = new URLSearchParams(window.location.search)
    const observationId = ref(params.get('state'))
    const code = ref(params.get('code'))
    console.log('Observation id is "' + observationId.value + '"')
    const iNaturalistUrl = ref('https://inaturalist.nz/observations/' + observationId.value)
    return {
      observationId, 
      code, 
      iNaturalistUrl
    }
  },
  methods: {
    async updateObservation() {
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

<style>
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
</style>

