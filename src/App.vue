<script setup>
</script>

<template>
  <div>
    <div>Hello {{ observationId }}</div>
    <div>
      <button @click="callAPI">Call API</button>
    </div>
  </div>
</template>

<script>
import { ref } from 'vue'

const params = new URLSearchParams(window.location.search);
const observationId = ref('');
observationId.value = params.get('state'); 
console.log('Observation id is "' + observationId.value + '"');
const code = params.get('code');
console.log('Auth code is "' + code + '"');

export default {
  name: "App",
  data() {
    return {
      value: "World"
    };
  },
  methods: {
    async callAPI() {

      try {
        const url = new URL('/api/update', window.location.href);
        url.searchParams.set('state', observationId);
        url.searchParams.set('auth-code', code);
        console.log(url);
        const response = await fetch(url, {
            method: "POST"
          }
        );
        
        if (!response.ok) {
          console.log(response);
          console.log(response.status);
          console.log(response.ok);
          throw new Error('Network response was not ok');
        }
        const text = await response.text();
        console.log(text);
        // const data = await response.json();
        // console.log(data);
        // Handle the API response data here
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error if any
      }
    }
  }
};
</script>
