import Vue from "vue";
import Vuelidate from "vuelidate";
import store from "@/store";
import router from "@/router";

import { createProvider } from "@/apollo";

import { BootstrapVue, IconsPlugin } from "bootstrap-vue";

import "bootstrap/dist/css/bootstrap.css";
import "bootstrap-vue/dist/bootstrap-vue.css";

Vue.use(BootstrapVue);

Vue.use(IconsPlugin);

// import VueYandexMetrika from "vue-yandex-metrika";

import App from "@/App.vue";
import "./registerServiceWorker";

Vue.use(Vuelidate);
Vue.config.productionTip = false;

// more info: https://github.com/vchaptsev/vue-yandex-metrika
// Vue.use(VueYandexMetrika, {
//   id: process.env.VUE_APP_YANDEX_METRIKA,
//   env: process.env.NODE_ENV,
//   router
// })

new Vue({
  router,
  store,
  provide: createProvider().provide(),
  render: (h) => h(App),
}).$mount("#app");
