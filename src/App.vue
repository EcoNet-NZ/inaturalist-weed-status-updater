<template>
  <div>Hello {{ value }}</div>
  <div>
    <button @click="callAPI">Call API</button>
  </div>
</template>

<script>
const params = new URLSearchParams(window.location.search);
const state = params.get('state');
console.log('State is "' + state + '"');
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
        const response = await fetch('https://api.example.com/data');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        console.log(data);
        // Handle the API response data here
      } catch (error) {
        console.error('Error fetching data:', error);
        // Handle error if any
      }
    }
  }
};
</script>
