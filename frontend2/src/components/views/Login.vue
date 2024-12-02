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
        <a-form-item
          label="E-mail"
          name="email"
          :rules="[{ required: true, message: 'Please input your email!' }]"
        >
          <a-input v-model:value="formState.email" />
        </a-form-item>

        <a-form-item
          label="Password"
          name="password"
          :rules="[{ required: true, message: 'Please input your password!' }]"
        >
          <a-input-password v-model:value="formState.password" />
        </a-form-item>

        <a-form-item name="remember" :wrapper-col="{ offset: 8, span: 16 }">
          <a-checkbox v-model:checked="formState.remember">
            Remember me
          </a-checkbox>
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
          <a-button type="primary" html-type="submit">Submit</a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

import AuthService from "../../services/AuthService";
import { AxiosResponse } from "axios";

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
    });
};

const fetchUserData = async () => {
  await AuthService.getUserData()
    .then((response) => {
      console.log("GET USER DATA | response: ", response);
    })
    .catch((error) => {
      console.log("GET USER DATA | error: ", error);
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

  .session__form-content {
    width: 300px;
  }
}
</style>
