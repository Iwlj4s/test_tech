// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import UserProfile from '../components/UserProfile.vue'
import Feed from '../components/Feed.vue'
import AuthForm from '../components/AuthForm.vue'
import UserProfileView from '../components/UserProfileView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    redirect: '/auth'
  },
  {
    path: '/auth',
    name: 'auth',
    component: AuthForm
  },
  {
    path: '/profile',
    name: 'profile',
    component: UserProfile,
    meta: { requiresAuth: true }
  },
  {
    path: '/feed',
    name: 'feed',
    component: Feed,
    meta: { requiresAuth: true }
  },
  {
    path: '/user/:id',
    name: 'user',
    component: UserProfileView,
    meta: { requiresAuth: true }
  },
  {
  path: '/admin',
  name: 'admin',
  component: () => import('../components/AdminPanel.vue'),
  meta: { 
    requiresAuth: true,
    requiresAdmin: true 
  }
}
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const { useUserStore } = await import('../stores/userStore.js')
  const userStore = useUserStore()
  
  if (!userStore.user && userStore.isAuthenticated) {
    await userStore.loadUser()
  }
  
  if (to.meta.requiresAuth && !userStore.isAuthenticated) {
    next('/auth')
  } 
  else if (to.meta.requiresAdmin && !userStore.user?.is_admin) {
    alert('У вас нет прав администратора')
    next('/profile')
  }
  else {
    next()
  }
})

export default router