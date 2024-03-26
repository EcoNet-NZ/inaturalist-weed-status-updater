<script setup>
import ObservationUpdater from './components/ObservationUpdater.vue'
import ObservationReader from './components/ObservationReader.vue'
</script>

<template>
  <p>Updating iNaturalist observation <a :href="iNaturalistUrl">{{ observationId }}</a></p>
  <ObservationReader :observation-id="observationId"></ObservationReader>
  <!-- <label for="areaInput">Area m2:</label>
    <input type="number" id="areaInput" v-model="areaValue"> -->
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
  },
  data() {
    return {
      areaValue: 0,
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