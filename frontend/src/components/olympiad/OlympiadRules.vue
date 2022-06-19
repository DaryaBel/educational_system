<template>
  <div>
    <loader v-if="isLoading || olympiad == undefined"> </loader>
    <div v-else>
      <h1>{{ olympiad.name }}</h1>
      <p>
        Данная олимпиада состоит из {{ olympiad.olympiadTask.length }}
        {{ formOfWord(olympiad.olympiadTask.length, 1) }} с развернутым ответом.
        Ответ можно написать в текстовом поле или приложить в данное поле ссылку
        (например, на гугл-диск). Перед отправкой, проверьте, что ваш документ
        доступен для чтения по ссылке.
      </p>

      <button @click="toStart()" class="mt-2 text-gradient to-block">
        Начать
        <span class="text">Начать</span>
      </button>
    </div>
  </div>
</template>

<script>
import { UPDATE_RESULT } from "@/graphql/mutations/mutations";
import { OLYMPIAD_RULES, OLYMPIAD_STATUS } from "@/graphql/queries/queries.js";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "OlympiadRules",
  components: { Loader },
  apollo: {
    olympiad: {
      query: OLYMPIAD_RULES,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
    result: {
      query: OLYMPIAD_STATUS,
      variables() {
        return {
          userId: this.userId,
          olympiadId: this.$route.params.id,
        };
      },
    },
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    resultId() {
      if (this.result == undefined) return 0;
      else return this.result.id;
    },
  },
  data() {
    return {};
  },
  methods: {
    toStart() {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: UPDATE_RESULT,
          variables: {
            resultId: this.resultId,
            status: "BEGIN",
          },
        })
        .then(() => {
          this.$apollo.queries.result.refresh();
          this.$apollo.queries.result.refetch();
          this.$router.push({
            name: "OlympiadProcess",
            params: { id: this.$route.params.id },
          });
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },

    formOfWord(length, word) {
      // задания
      if (word == 1) {
        if (length == 1) return "задания";
        else return "заданий";
      }
    },
  },
};
</script>

<style lang="scss"></style>
