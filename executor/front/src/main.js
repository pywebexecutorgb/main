import Vue from 'vue'
import VueRouter from 'vue-router'
import VueClipboard from 'vue-clipboard2'
import {
  store
} from './store'

import methods from './methods.js'

import App from './App.vue'
import Code from './components/Code.vue'
import UserProfile from './components/UserProfile.vue'
import UserHistory from './components/UserHistory.vue'

/*
 * Optimize JS and CSS styles and load this imports only when it needs
 * import UserCreate from './components/UserCreate.vue'
 * import UserValidateEmail from './components/UserValidateEmail.vue'
 * import UserResetPassword from './components/UserResetPassword.vue'
 */

Vue.config.productionTip = false;

const router = new VueRouter({
  mode: 'history',
  routes: [
    // main code URLs
    {
      path: '/',
      component: Code
    },
    {
      path: '/code/:pk?',
      component: Code,
      props: true
    },

    // users URLs
    {
      path: '/user/profile',
      component: UserProfile
    },
    {
      path: '/user/history',
      component: UserHistory
    },

    // webpack optimization: built app as chunks with import
    {
      path: '/user/create',
      component: () => import('./components/UserCreate.vue')
    },
    {
      path: '/user/validate-email/:uid/:token',
      props: true,
      component: () => import('./components/UserValidateEmail.vue')
    },
    {
      path: '/user/reset-password/:uid/:token',
      props: true,
      component: () => import('./components/UserResetPassword.vue')
    },

    // redirect URLs
    {
      path: '/s/:hash',
      beforeEnter: (to, _, next) => methods.nextShortURL(to.params.hash, next),
    },
  ],
});

Vue.use(VueRouter);
Vue.use(VueClipboard);
new Vue({
  store,
  router,
  render: h => h(App),
}).$mount('#app');