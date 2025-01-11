import { createRouter, createWebHistory, RouterOptions } from "vue-router";

import Login from "../components/views/Login.vue";
import Register from "../components/views/Register.vue";
import Dashboard from "../components/views/Dashboard.vue";
import UserProfile from "../components/views/UserProfile.vue";

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
    name: "user-profile",
    path: "/dashboard/user-profile",
    component: UserProfile,
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
