<script setup>
  import { ref } from 'vue'

  const params = new URLSearchParams(window.location.search)
  const observationId = ref(params.get('state'))
  console.log('Observation id is "' + observationId.value + '"')
  const iNaturalistUrl = 'https://inaturalist.nz/observations/' + observationId.value
</script>

<template>
  <div>Updating iNaturalist observation <a :href="iNaturalistUrl">{{ observationId }}</a></div>
  <div>
    <button @click="callAPI">Call API</button>
  </div>
  <div>{{ message }}</div>
</template>

<script>
export default {
  name: 'App',
  methods: {
    async callAPI() {

      const params = new URLSearchParams(window.location.search)
      const observationId = params.get('state')
      const code = params.get('code')
      const message = ref('')

      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('auth-code', code)
        url.searchParams.set('state', observationId)
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
        message.value = "Success! iNaturalist observation has been updated. CAMS will be updated within an hour."
        // const data = await response.json()
        // console.log(data)
        // Handle the API response data here
      } catch (error) {
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
</style>

