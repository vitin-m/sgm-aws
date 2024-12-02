import axios from "axios";

const instance = axios.create({
  timeout: 10000,
  baseURL: import.meta.env.VITE_API_ROOT,
  headers: {
    Accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  },
});

export default instance;
