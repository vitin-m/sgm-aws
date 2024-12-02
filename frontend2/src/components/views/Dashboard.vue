<template>
  <div class="dashboard-session">
    <h1>Dashboard</h1>
    <!-- Usua'rio -->
    <div v-if="userData" class="session__user-data">
      <img
        alt="Profile Image"
        :src="
          userData.profile_pic
            ? 'data:image/png;base64,' + userData.profile_pic
            : 'https://thumbs.dreamstime.com/b/perfil-de-usu%C3%A1rio-do-vetor-avatar-padr%C3%A3o-179376714.jpg'
        "
      />

      <h2>Usuário</h2>
      <p><strong>Username:</strong> {{ userData.username }}</p>
      <p><strong>Nome:</strong> {{ userData.full_name }}</p>
      <p><strong>Email:</strong> {{ userData.email }}</p>
      <!-- <p><strong>Criado em:</strong> {{ userData.createdAt }}</p> -->
      <p><strong>Descrição:</strong> {{ userData.description }}</p>
    </div>

    <!-- Logout -->
    <a-button class="session__logout" @click="handleLogout">Logout</a-button>
  </div>
</template>

<script setup lang="ts">
import IUserData from "@/interfaces/IUserData";
import { computed, onBeforeMount, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useStore } from "vuex";

onBeforeMount(async () => {
  await store.dispatch("Auth/fetchUserData");
});

onMounted(() => {
  console.log("Dashboard | userData: ", userData.value);
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
  align-items: center;
  gap: 1rem;

  .session__user-data {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;

    img {
      width: 100px;
      height: 100px;
      border-radius: 50%;
    }
  }

  .session__logout {
    margin-top: 20px;
  }
}
</style>
