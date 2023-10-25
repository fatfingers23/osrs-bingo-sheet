import { createRouter, createWebHistory } from 'vue-router'
import BingoSheet from '../views/BingoSheet.vue';

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: BingoSheet
    },
    {
      path: '/:passcode',
      name: 'team',
      component: BingoSheet
    },
  ]
})

export default router
