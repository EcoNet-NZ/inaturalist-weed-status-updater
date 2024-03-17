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

      // const xhr = new XMLHttpRequest();
 
      // xhr.open('GET', 'https://inat-updater-test.azurewebsites.net/update?state=12344&code2=X');
      
      // xhr.onreadystatechange = function() {
      //   if(xhr.readyState === 4 && xhr.status === 200) {
      //     console.log(xhr.responseText);
      //   }
      // }
      
      // xhr.send(); 

      try {
        // const url = new URL('/api/upload');
        // const url = new URL('https://inat-updater-test.azurewebsites.net/update');
        // url.searchParams.set('state', state);
        // url.searchParams.set('code1', code);
        // console.log(url);
        const response = await fetch('/api/upload', {
          // mode: "no-cors",  // TODO add Access-Control-Allow-Origin to destination
          // credentials: "omit",
          // headers: {}
        });
        
        if (!response.ok) {
          console.log(response);
          console.log(response.status);
          console.log(response.ok);
          throw new Error('Network response was not ok');
        }
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
