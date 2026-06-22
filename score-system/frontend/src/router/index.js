import { createRouter, createWebHistory } from 'vue-router';
import { useAuthStore } from '../store/auth';

const routes = [
  { path: '/login', component: () => import('../views/Login.vue') },
  {
    path: '/dashboard',
    component: () => import('../views/Dashboard.vue'),
    meta: { requiresAuth: true }
  },
  {
    path: '/scores',
    component: () => import('../views/Scores.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'student'] }
  },
  {
    path: '/report',
    component: () => import('../views/Report.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'admin'] }
  },
  {
    path: '/admin',
    component: () => import('../views/Admin.vue'),
    meta: { requiresAuth: true, roles: ['admin'] }
  },
  { path: '/', redirect: '/login' },
  { path: '/countdown', component: () => import('../views/countdown/CountdownPage.vue') }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const auth = useAuthStore();
  if (to.meta.requiresAuth && !auth.token) {
    next('/login');
  } else if (to.meta.roles && !to.meta.roles.includes(auth.user.role)) {
    next('/login');
  } else {
    next();
  }
});

export default router;
