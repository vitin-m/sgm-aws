"use server";

import { redirect } from "next/navigation";

import axiosInstance from "../../../../lib/axios";

export default async function LoginAction(fromData: FormData) {
  console.log("Login Action", fromData);
  const { email, password } = Object.fromEntries(fromData.entries());

  console.log("Data:", email, password);

  const params = new URLSearchParams();
  params.append("username", email.toString());
  params.append("password", password.toString());
  params.append("grant_type", "password");
  params.append("scope", "");
  params.append("client_id", "");
  params.append("client_secret", "");

  axiosInstance
    .post("/api/v1/login/access-token", params)
    .then((response) => {
      console.log("Login Success", response.data);
    })
    .catch((error) => {
      console.log("Login Error", error.toJSON());
    });

  redirect("/home");
}
