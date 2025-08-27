import { createRouter, createWebHistory } from '@ionic/vue-router';
import { RouteRecordRaw } from 'vue-router';
import TabsPage from '../views/TabsPage.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    redirect: '/home/suggestions'
  },
  {
    path: '/home/',
    component: TabsPage,
    children: [
      {
        path: '',
        redirect: '/home/suggestions'
      },
      {
        path: 'suggestions',
        component: () => import('@/views/suggestions.vue')
      },
      {
        path: 'generate',
        component: () => import('@/views/generate.vue')
      },
      {
        path: 'settings',
        component: () => import('@/views/settings.vue')
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes
})

export default router
