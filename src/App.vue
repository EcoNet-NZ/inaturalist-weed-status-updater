<!--
====================================================================
Copyright 2024-2025 EcoNet.NZ

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
====================================================================
-->
<script setup>
import iNaturalistUpdater from './components/iNaturalistUpdater.vue'
import Calendar from 'primevue/calendar';
import RadioButton from 'primevue/radiobutton';
// import TabPanel from 'primevue/tabpanel';
// import TabView from 'primevue/tabview';
</script>

<template>
  <div class="grid">
    <div class="col-12 md:col-6 mx-auto">
      <div class="surface-card p-4 shadow-2 border-round">
        <div class="text-center mb-5">
          <div class="text-900 text-3xl font-medium mb-3">Update iNaturalist observation <a :href="iNaturalistUrl">{{ observationId }}</a></div>
          <span class="text-600 font-medium">as the logged-in iNaturalist user</span>
        </div>

        <div class="flex flex-column gap-3">
          <div class="pb-4 flex align-items-center gap-2" :class="{ 'p-error': !visitDateValid }">
            <label for="visit-date" class="font-medium text-900 w-6rem">Visit Date</label>
            <Calendar id="visit-date" v-model="visitDate" dateFormat="dd/mm/yy" :maxDate="today" class="w-full" />
            <span v-if="!visitDateValid">Visit date is required.</span>
          </div>
        </div>

        <div class="flex align-items-start gap-2 mb-3">
  <label class="font-medium text-900 w-6rem mb-3 label-align">Is this weed:</label>
  <div class="inline-flex flex-wrap gap-2">
    <div class="field-radiobutton" style="padding: 0; margin: 0;"> <!-- Reduced padding and margin -->
      <RadioButton v-model="status" value="controlled" inputId="controlled" name="controlled" :disabled="disableRadioButtons" />
      <label for="controlled" class="ml-2 label-align">Controlled</label>
    </div>
    <div class="field-radiobutton" style="padding: 0; margin: 0;">
      <RadioButton v-model="status" value="alive" inputId="alive" name="alive" :disabled="disableRadioButtons" />
      <label for="alive" class="ml-2 label-align">Alive</label>
    </div>
    <div class="field-radiobutton" style="padding: 0; margin: 0;">
      <RadioButton v-model="status" value="dead" inputId="dead" name="dead" :disabled="disableRadioButtons" />
      <label for="dead" class="ml-2 label-align">Dead</label>
    </div>
    <div class="field-radiobutton" style="padding: 0; margin: 0;">
      <RadioButton v-model="status" value="duplicate" inputId="duplicate" name="duplicate" :disabled="disableRadioButtons" />
      <label for="duplicate" class="ml-2 label-align">Duplicate</label>
    </div>
  </div>
</div>


        <iNaturalistUpdater v-if="status === 'controlled'" @update-requested="disableRadioButtons = true" :controlled=true :observation-id="observationId" :code="code" :date-controlled="dateOnly(visitDate)"></iNaturalistUpdater>
        <iNaturalistUpdater v-if="status === 'alive'" @update-requested="disableRadioButtons = true" :alive=true :observation-id="observationId" :code="code" :date-of-status-update="dateOnly(visitDate)"></iNaturalistUpdater>
        <iNaturalistUpdater v-if="status === 'dead'" @update-requested="disableRadioButtons = true" :dead=true :observation-id="observationId" :code="code" :date-of-status-update="dateOnly(visitDate)"></iNaturalistUpdater>
        <iNaturalistUpdater v-if="status === 'duplicate'" @update-requested="disableRadioButtons = true" :duplicate=true :observation-id="observationId" :code="code" :date-of-status-update="dateOnly(visitDate)"></iNaturalistUpdater>

        <!-- <TabView>
          <TabPanel header="Controlled">
            <div class="flex flex-column gap-3">
                <iNaturalistUpdater :controlled=true :observation-id="observationId" :code="code" :date-controlled="dateOnly(visitDate)"></iNaturalistUpdater>
            </div>
          </TabPanel>
          <TabPanel header="Alive">
            <div class="flex flex-column gap-3">
            </div>
          </TabPanel>
          <TabPanel header="Dead / Not Present">
              <iNaturalistUpdater :dead=true :observation-id="observationId" :code="code" :date-of-status-update="dateOnly(visitDate)"></iNaturalistUpdater>
          </TabPanel>
        </TabView> -->
      </div>
    </div>
  </div>
</template>

<script>
const dayjs = require('dayjs')

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
      status: '',
      disableRadioButtons: false,

      today: new Date(),
    }
  },

  computed: {
    visitDateValid() {
      return this.visitDate != null
    }
  },

  methods: {      
    dateOnly(date) {
      return dayjs(date).format('YYYY-MM-DD')
    }
  }
}
</script>

<style scoped>
.inline-flex {
  display: inline-flex;
  align-items: center;
}

.inline-flex > div {
  margin-right: 1rem;
}
</style>