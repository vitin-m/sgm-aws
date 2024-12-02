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
    login({ commit }: any, { token, userData }: any) {
      commit("setToken", token);
      commit("setUserData", userData);
    },
    logout({ commit }: any) {
      commit("setToken", null);
      commit("setUserData", null);
    },
  },
};
