<template>
  <div>
    <loader v-if="isLoading"></loader>
    <div v-else>
      <h2>Вы действительно хотите удалить аккаунт?</h2>
      <br />
      <button class="gradient to-block mr-4" @click="backToProfile()">
        Нет
      </button>
      <button class="text-gradient to-block" @click="deleteAccount()">
        Да
        <span class="text">Да</span>
      </button>
    </div>
  </div>
</template>
<script>
import jwt from "jsonwebtoken";
import { DELETE_USER } from "@/graphql/mutations/mutations";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "DeleteAccount",
  components: { Loader },
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
