import AuthService from "../services/AuthService";
import IUserData from "../interfaces/IUserData";

export interface IAuthenticationState {
  token: null | string;
  userData: null | IUserData;
}

const state: IAuthenticationState = {
  token: null,
  userData: null,
};

export default {
  namespaced: true,
  state,
  getters: {
    getAllData: (state: IAuthenticationState): IAuthenticationState => state,
    isAuthenticated: (state: IAuthenticationState): boolean => !!state.token,
    getUserData: (state: IAuthenticationState): null | IUserData =>
      state.userData,
  },
  mutations: {
    setToken(state: IAuthenticationState, token: string) {
      state.token = token;
    },
    setUserData(state: IAuthenticationState, userData: IUserData) {
      state.userData = userData;
    },
  },
  actions: {
    async login({ commit }: any, { token, userData }: any) {
      await commit("setToken", token);
      await commit("setUserData", userData);
    },
    async logout({ commit }: any) {
      await commit("setToken", null);
      await commit("setUserData", null);
      localStorage.removeItem("__sgm-aws");
    },
    async fetchUserData({ commit }: any) {
      const token = localStorage.getItem("__sgm-aws");

      const response = await AuthService.getUserData();

      console.log("Response", response);

      if (response.status === 200) {
        await commit("setToken", token);
        await commit("setUserData", response.data);
      } else {
        await commit("setToken", null);
        await commit("setUserData", null);
      }
    },
  },
};
