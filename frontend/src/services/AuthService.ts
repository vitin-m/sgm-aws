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
  logout: () => {
    localStorage.removeItem("__sgm-aws");
  },
  getUserData: () => {
    return AxiosInstance.get("/user/me");
  },
  register: (
    fullname: string,
    username: string,
    email: string,
    password: string,
    description?: string,
    profileImage?: string | null
  ) => {
    return AxiosInstance.post(
      "/user/signup",
      {
        email: email,
        password: password,
        username: username,
        full_name: fullname,
        description: description,
        profile_pic: profileImage ?? undefined,
      },
      {
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
  },
};
