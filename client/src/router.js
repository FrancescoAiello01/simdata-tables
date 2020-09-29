import Vue from 'vue';
import Router from 'vue-router';
import Home from './components/Home.vue';
import Calculate from './components/Calculate.vue';

Vue.use(Router);

export default new Router({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: [
    {
      path: '/',
      name: 'Home',
      component: Home,
    },
    {
      path: '/calculate',
      name: 'Calculate',
      component: Calculate,
    },
  ],
});
