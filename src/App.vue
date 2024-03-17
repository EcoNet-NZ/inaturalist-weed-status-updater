<template>
  <div>Hello {{ value }}</div>
</template>

<script>
const params = new URLSearchParams(window.location.search);
const paramValue = params.get('state');
console.log('State is "' + paramValue + '"');

export default {
  name: "App",
  data() {
    return {
      value: "World"
    };
  }
};
</script>
