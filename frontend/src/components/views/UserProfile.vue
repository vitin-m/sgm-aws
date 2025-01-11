<template>
  <div class="dashboard-session">
    <!-- Navbar -->
    <DashboardHeader :userData="userData" />

    <div class="dashboard-content">
      <!-- Usuário -->
      <a-spin v-if="!userData" size="large" />

      <template v-else>
        <ProfileDataCard
          v-if="modeManager.mode === 'default'"
          :userData="userData"
          @editProfile="modeManager.setEditProfileMode()"
          @editPassword="modeManager.setEditPasswordMode()"
        />

        <EditUserPasswordCard
          :userData="userData"
          @cancel="modeManager.setDefaultMode()"
          v-if="modeManager.mode === 'edit-password'"
        />

        <EditUserProfileCard
          :userData="userData"
          @cancel="modeManager.setDefaultMode()"
          v-if="modeManager.mode === 'edit-profile'"
        />
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import DashboardHeader from "../shared/dashboard/DashboardHeader.vue";
import ProfileDataCard from "../shared/user-profile/ProfileDataCard.vue";
import EditUserPasswordCard from "../shared/user-profile/EditUserPasswordCard.vue";
import EditUserProfileCard from "../shared/user-profile/EditUserProfileCard.vue";

import { useStore } from "vuex";
import { computed, onBeforeMount, onMounted, reactive } from "vue";

import IUserData from "../../interfaces/IUserData";

type IModeType = "default" | "edit-profile" | "edit-password";

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

const modeManager = reactive({
  mode: "default" as IModeType,
  setEditProfileMode() {
    this.mode = "edit-profile";
  },
  setEditPasswordMode() {
    this.mode = "edit-password";
  },
  setDefaultMode() {
    this.mode = "default";
  },
});
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
