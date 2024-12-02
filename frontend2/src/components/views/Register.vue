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
          label="Username"
          name="username"
          :rules="[{ required: true, message: 'Please input your username!' }]"
        >
          <a-input v-model:value="formState.username" />
        </a-form-item>

        <a-form-item
          label="Full Name"
          name="full_name"
          :rules="[{ required: true, message: 'Please input your full name!' }]"
        >
          <a-input v-model:value="formState.full_name" />
        </a-form-item>

        <!-- <a-form-item label="Description" name="description">
          <a-input v-model:value="formState.description" />
        </a-form-item> -->

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

        <!-- Imagem -->
        <a-form-item label="Profile Image" name="profileImage">
          <a-upload
            :maxCount="1"
            accept="image/png"
            v-model:file-list="formState.profileImage"
          >
            <a-button>Click to Upload</a-button>
          </a-upload>
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
import { useRouter } from "vue-router";

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
    formState.value.email,
    formState.value.password,
    formState.value.username,
    formState.value.full_name,
    formState.value.description,
    profileImageBase64
  )
    .then(async (response) => {
      console.log("REGISTER | response: ", response);
      router.push({ name: "login" });
    })
    .catch((error) => {
      console.log("REGISTER | error: ", error);
      alert("Erro ao registrar usuário");
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
  background: linear-gradient(135deg, #000000 0%, #fc2525 100%); 
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
      background: #fc0404;
      color: #fff;
      font-weight: bold;
      border: none;
      padding: 0.75rem;
      border-radius: 5px;
      transition: all 0.3s;

      &:hover {
        background: #2575fc;
        transform: translateY(-2px);
      }
    }
  }
}
</style>
