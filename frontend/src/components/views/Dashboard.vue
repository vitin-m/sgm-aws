<template>
  <div class="dashboard-session">
    <!-- Navbar -->
    <DashboardHeader :userData="userData" />

    <a-spin
      size="large"
      v-if="!userData"
      :style="{
        margin: 'auto',
      }"
    />

    <div v-else class="dashboard-content">
      <!-- Search -->
      <div class="content__search-container">
        <a-select
          size="large"
          style="width: 120px"
          :options="typeOptions"
          v-model:value="tableFilter.type"
        />

        <a-input-search
          size="large"
          enter-button
          v-model:value="tableFilter.search"
          placeholder="Pesquise um item na sua biblioteca."
        />
      </div>

      <!-- Table -->
      <a-table :columns="tableColumns" :data-source="tableData">
        <template #bodyCell="{ column, record }">
          <template v-if="column.key === 'name'">
            <a>
              {{ record.name }}
            </a>
          </template>
        </template>
      </a-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import DashboardHeader from "../shared/dashboard/DashboardHeader.vue";

import { useStore } from "vuex";
import { computed, onBeforeMount, onMounted, reactive, ref } from "vue";

import IUserData from "../../interfaces/IUserData";
import { SelectProps, TableColumnsType } from "ant-design-vue";

type IArchiveType = "all" | "image" | "video" | "audio";

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

const tableFilter = reactive({
  search: "" as string,
  type: "all" as IArchiveType,
});

const tableData = ref([]);

const tableColumns = ref<TableColumnsType>([
  {
    dataIndex: "name",
    key: "name",
    title: "Nome do Arquivo",
  },
  {
    dataIndex: "description",
    key: "description",
    title: "Descrição",
  },
  {
    dataIndex: "metadata",
    key: "metadata",
    title: "Meta Dados",
  },
  {
    dataIndex: "size",
    key: "size",
    title: "Tamanho",
  },
  {
    dataIndex: "uploadAt",
    key: "uploadAt",
    title: "Data de Upload",
  },
  {
    key: "MIMEType",
    dataIndex: "MIMEType",
    title: "MIME Type",
  },
  {
    key: "tags",
    dataIndex: "tags",
    title: "Tags",
  },
  {
    key: "options",
    dataIndex: "options",
    title: "Opções",
  },
]);

const typeOptions = ref<SelectProps["options"]>([
  { value: "all", label: "Todos" },
  { value: "image", label: "Imagens" },
  { value: "video", label: "Vídeos" },
  { value: "audio", label: "Áudios" },
]);
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
    flex-direction: column;

    padding: 80px 2rem; /* 80px para evitar sobreposição da navbar */
    align-items: center;
    justify-content: center;

    gap: 1rem;

    .content__search-container {
      width: 60vw;
      max-width: 600px;

      display: flex;
      gap: 1rem;
      justify-content: center;
    }
  }
}
</style>
