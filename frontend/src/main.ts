import { createApp } from "vue";
import "./styles/global.scss";
import App from "./App.vue";

// Ant Dv
import Antd from "ant-design-vue";
import "ant-design-vue/dist/reset.css";

// Vue Router
import router from "./router/router";

// VueX
import store from "./store/vuex";

const app = createApp(App);

app.use(Antd);
app.use(router);
app.use(store);

app.mount("#app");
