<template>
  <div class="profile-data-card">
    <h2 class="user-title">Perfil do Usuário</h2>

    <img
      alt="Profile Image"
      class="profile-img"
      :src="
        userData.profile_pic
          ? 'data:image/png;base64,' + userData.profile_pic
          : 'https://thumbs.dreamstime.com/b/perfil-de-usu%C3%A1rio-do-vetor-avatar-padr%C3%A3o-179376714.jpg'
      "
    />

    <p><strong>Nome de Usuário:</strong> {{ userData.username }}</p>
    <p><strong>Nome Completo:</strong> {{ userData.full_name }}</p>
    <p><strong>Email:</strong> {{ userData.email }}</p>
    <p>
      <strong>Descrição:</strong>
      {{ userData.description ? userData.description : "Sem Descrição" }}
    </p>
    <p>
      <strong>Data de Criação:</strong>
      {{ DataParse.UTCToLocal(userData.created_at, "DD/MM/YYYY") }}
    </p>

    <!-- Options -->
    <div class="profile__options">
      <a-button
        type="default"
        :icon="h(EditOutlined)"
        @click="$emit('editProfile')"
      >
        Editar Perfil
      </a-button>

      <a-button
        type="default"
        :icon="h(KeyOutlined)"
        @click="$emit('editPassword')"
      >
        Alterar Senha
      </a-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { h } from "vue";
import { EditOutlined, KeyOutlined } from "@ant-design/icons-vue";

import IUserData from "@/interfaces/IUserData";
import DataParse from "@/utils/DataParse";

interface Props {
  userData: IUserData;
}

defineProps<Props>();

defineEmits(["editProfile", "editPassword"]);
</script>

<style scoped lang="scss">
.profile-data-card {
  padding: 3rem 2.5rem;
  max-width: 500px;

  transform: translateY(10px);
  animation: fadeIn 1s ease forwards;

  color: #333;
  border-radius: 15px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.2);

  display: flex;
  flex-direction: column;

  gap: 1rem;
  align-items: center;
  justify-content: center;

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

  p {
    margin-bottom: 0rem;
  }

  .profile__options {
    display: flex;
    gap: 1rem;
  }

  .profile-img {
    width: 135px;
    height: 135px;
    border-radius: 50%;
    margin-bottom: 1 rem;
  }

  .user-title {
    font-size: 1.5rem;
    font-weight: bold;
    color: #5c5edc;
    margin-bottom: 1rem;
  }
}
</style>
