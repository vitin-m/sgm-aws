<template>
  <div class="dashboard-session">
    <!-- Navbar -->
    <nav class="navbar">
      <h1 class="navbar-title">SGM-AWS</h1>
      <div class="nav-profile-box">
        <img
          alt="Profile Image"
          :src="
            userData?.profile_pic
              ? 'data:image/png;base64,' + userData.profile_pic
              : 'https://thumbs.dreamstime.com/b/perfil-de-usu%C3%A1rio-do-vetor-avatar-padr%C3%A3o-179376714.jpg'
          "
          class="navbar-profile"
          @click="navigateToMe"
        />
        
        <!-- Logout -->
        <a-button class="session__logout" @click="handleLogout">Logout</a-button>
      </div>
    </nav>

    <div class="dashboard-content">
      <!-- Usuário -->
      <div v-if="userData" class="session__user-data">
        <img
          alt="Profile Image"
          :src="
            userData.profile_pic
              ? 'data:image/png;base64,' + userData.profile_pic
              : 'https://thumbs.dreamstime.com/b/perfil-de-usu%C3%A1rio-do-vetor-avatar-padr%C3%A3o-179376714.jpg'
          "
          class="profile-img"
        />

        <h2 class="user-title">Usuário</h2>
        <p><strong>Username:</strong> {{ userData.username }}</p>
        <p><strong>Nome:</strong> {{ userData.full_name }}</p>
        <p><strong>Email:</strong> {{ userData.email }}</p>
        <p>
          <strong>Descrição:</strong>
          {{ userData.description ? userData.description : "Sem Descrição" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import IUserData from "../../interfaces/IUserData";
import { computed, onBeforeMount, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

onBeforeMount(async () => {
  const loggedUser: null | IUserData = await store.dispatch(
    "Auth/fetchUserData"
  );
  if (!loggedUser) {
    console.log("Dashboard | User not logged in");
    handleLogout();
  }
});

onMounted(() => {
  console.log("Dashboard | user Data: ", userData.value);
});

const store = useStore();
const router = useRouter();

const userData = computed(
  (): IUserData | null => store.getters["Auth/getUserData"]
);

async function handleLogout() {
  await store.dispatch("Auth/logout");
  router.push({ name: "login" });
}

function navigateToMe() {
  router.push({ path: "/me" });
}
</script>

<style scoped lang="scss">
.dashboard-session {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(135deg, #a8c0ff, #fbc2eb); /* Suavizando o gradiente */
  color: white;

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
    }
    .nav-profile-box{
      display: flex;
      align-items: center;
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
    .session__logout {
      margin-left: 2rem;
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

  .dashboard-content {
    display: flex;
    flex-direction: row;
    justify-content: flex-start;
    align-items: flex-start;
    width: 100%;
    padding: 80px 2rem; /* 80px para evitar sobreposição da navbar */

    .session__user-data {
      background: rgba(255, 255, 255, 0.9); /* Transparente e suave */
      padding: 1.5rem;
      border-radius: 15px;
      box-shadow: 0px 8px 30px rgba(0, 0, 0, 0.2);
      color: #333;
      width: 100%;
      max-width: 300px;
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

      .profile-img {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        margin-bottom: 1rem;
      }

      .user-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #5c5edc; /* Cor suave de título */
        margin-bottom: 1rem;
      }

      p {
        margin-bottom: 0.5rem;
      }
    }
  }
}
</style>

