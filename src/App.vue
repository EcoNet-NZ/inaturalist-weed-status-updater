<script setup>
import ObservationReader from './components/ObservationReader.vue'
import Calendar from 'primevue/calendar';
import TabView from 'primevue/tabview';
import TabPanel from 'primevue/tabpanel';
</script>

<template>
  <div class="grid">
    <div class="col-12 md:col-6 mx-auto">
      <div class="surface-card p-4 shadow-2 border-round">
        <div class="text-center mb-5">
          <div class="text-900 text-3xl font-medium mb-3">Updating iNaturalist observation <a :href="iNaturalistUrl">{{ observationId }}</a></div>
          <!-- <span class="text-600 font-medium">Join the community</span> -->
        </div>

        <div class="flex flex-column gap-3">
          <div class="pb-4 flex align-items-center gap-2">
            <label for="visit-date" class="font-medium text-900 w-6rem">Visit Date</label>
            <Calendar id="visit-date" v-model="visitDate" dateFormat="dd/mm/yy" class="w-full" />
          </div>
        </div>
        
        <TabView>
          <TabPanel header="Controlled">
            <div class="flex flex-column gap-3">
                <ObservationReader :controlled=true :observation-id="observationId" :code="code"></ObservationReader>
            </div>
          </TabPanel>
          <TabPanel header="Alive">
            <div class="flex flex-column gap-3">
              <ObservationReader :alive=true :observation-id="observationId" :code="code"></ObservationReader>
            </div>
          </TabPanel>
          <TabPanel header="Dead / No Control Needed">
              <ObservationReader :dead=true :observation-id="observationId" :code="code"></ObservationReader>
          </TabPanel>
        </TabView>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'weed-status-updater',
  created: function() {
    const params = new URLSearchParams(window.location.search)
      this.observationId = params.get('state')
      this.code = params.get('code')
      console.log('Observation id is "' + this.observationId + '"')
      console.log("Code is " + this.code)
      this.iNaturalistUrl = 'https://inaturalist.nz/observations/' + this.observationId
  },  
  data() {
    return {
      name: '',
      email: '',
      password: '',
      visitDate: new Date(),
    }
  }
}
</script>