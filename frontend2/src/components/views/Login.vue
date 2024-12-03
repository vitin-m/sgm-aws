<template>
  <div class="login-session">
    <div class="session__form-content">
      <a-form
        :model="formState"
        name="basic"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 16 }"
        autocomplete="off"
        @finish="handleSubmitLogin"
        @finishFailed="handleSubmitLoginFailed"
      >
        <h2 class="form-title">Login</h2>

        <a-form-item
          label="E-mail"
          name="email"
          :rules="[{ required: true, message: 'Please input your email!' }]"
        >
          <a-input v-model:value="formState.email" />
        </a-form-item>

        <a-form-item
          label="Senha"
          name="password"
          :rules="[{ required: true, message: 'Please input your password!' }]"
        >
          <a-input-password v-model:value="formState.password" />
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
          <a-button type="primary" html-type="submit" class="btn-submit">
            Login
          </a-button>
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
          <router-link to="/register" class="register-link">
            Registre-se
          </router-link>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

import AuthService from "../../services/AuthService";
import { AxiosResponse } from "axios";

import IUserData from "../../interfaces/IUserData";
import { useStore } from "vuex";
import { useRouter } from "vue-router";
import { notification } from "ant-design-vue";

const store = useStore();
const route = useRouter();

interface FormState {
  email: string;
  password: string;
  remember: boolean;
}

const formState = reactive<FormState>({
  email: "",
  password: "",
  remember: true,
});

const handleSubmitLogin = async (values: any) => {
  console.log("Success:", values);

  await AuthService.login(formState.email, formState.password)
    .then(
      (
        response: AxiosResponse<{ access_token: string; token_type: string }>
      ) => {
        console.log("LOGIN | response: ", response);
        const token = response.data.access_token;
        localStorage.setItem("__sgm-aws", token);
        fetchUserData();
      }
    )
    .catch((error) => {
      console.log("LOGIN | error: ", error);

      if (typeof error.response.data.detail === "string") {
        notification.error({
          message: "Error",
          placement: "bottomRight",
          description: error.response.data.detail,
        });
      } else {
        notification.error({
          message: "Error",
          placement: "bottomRight",
          description: error.response.data.detail[0].msg,
        });
      }
    });
};

const fetchUserData = async () => {
  await AuthService.getUserData()
    .then(async (response: AxiosResponse<IUserData>) => {
      console.log("GET USER DATA | response: ", response);
      const token = import.meta.env.VITE_API_ROOT;
      await store.dispatch("Auth/login", {
        token,
        userData: {
          ...response.data,
        },
      });

      route.push({ name: "dashboard" });
    })
    .catch((error) => {
      console.log("GET USER DATA | error: ", error);
      alert("Get user data failed");
    });
};

const handleSubmitLoginFailed = (errorInfo: any) => {
  console.log("Failed:", errorInfo);
};
</script>

<style scoped lang="scss">
.login-session {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(135deg, #000000 0%, #fc2525 100%);
  padding: 1rem;

  .session__form-content {
    width: 100%;
    max-width: 400px;
    background: #fff;
    border-radius: 10px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    padding: 2rem;

    .form-title {
      text-align: center;
      margin-bottom: 1.5rem;
      color: #333;
      font-size: 1.8rem;
      font-weight: 600;
    }

    .btn-submit {
      width: 100%;
      background: #ff0000;
      color: #ffffff;
      font-weight: bold;
      border: none;
      padding: 0.2rem;
      border-radius: 5px;
      transition: all 0.3s;

      &:hover {
        background: #ff0404;
        transform: translateY(-2px);
      }
    }
    .register-link {
      display: inline-block;
      text-align: right;
      width: 100%;
      transform: translateY(-1.5rem);
      //margin-top: 0rem;
      color: #ff0404;
      text-decoration: none;
      font-weight: 600;
      transition: all 0.3s;

      &:hover {
        color: #2575fc;
        text-decoration: underline;
      }
    }
  }
}
</style>
