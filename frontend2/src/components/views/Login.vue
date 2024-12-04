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
        <h3 class="form-title">Login</h3>

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
  background: linear-gradient(135deg, #a8c0ff, #fbc2eb);
  padding: 1rem;

  .session__form-content {
    width: 100%;
    max-width: 400px;
    background: rgba(255, 255, 255, 0.9);
    border-radius: 15px;
    box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.2);
    padding: 2.5rem;
    transform: translateY(10px);
    animation: fadeIn 1s ease forwards;

    @keyframes fadeIn {
      from {
        opacity: 0;
        transform: translateY(30px);
      }
      to {
        opacity: 1;
        transform: translateY(0);
      }
    }

    .form-title {
      text-align: center;
      margin-bottom: 2rem;
      color: #5c5edc;
      font-size: 1.8rem;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 1px;
    }

    a-form-item {
      margin-bottom: 1.5rem;

      input {
        border: 1px solid #d1d1d1;
        padding: 0.8rem;
        border-radius: 8px;
        transition: all 0.3s ease;

        &:focus {
          border-color: #5c5edc;
          box-shadow: 0 0 5px rgba(92, 94, 220, 0.5);
        }
      }
    }

    .btn-submit {
      width: 100%;
      margin: 0 auto; /* Centraliza o botão */
      display: block;
      background: linear-gradient(135deg, #6dd5ed, #2193b0);
      color: #ffffff;
      font-weight: bold;
      border: none;
      padding: 0.1rem;
      border-radius: 8px;
      font-size: 1rem;
      transition: all 0.3s ease;

      &:hover {
        background: linear-gradient(135deg, #2193b0, #6dd5ed);
        transform: scale(1.05);
        box-shadow: 0 4px 15px rgba(33, 147, 176, 0.5);
      }
    }

    .register-link {
      position: absolute; /* Posiciona o link no canto inferior direito */
      bottom: 1.5rem;
      right: 2rem;
      color: #5c5edc;
      text-decoration: none;
      font-weight: 600;
      transition: all 0.3s ease;

      &:hover {
        color: #333;
        text-decoration: underline;
        letter-spacing: 1px;
      }
    }

    position: relative; /* Necessário para que o position: absolute do register-link funcione */
  }
}
</style>


