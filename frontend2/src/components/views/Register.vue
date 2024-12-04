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
        <h2 class="form-title">Registre-se</h2>
        <a-form-item
          label="Username"
          name="username"
          :rules="[{ required: true, message: 'Please input your username!' }]"
        >
          <a-input v-model:value="formState.username" />
        </a-form-item>

        <a-form-item
          label="Nome Completo"
          name="full_name"
          :rules="[{ required: true, message: 'Please input your full name!' }]"
        >
          <a-input v-model:value="formState.full_name" />
        </a-form-item>

        <a-form-item label="Description" name="description">
          <a-input v-model:value="formState.description" />
        </a-form-item>

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

        <!-- Imagem -->
        <a-form-item
          label="Imagem de Perfil"
          name="profileImage"
          :rules="[
            { required: true, message: 'Please input your profile image!' },
          ]"
        >
          <a-upload
            :maxCount="1"
            accept="image/png"
            v-model:file-list="formState.profileImage"
          >
            <a-button>Click to Upload</a-button>
          </a-upload>
        </a-form-item>

        <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
          <a-button type="primary" html-type="submit" class="btn-submit">
            Registrar
          </a-button>
        </a-form-item>
      </a-form>
    </div>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from "vue";

import AuthService from "../../services/AuthService";
import { useRouter } from "vue-router";

import { notification } from "ant-design-vue";

const router = useRouter();

const formState = ref({
  email: "",
  password: "",
  username: "",
  full_name: "",
  description: "",
  profileImage: null as null | any[],
});

const allowedFormats = ["jpeg", "png", "gif"];
const maxSizeInBytes = 2 * 1024 * 1024; // 2 MB
const handleSubmitRegister = async () => {
  console.log("REGISTER | formState: ", formState.value);

  let profileImageBase64 = null;

  if (formState.value.profileImage) {
    profileImageBase64 = await validateAndConvertImage(
      formState.value.profileImage[0].originFileObj as File,
      maxSizeInBytes,
      allowedFormats
    );
  }

  await AuthService.register(
    formState.value.full_name,
    formState.value.username,
    formState.value.email,
    formState.value.password,
    formState.value.description,
    profileImageBase64
  )
    .then(async (response) => {
      console.log("REGISTER | response: ", response);
      notification.success({
        message: "Success",
        placement: "bottomRight",
        description: "Novo usuário cadastrado com sucesso!",
      });
      router.push({ name: "login" });
    })
    .catch((error: any) => {
      console.log("REGISTER | error: ", error);

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
  background: linear-gradient(135deg, #a8c0ff, #fbc2eb);
  padding: 1rem;

  .session__form-content {
    width: 100%;
    max-width: 450px;
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

    .login-link {
      display: block;
      text-align: center;
      margin-top: 1.5rem;
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
  }
}
</style>


