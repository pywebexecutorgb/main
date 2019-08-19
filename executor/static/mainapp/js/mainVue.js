Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {path: '/code/:pk', component: codeBlock, props: true},
    {path: '/', component: codeBlock},
    {path: '/user/create', component: createUser},
    {path: '/user/verify/:uid/:token', component: verifyEmail}
  ],
});

const app = new Vue({
  el: '#app',
  router,

  components: {
    login,
  },
});
