// import './assets/main.css'
import 'v-calendar/style.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import piniaPersist from 'pinia-plugin-persistedstate'
import VCalendar from 'v-calendar'

import App from './App.vue'
import router from './router'

const app = createApp(App)
const pinia = createPinia()


app.use(createPinia())
pinia.use(piniaPersist)
app.use(router)
app.use(VCalendar, {})

app.mount('#app')
