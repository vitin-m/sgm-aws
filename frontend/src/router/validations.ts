import AuthService from "@/services/AuthService";
import { RouteLocationNormalized, NavigationGuardNext } from "vue-router";

async function routerValidations(
  to: RouteLocationNormalized,
  from: RouteLocationNormalized,
  next: NavigationGuardNext
): Promise<any> {
  const pathFrom = from.name;
  const pathName = to.name;
  const pathUrl = to.path;

  if (pathFrom == null) {
    console.log("ROUTER VALIDATION | First Load");
  }

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

    try {
      const response = await AuthService.getUserData();
      console.log("ROUTER VALIDATION | Get User Data", response);
    } catch (error) {
      localStorage.removeItem("__sgm-aws");
      return next({ name: "login" });
    }
  }

  // Return default next route
  return next();
}

export default routerValidations;
