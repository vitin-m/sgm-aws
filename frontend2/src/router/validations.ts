import { ComponentPublicInstance } from "vue";
import {
  RouteLocationRaw,
  RouteLocationNormalized,
  NavigationGuardNext,
} from "vue-router";
type NavigationGuardNextCallback = (vm: ComponentPublicInstance) => unknown;

async function routerValidations(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
) {
  const pathName = to.name;
  const pathUrl = to.path;

  // Home and Already Authenticated
  if (pathName == "login") {
    console.log("ROUTER VALIDATION | Login");
    const token = localStorage.getItem("__sgm-aws");

    if (token) {
      return next({ name: "dashboard" });
    }
  }

  // If trying to enter dashboard without login
  if (pathUrl.includes("dashboard")) {
    console.log("ROUTER VALIDATION | Dashboard");
    const token = localStorage.getItem("__sgm-aws");

    if (!token) {
      return next({ name: "login" });
    }
  }

  // Return default next route
  return next();
}

export default routerValidations;
