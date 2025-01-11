<template>
  <a-config-provider :locale="locale">
    <RouterView />
  </a-config-provider>
</template>

<script setup lang="ts">
import { ref } from "vue";
import pt_BR from "ant-design-vue/es/locale/pt_BR";

const locale = ref(pt_BR);
</script>

<style scoped lang="scss"></style>
