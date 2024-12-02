import axios from "axios";

const instance = axios.create({
  timeout: 10000,
  baseURL: process.env["BACKEND_HOST"],
  headers: {
    Accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  },
});

console.log('AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA', instance);
export default instance;
