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
      <p v-if="olympiad.timeToPass != null && olympiad.timeToPass != 0">
        На решение заданий даётся {{ formatTime(olympiad.timeToPass) }}. Если
        работа не будет отправлена по истечению данного времени, она отправится
        автоматически.
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
      hours: "",
      minutes: "",
      seconds: "",
    };
  },
  methods: {
    toStart() {
      let start = new Date();
      let delta = Math.trunc(this.olympiad.timeToPass);
      let finish = new Date(start.setMilliseconds(delta * 1000));
      this.$apollo
        .mutate({
          mutation: UPDATE_RESULT,
          variables: {
            resultId: this.resultId,
            startTryTime: Math.trunc(start.getTime() / 1000),
            finishTryTime: Math.trunc(finish.getTime() / 1000),
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
    formatTime(time) {
      if (!time) return null;
      time = Math.trunc(time);
      this.seconds = time % 60;
      time = (time - this.seconds) / 60;
      this.minutes = time % 60;
      this.hours = (time - this.minutes) / 60;
      let result;
      result = "";
      if (this.hours != 0) {
        result = result + ` ${this.hours} ${this.formOfWord(this.hours, 2)}`;
      }
      if (this.minutes != 0) {
        result =
          result + ` ${this.minutes} ${this.formOfWord(this.minutes, 3)}`;
      }
      if (this.seconds != 0) {
        result =
          result + ` ${this.seconds} ${this.formOfWord(this.seconds, 4)}`;
      }
      return result;
    },
    formOfWord(length, word) {
      // задания
      if (word == 1) {
        if (length == 1) return "задания";
        else return "заданий";
      }
      // часы
      if (word == 2) {
        if (
          length % 10 >= 2 &&
          length % 10 <= 4 &&
          length % 100 != 12 &&
          length % 100 != 13 &&
          length % 100 != 14
        )
          return "часа";
        else {
          if (
            (length % 10 >= 5 && length % 10 <= 9) ||
            (length % 100 >= 10 && length % 100 <= 20) ||
            length % 10 == 0
          )
            return "часов";
          else return "час";
        }
      }
      // минуты
      if (word == 3) {
        if (
          length % 10 >= 2 &&
          length % 10 <= 4 &&
          length % 100 != 12 &&
          length % 100 != 13 &&
          length % 100 != 14
        )
          return "минуты";
        else {
          if (
            (length % 10 >= 5 && length % 10 <= 9) ||
            (length % 100 >= 10 && length % 100 <= 20) ||
            length % 10 == 0
          )
            return "минут";
          else return "минута";
        }
      }
      // секунды
      if (word == 4) {
        if (
          length % 10 >= 2 &&
          length % 10 <= 4 &&
          length % 100 != 12 &&
          length % 100 != 13 &&
          length % 100 != 14
        )
          return "секунды";
        else {
          if (
            (length % 10 >= 5 && length % 10 <= 9) ||
            (length % 100 >= 10 && length % 100 <= 20) ||
            length % 10 == 0
          )
            return "секунд";
          else return "секунда";
        }
      }
    },
  },
};
</script>

<style lang="scss"></style>
