<template>
  <div>
    <div v-if="olympiad == undefined">
      <p>Загрузка...</p>
    </div>
    <div v-else>
      <h1>{{ olympiad.name }}</h1>
      <p>
        Данная олимпиада состоит из {{ olympiad.olympiadTask.length }}
        {{ formOfWord(olympiad.olympiadTask.length, 1) }} с развернутым ответом.
        Ответ можно написать в текстовом поле или приложить в данное поле ссылку
        (например, на гугл-диск). Перед отправкой, проверьте, что ваш документ
        доступен для чтения по ссылке.
      </p>

      <button @click="toStart()">Начать</button>
    </div>
  </div>
</template>

<script>
import { UPDATE_RESULT } from "@/graphql/mutations/mutations";
import { OLYMPIAD_RULES, OLYMPIAD_STATUS } from "@/graphql/queries/queries.js";

export default {
  name: "OlympiadRules",
  apollo: {
    olympiad: {
      query: OLYMPIAD_RULES,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
    studentOlympiadResult: {
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
    resultId() {
      if (this.studentOlympiadResult == undefined) return 0;
      else return this.studentOlympiadResult.id;
    },
  },
  data() {
    return {
      userId: 2,
    };
  },
  methods: {
    toStart() {
      this.$apollo
        .mutate({
          mutation: UPDATE_RESULT,
          variables: {
            resultId: this.resultId,
            status: "BEGIN",
          },
        })
        .then(() => {
          this.$apollo.queries.studentOlympiadResult.refresh();
          this.$apollo.queries.studentOlympiadResult.refetch();
          this.$router.push({
            name: "OlympiadProcess",
            params: { id: this.$route.params.id },
          });
        })
        .catch((error) => {
          console.error(error);
        });
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
