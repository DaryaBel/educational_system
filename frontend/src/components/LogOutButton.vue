<template>
  <div>
    <button class="text-gradient" @click="logOut">
      Выйти
      <span class="text">Выйти</span>
    </button>
    <button class="gradient" @click="logOut">Выйти</button>
  </div>
</template>

<script>
import logout from "@/graphql/mutations/logout.gql";
export default {
  name: "LogOutButton",
  methods: {
    logOut() {
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({ mutation: logout })
        .then(() => {
          localStorage.removeItem("token");
          this.$store.commit("SET_IS_AUTHENTICATED", false);
          this.$store.commit("SET_USER_ID", 0);
          this.$store.commit("SET_ORGANIZER", false);
          this.$store.commit("MODERATE_ORGANIZER", false);
          this.$store.commit("SET_STUDENT", false);
          this.$router.push("LogIn");
          this.$store.commit("STOP_LOADING");
        })
        .catch(() => {});
    },
  },
};
</script>

<style lang="scss" scoped></style>
