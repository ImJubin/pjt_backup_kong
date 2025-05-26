// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import CompareView from '@/views/CompareView.vue'

const routes = [
  {
    path: '/',
    redirect: '/compare',  // 첫 진입 시 /compare로 자동 이동
  },
  {
    path: '/compare',
    name: 'Compare',
    component: CompareView
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router