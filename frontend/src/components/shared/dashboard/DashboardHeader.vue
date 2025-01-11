<template>
  <nav class="navbar">
    <!-- Title -->
    <h1 class="navbar-title" @click="handleOpenHome">SGM-AWS</h1>

    <!-- Menu -->
    <div class="nav-profile-box">
      <!-- Profile -->
      <div class="my-profile" @click="handleOpenUserProfile">
        <img
          alt="Profile Image"
          class="navbar-profile"
          :src="
            userData?.profile_pic
              ? 'data:image/png;base64,' + userData.profile_pic
              : 'https://thumbs.dreamstime.com/b/perfil-de-usu%C3%A1rio-do-vetor-avatar-padr%C3%A3o-179376714.jpg'
          "
        />
        <span>Meu Perfil</span>
      </div>

      <!-- Home -->
      <a-button class="session__home" @click="handleOpenHome"> Home </a-button>

      <!-- Logout -->
      <a-button class="session__logout" @click="handleLogout">
        Logout
      </a-button>
    </div>
  </nav>
</template>

<script setup lang="ts">
import IUserData from "@/interfaces/IUserData";
import { computed } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

const store = useStore();
const router = useRouter();

const userData = computed(
  (): IUserData | null => store.getters["Auth/getUserData"]
);

async function handleLogout() {
  await store.dispatch("Auth/logout");
  router.push({ name: "login" });
}

function handleOpenUserProfile() {
  router.push({ name: "user-profile" });
}

function handleOpenHome() {
  router.push({ name: "dashboard" });
}
</script>

<style scoped lang="scss">
.navbar {
  width: 100%;
  height: 60px;
  background: #6dd5ed; /* Azul suave */
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 1rem;
  position: fixed;
  top: 0;
  left: 0;
  z-index: 10;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);

  .navbar-title {
    font-size: 1.5rem;
    color: white;
    font-weight: bold;
    width: 100%;
    height: 30%;
    text-align: left;
    padding: 0rem;

    &:hover {
      cursor: pointer;
    }
  }

  .nav-profile-box {
    display: flex;
    align-items: center;

    gap: 1rem;
  }

  .my-profile {
    display: flex;
    align-items: center;

    padding: 0.5rem 1rem;
    border-radius: 8px;

    span {
      width: max-content;
      margin-left: 1rem;
      font-weight: bold;
      color: white;
    }

    &:hover {
      cursor: pointer;
      background-color: rgba(255, 255, 255, 0.2);
    }

    .navbar-profile {
      width: 40px;
      height: 40px;
      border-radius: 50%;
      cursor: pointer;
      border: 2px solid white;
      transition: all 0.3s;

      &:hover {
        transform: scale(1.1);
        border-color: #5c5edc; /* Azul suave de hover */
      }
    }
  }

  .session__logout {
    background: rgba(92, 94, 220, 0.5);
    color: white;
    font-weight: bold;
    border: none;
    padding: 0.1rem 2rem;
    border-radius: 8px;
    font-size: 1rem;
    transition: all 0.3s ease;

    &:hover {
      background: #5c5edc;
      transform: scale(1.05);
      box-shadow: 0 4px 15px rgba(92, 94, 220, 0.5);
    }
  }
}
</style>
