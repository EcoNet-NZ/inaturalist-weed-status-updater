<script setup>
import ObservationUpdater from './components/ObservationUpdater.vue'
</script>

<template>
  <p>Updating iNaturalist observation <a :href="iNaturalistUrl">{{ observationId }}</a></p>
  <ObservationUpdater :observation-id="observationId" :code="code"></ObservationUpdater>
</template>

<script>
export default {
  name: 'weed-status-updater',
  created: function() {
    const params = new URLSearchParams(window.location.search)
      this.observationId = params.get('state')
      this.code = params.get('code')
      console.log('Observation id is "' + this.observationId + '"')
      this.iNaturalistUrl = 'https://inaturalist.nz/observations/' + this.observationId
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