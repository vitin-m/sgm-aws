import axios from "axios";

const instance = axios.create({
  timeout: 10000,
  baseURL: "http://localhost:8000",
  headers: {
    Accept: "application/json",
    "Content-Type": "application/x-www-form-urlencoded",
  },
});

export default instance;
