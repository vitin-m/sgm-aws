<template>
  <div class="edit-user-profile">
    <!-- Form -->
    <a-form
      name="basic"
      autocomplete="off"
      :model="formState"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      @finish="handleSubmitProfile"
      @finishFailed="handleSubmitProfileFailed"
    >
      <h2 class="form-title">Alterar Dados do Perfil</h2>

      <!-- Full Name -->
      <a-form-item
        label="Nome Completo"
        name="full_name"
        :rules="[{ required: true, message: 'Please input your full name!' }]"
      >
        <a-input v-model:value="formState.full_name" />
      </a-form-item>

      <!-- Description -->
      <a-form-item label="Description" name="description">
        <a-input v-model:value="formState.description" />
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

      <!-- Options -->
      <a-form-item :wrapper-col="{ offset: 8, span: 16 }">
        <a-button type="primary" html-type="submit" class="btn-submit">
          Salvar
        </a-button>

        <a-button
          type="default"
          @click="$emit('cancel')"
          style="margin-left: 10px"
        >
          Voltar
        </a-button>
      </a-form-item>
    </a-form>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";

import IUserData from "@/interfaces/IUserData";
import ParseImageToBase64 from "@/utils/ParseImageToBase64";

interface Props {
  userData: IUserData;
}

interface IFormState {
  full_name: string;
  description: string;
  profileImage: null | any[];
}

defineProps<Props>();

defineEmits(["cancel"]);

const allowedFormats = ["jpeg", "png", "gif"];
const maxSizeInBytes = 2 * 1024 * 1024; // 2 MB

const formState = reactive<IFormState>({
  full_name: "",
  description: "",
  profileImage: null as null | any[],
});

const handleSubmitProfileFailed = (errorInfo: any) => {
  console.log("Failed:", errorInfo);
};

const handleSubmitProfile = async (e: IFormState) => {
  let profileImageBase64 = null;

  if (formState.profileImage) {
    profileImageBase64 = await ParseImageToBase64(
      formState.profileImage[0].originFileObj as File,
      maxSizeInBytes,
      allowedFormats
    );
  }

  console.log("Submitted", { ...e, profileImageBase64 });
};
</script>

<style scoped lang="scss">
.edit-user-profile {
  width: 100%;
  max-width: 500px;

  padding: 3rem 2.5rem;

  transform: translateY(10px);
  animation: fadeIn 1s ease forwards;

  color: #333;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.2);

  display: flex;
  flex-direction: column;
  gap: 1rem;

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
}
</style>
