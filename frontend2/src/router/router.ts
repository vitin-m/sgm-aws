import { createRouter, createWebHistory, RouterOptions } from "vue-router";

import Login from "../components/views/Login.vue";
import Register from "../components/views/Register.vue";

const routes = [
  {
    name: "login",
    path: "/",
    component: Login,
  },
  {
    name: "register",
    path: "/register",
    component: Register,
  },
] as RouterOptions["routes"];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
