import Vue from "vue";
import VueRouter from "vue-router";

import ExampleComponent from "@/components/ExampleComponent.vue";
import LogIn from "@/components/LogIn.vue";
import SignUp from "@/components/SignUp.vue";
import SignUpEmployee from "@/components/SignUpEmployee.vue";

const routes = [
  {
    path: "/login",
    name: "LogIn",
    component: LogIn,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
  },
  {
    path: "/signup-employee",
    name: "SignUpEmployee",
    component: SignUpEmployee,
  },
  { path: "/", component: ExampleComponent },
];

Vue.use(VueRouter);
const router = new VueRouter({
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 };
  },
  mode: "history",
  routes,
});

export default router;
