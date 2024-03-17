<template>
  <div>
    <div>Hello {{ value }}</div>
    <div>
      <button @click="callAPI">Call API</button>
    </div>
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
        const url = new URL('https://inat-updater-test.azurewebsites.net/update');
        url.searchParams.set('state', state);
        url.searchParams.set('authCode', code);
        console.log(url);
        const response = await fetch(url, {
          mode: "no-cors",  // TODO add Access-Control-Allow-Origin to destination
          credentials: "omit",
          headers: {}
        });
        console.log(response);
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
