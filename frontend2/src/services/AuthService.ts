import AxiosInstance from "./AxiosInstance";

export default {
  login: (email: string, password: string) => {
    const params = new URLSearchParams();
    params.append("username", email);
    params.append("password", password);
    params.append("grant_type", "password");
    params.append("scope", "");
    params.append("client_id", "");
    params.append("client_secret", "");

    return AxiosInstance.post("/login/access-token", params);
  },
};
