<script setup>
  import { ref } from 'vue'

  const observationId = ref('');
  const params = new URLSearchParams(window.location.search);
  observationId.value = params.get('state'); 
  // const observationId = params.get('state'); 
  console.log('Observation id is "' + observationId.value + '"');
  const code = params.get('code');
  console.log('Auth code is "' + code + '"');
</script>

<template>
  <img alt="Vue logo" src="./assets/logo.png">
  <HelloWorld msg="Welcome to Your Vue.js App"/>
  <div><span>Hello </span><span>{{ observationId }}</span></div>
    <div>
      <button @click="callAPI">Call API</button>
    </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  components: {
    HelloWorld
  },
  methods: {
    async callAPI() {

      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('state', this.observationId.value)
        url.searchParams.set('auth-code', this.code)
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
