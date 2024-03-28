<script setup>
// import ObservationUpdater from './components/ObservationUpdater.vue'
import ObservationReader from './components/ObservationReader.vue'
// import InputText from 'primevue/inputtext';
// import Button from 'primevue/button';
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
              <!-- <div class="flex align-items-center gap-2"> -->
                <ObservationReader :controlled=true :observation-id="observationId" :code="code"></ObservationReader>

                <!-- <label for="name" class="font-medium text-900 w-6rem">Name</label>
                <InputText id="name" v-model="name" class="p-3 border-1 border-300 border-round w-full" /> -->
              <!-- </div>
              <div class="flex align-items-center gap-2">
                <label for="email" class="font-medium text-900 w-6rem">Email</label>
                <InputText id="email" v-model="email" class="p-3 border-1 border-300 border-round w-full" />
              </div>
              <div class="flex align-items-center gap-2">
                <label for="password" class="font-medium text-900 w-6rem">Password</label>
                <InputText id="password" v-model="password" type="password" class="p-3 border-1 border-300 border-round w-full" />
              </div> -->
              <!-- <ObservationUpdater :observation-id="observationId" :code="code"></ObservationUpdater> -->
            </div>

          </TabPanel>
          <TabPanel header="Alive">
            <div class="flex flex-column gap-3">
              <ObservationReader :alive=true :observation-id="observationId" :code="code"></ObservationReader>
              <!-- <ObservationUpdater :observation-id="observationId" :code="code"></ObservationUpdater> -->
            </div>
          </TabPanel>
          <TabPanel header="Dead / No Control Needed">
              <ObservationReader :dead=true :observation-id="observationId" :code="code"></ObservationReader>
              <!-- <ObservationUpdater :observation-id="observationId" :code="code"></ObservationUpdater> -->
            <!-- </div> -->
          </TabPanel>
        </TabView>
      </div>
    </div>
  </div>
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
export default {
  name: 'weed-status-updater',
  created: function() {
    const params = new URLSearchParams(window.location.search)
      this.observationId = params.get('state')
      this.code = params.get('code')
      console.log('Observation id is "' + this.observationId + '"')
      this.iNaturalistUrl = 'https://inaturalist.nz/observations/' + this.observationId
  },  
  // components: {
  //   InputText,
  //   Button
  // },
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