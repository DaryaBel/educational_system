<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else>
      <h1>Ваш аккаунт пока не был одобрен Администратором.</h1>
      <p>Ожидайте, обычно это занимает до одного дня.</p>
    </div>
  </div>
</template>
<script>
export default {
  name: "Moderation",
  computed: {
    isLoading() {
      return this.$store.state.isLoading;
    },
  },
};
</script>
