import { createRouter, createWebHistory, RouterOptions } from "vue-router";

import Login from "../components/views/Login.vue";
import Register from "../components/views/Register.vue";
import Dashboard from "../components/views/Dashboard.vue";
import Home from "../components/views/home.vue";

import routerValidations from "./validations.ts";

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
  {
    name: "dashboard",
    path: "/dashboard",
    component: Dashboard,
  },
  {
    name: "home",
    path: "/home",
    component: Home,
  },

] as RouterOptions["routes"];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

// Router Validations
router.beforeResolve(async (to, from, next) => {
  return (await routerValidations(to, from, next)) || next();
});

export default router;
