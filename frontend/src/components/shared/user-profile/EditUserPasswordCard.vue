<template>
  <div class="edit-user-password">
    <!-- Form -->
    <a-form
      name="basic"
      autocomplete="off"
      :model="formState"
      :label-col="{ span: 8 }"
      :wrapper-col="{ span: 16 }"
      @finish="handleSubmitPassword"
      @finishFailed="handleSubmitPasswordFailed"
    >
      <h2 class="form-title">Alterar Senha</h2>

      <a-form-item
        label="Antiga Senha"
        name="oldPassword"
        :rules="[
          { required: true, message: 'Please input your old password!' },
        ]"
      >
        <a-input-password v-model:value="formState.oldPassword" />
      </a-form-item>

      <a-form-item
        label="Nova Senha"
        name="newPassword"
        :rules="[
          { required: true, message: 'Please input your new password!' },
        ]"
      >
        <a-input-password v-model:value="formState.newPassword" />
      </a-form-item>

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

interface Props {
  userData: IUserData;
}

interface IFormState {
  oldPassword: string;
  newPassword: string;
}

defineProps<Props>();

defineEmits(["cancel"]);

const formState = reactive<IFormState>({
  oldPassword: "",
  newPassword: "",
});

const handleSubmitPasswordFailed = (errorInfo: any) => {
  console.log("Failed:", errorInfo);
};

const handleSubmitPassword = (e: IFormState) => {
  console.log("Submitted", e);
};
</script>

<style scoped lang="scss">
.edit-user-password {
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
