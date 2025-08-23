import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import Home from '../views/Home.vue'
import Create from '../views/Create.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home
  },
  {
    path: '/create',
    name: 'Create',
    component: Create
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
