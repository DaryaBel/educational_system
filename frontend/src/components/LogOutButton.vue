<template>
  <div>
    <button @click="logOut">Выйти</button>
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
          clearInterval(logOutInterval);
          this.$store.commit("SET_IS_AUTHENTICATED", false);
          this.$router.push(AUTH_PATH);
          this.$store.commit("STOP_LOADING");
        })
        .catch(() => {});
    },
  },
};
</script>

<style lang="scss" scoped></style>
