<template>
  <div>
    <h1>Вы действительно хотите удалить аккаунт?</h1>
    <button @click="backToProfile()">Нет</button>
    <button @click="deleteAccount()">Да</button>
  </div>
</template>
<script>
export default {
  name: "DeleteAccount",
  methods: {
    backToProfile() {
      this.$router.push({ name: "Profile" });
    },
    deleteAccount() {
      //удалить аккаунт
      this.$router.push({ path: "/" });
    },
  },
};
</script>
