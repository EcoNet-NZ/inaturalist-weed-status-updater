import { createApp } from 'vue';
import App from './App.vue'
import PrimeVue from 'primevue/config';
// import 'primevue/resources/themes/aura-light-green/theme.css'
import 'primeflex/primeflex.css'
import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';

const app = createApp(App);
// app.use(PrimeVue);
app.use(PrimeVue, { ripple: true })
app.mount('#app')
