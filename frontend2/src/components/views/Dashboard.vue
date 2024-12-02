<template>
  <div class="dashboard-session">
    <h1>Dashboard</h1>

    <!-- Usua'rio -->
    <div>
      <h2>Usuário</h2>
      <p>Nome: {{ userData.full_name }}</p>
      <p>Username: {{ userData.username }}</p>
      <p>Email: {{ userData.email }}</p>
      <p>Descrição: {{ userData.description }}</p>

      <img :src="userData.profile_pic" alt="Profile Image" />
    </div>
  </div>
</template>

<script setup lang="ts">
import IUserData from "@/interfaces/IUserData";
import { computed, onMounted } from "vue";
import { useStore } from "vuex";

onMounted(() => {
  console.log("Dashboard | userData: ", userData.value);
});

const store = useStore();

const userData = computed((): IUserData => store.getters["Auth/userData"]);
</script>

<style scoped></style>
