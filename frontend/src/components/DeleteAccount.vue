<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else>
      <h1>Вы действительно хотите удалить аккаунт?</h1>
      <button @click="backToProfile()">Нет</button>
      <button @click="deleteAccount()">Да</button>
    </div>
  </div>
</template>
<script>
import jwt from "jsonwebtoken";
import { DELETE_USER } from "@/graphql/mutations/mutations";

export default {
  name: "DeleteAccount",
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
  },
  methods: {
    backToProfile() {
      this.$router.push({ name: "Profile" });
    },
    deleteAccount() {
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({
          mutation: DELETE_USER,
          variables: {
            userId: this.userId,
            p,
          },
        })
        .then(() => {
          localStorage.removeItem("token");
          this.$store.commit("SET_IS_AUTHENTICATED", false);
          this.$store.commit("SET_USER_ID", 0);
          this.$store.commit("SET_ORGANIZER", false);
          this.$store.commit("MODERATE_ORGANIZER", false);
          this.$store.commit("SET_STUDENT", false);
          this.$router.push({ path: "/" });
        })
        .catch((error) => {
          console.error(error);
        });

      this.$store.commit("STOP_LOADING");
      this.$router.push({ path: "/" });
    },
  },
};
</script>
