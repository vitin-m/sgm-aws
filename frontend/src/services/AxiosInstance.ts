import axios from "axios";

const instance = axios.create({
  timeout: 10000,
  baseURL: import.meta.env.VITE_API_ROOT,
  headers: {
    Accept: "application/json",
    "Access-Control-Allow-Origin": "*",
    "Content-Type": "application/x-www-form-urlencoded",
  },
});

instance.interceptors.request.use(
  (requestConfig) => {
    // Adiciona o token Bearer a todas as requisições
    const token = localStorage.getItem("__sgm-aws");
    if (token) {
      requestConfig.headers["Authorization"] = `Bearer ${token}`;
    }

    return requestConfig;
  },
  (error) => {
    // Lida com erros de requisição
    return Promise.reject(error);
  }
);

export default instance;
