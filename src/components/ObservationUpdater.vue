<script setup>
import Button from 'primevue/button';
</script>

<template>
    <Button @click="updateObservation" label="Update the Observation" class="p-3 border-1 border-300 border-round bg-primary text-white font-medium" />
<!-- 
    <Button @click="updateObservation">Update observation</button> -->
  <p v-if="message">{{ message }}</p>
</template>

<script>
export default {
  name: 'ObservationUpdater',
  props: {
    observationId: String,
    code: String
  },
  data() {
    return {
      message: ""
    };
  },
  methods: {
    async updateObservation() {
      try {
        const url = new URL('/api/update', window.location.href)
        url.searchParams.set('auth-code', this.code)
        url.searchParams.set('state', btoa(this.observationId))
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
        
        this.message = "Success!! iNaturalist observation has been updated. The updates will be synchronised to CAMS within an hour."
      } catch (error) {
        this.message = "Error updating observation, please report to support@econet.nz. " + error
        console.error('Error fetching data:', error)
      }
    }
  }
}
</script>