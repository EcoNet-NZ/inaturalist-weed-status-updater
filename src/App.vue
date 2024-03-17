<template>
  <div>Hello {{ value }}</div>
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
  }
};
</script>
