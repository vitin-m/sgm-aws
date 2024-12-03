<template>
  <div class="dashboard-session">
    <h1 class="dashboard-title">Dashboard</h1>
    <!-- Usua'rio -->
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

    <!-- Logout -->
    <a-button class="session__logout" @click="handleLogout">Logout</a-button>
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
</script>

<style scoped lang="scss">
.dashboard-session {
  height: 100vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  gap: 2rem;
  background: linear-gradient(135deg, #000000 0%, #fc2525 100%);
  color: white;
  padding: 2rem;

  .dashboard-title {
    font-size: 2rem;
    font-weight: bold;
    color: white;
  }

  .session__user-data {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0px 4px 20px rgba(0, 0, 0, 0.1);
    text-align: center;
    color: #333;
    width: 100%;
    max-width: 400px;

    .profile-img {
      width: 100px;
      height: 100px;
      border-radius: 50%;
      margin-bottom: 1rem;
    }

    .user_title {
      font-size: 1.5rem;
      font-weight: bold;
      color: #fc0404;
      margin-bottom: 1rem;
    }

    p {
      margin-bottom: 0.5rem;
    }

    .session__logout {
      background: #fc0404;
      color: white;
      font-weight: bold;
      border: none;
      padding: 0.75rem 2rem;
      border-radius: 5px;
      transition: all 0.3s;
    }

    .session__logout:hover {
      background: #fc2525;
      transform: translateY(-2px);
    }
  }
}
</style>
