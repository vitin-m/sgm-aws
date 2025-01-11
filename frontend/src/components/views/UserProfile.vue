<template>
  <div class="dashboard-session">
    <!-- Navbar -->
    <DashboardHeader :userData="userData" />

    <div class="dashboard-content">
      <!-- Usuário -->
      <a-spin v-if="!userData" size="large" />
      <ProfileDataCard v-else :userData="userData" />
    </div>
  </div>
</template>

<script setup lang="ts">
import ProfileDataCard from "../shared/user-profile/ProfileDataCard.vue";
import DashboardHeader from "../shared/dashboard/DashboardHeader.vue";

import { useStore } from "vuex";
import { computed, onBeforeMount, onMounted } from "vue";

import IUserData from "../../interfaces/IUserData";

onBeforeMount(async () => {
  await store.dispatch("Auth/fetchUserData");
});

onMounted(() => {
  console.log("Dashboard | user Data: ", userData.value);
});

const store = useStore();

const userData = computed(
  (): IUserData | null => store.getters["Auth/getUserData"]
);
</script>

<style scoped lang="scss">
.dashboard-session {
  height: 100vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  background: linear-gradient(
    135deg,
    #a8c0ff,
    #fbc2eb
  ); /* Suavizando o gradiente */
  color: white;

  .dashboard-content {
    width: 100%;
    height: 100%;

    display: flex;
    flex-direction: row;

    padding: 80px 2rem; /* 80px para evitar sobreposição da navbar */
    align-items: center;
    justify-content: center;
  }
}
</style>
