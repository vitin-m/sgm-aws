<template >
  <div class="dashboard">
    <header class="dashboard-header">
      <img
        alt="Profile Image"
        class="profile-img"
        :src="'/ufpi.png'"
      />
      <div>
        <button @click="toggleOptions">Menu</button>
        <ul v-if="showOptions" class="options-list">
          <li v-for="option in options" :key="option.text">
            <router-link :to="option.link">{{ option.text }}</router-link>
          </li>
        </ul>
      </div>
    </header>
    <main class="dashboard-content">
      <section class="card">
        <h2>Bem vindo</h2>
        <p>Informações do usuário</p>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      showOptions: false,
      options: [
        { text: 'Home', link: '/home' },
        { text: 'Editar perfil', link: '/edit' },
        { text: 'Sair', link: '/' }
      ]
    };
  },
  methods: {
    toggleOptions() {
      this.showOptions = !this.showOptions;
    }
  }
};
</script>

<style lang="scss" scoped>
.profile-img {
  width: 25px;
  height: 25px;
  border-radius: 50%; 
  object-fit: cover; 
  background: red;
}

button {
  background-color: red;
  color: #000;
  padding: 5px 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  &:hover {
    background-color: rgb(221, 0, 0);
  }
  border-radius: 4px;
}

.dashboard-content {
  padding-top: 50px;
}

.dashboard {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 20px;
  background-color: #f9f9f9;
  height: 100vh;

  &-header {
    position: fixed;
    top: 0; 
    background: linear-gradient(135deg, #330000 0%, #fc2525 100% );
    color: #fff;
    padding: 10px;
    width: 100%;
    text-align: center;
    display: flex;
    justify-content: space-between;
    border-bottom: 1px solid #000;

    .options-list {
      position: absolute;
      right: 0;
      background-color: #ececec;
      border: 1px solid #000;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
      border-radius: 4px;
      
      width: 130px;
      list-style: none;
      padding: 10px;
      margin: 0;
      margin-top: 5px;
      z-index: 1000; /* Certifique-se de que o z-index seja maior que o do header */
    }
    
    .options-list li {
      padding: 5px 10px;
      cursor: pointer;
      color: red;
    }

    .options-list li:hover {
      background-color: #c5c5c5;
    }
  }
  
  &-content {
    display: flex;
    justify-content: space-around;
    width: 100%;
    margin-top: 20px;
    

    .card {
      background-color: #e4e4e4;
      border: 1px solid #000;
      border-radius: 5px;
      padding: 20px;
      width: 45%;
      box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);

      h2 {
        margin-top: 0;
      }
    }
  }
}
</style>