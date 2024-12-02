<template>
  <div class="register-session">
    <div class="session__form-content">
      <a-form
        :model="formState"
        name="basic"
        :label-col="{ span: 8 }"
        :wrapper-col="{ span: 16 }"
        autocomplete="off"
        @finish="handleSubmitRegister"
        @finishFailed="handleSubmitRegisterFailed"
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

        <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
          <a-button type="primary" html-type="submit">Submit</a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";

import AuthService from "../../services/AuthService";

const formState = ref({
  email: "",
  password: "",
  username: "",
  full_name: "",
  description: "",
  profileImage: null,
});

const allowedFormats = ["jpeg", "png", "gif"];
const maxSizeInBytes = 2 * 1024 * 1024; // 2 MB

const handleSubmitRegister = async (values: any) => {
  console.log("Success:", values);

  let profileImageBase64 = null;

  if (formState.value.profileImage) {
    profileImageBase64 = await validateAndConvertImage(
      formState.value.profileImage,
      maxSizeInBytes,
      allowedFormats
    );
  }

  await AuthService.register(
    formState.value.email,
    formState.value.password,
    formState.value.username,
    formState.value.full_name,
    formState.value.description,
    profileImageBase64
  )
    .then(async (response) => {
      console.log("REGISTER | response: ", response);
    })
    .catch((error) => {
      console.log("REGISTER | error: ", error);
    });
};

const handleSubmitRegisterFailed = (errorInfo: any) => {
  console.log("Failed:", errorInfo);
};

async function validateAndConvertImage(
  file: File,
  maxSizeInBytes: number,
  allowedFormats: string[]
): Promise<string> {
  // Verifica o formato da imagem
  const fileFormat = file.type.split("/")[1];
  if (!allowedFormats.includes(fileFormat)) {
    throw new Error(
      `Formato de imagem não permitido. Formatos permitidos: ${allowedFormats.join(
        ", "
      )}`
    );
  }

  // Verifica o tamanho da imagem
  if (file.size > maxSizeInBytes) {
    throw new Error(
      `O tamanho da imagem não pode exceder ${maxSizeInBytes / 1024 / 1024} MB`
    );
  }

  // Converte a imagem para Base64
  const base64String = await convertToBase64(file);
  return base64String;
}

function convertToBase64(file: File): Promise<string> {
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = () => {
      const base64String = reader.result as string;
      const base64Data = base64String.split(",")[1]; // Remove o prefixo data:image/png;base64,
      resolve(base64Data);
    };
    reader.onerror = (error) => reject(error);
  });
}
</script>

<style scoped lang="scss">
.register-session {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;

  .session__form-content {
    width: 300px;
  }
}
</style>
