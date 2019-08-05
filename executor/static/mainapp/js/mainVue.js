Vue.use(VueRouter);

const router = new VueRouter({
  mode: 'history',
  routes: [
    {path: '/code/:pk', component: codeBlock, props: true},
    {path: '/', component: codeBlock},
  ],
});

const app = new Vue({
  el: '#app',
  router,
});
