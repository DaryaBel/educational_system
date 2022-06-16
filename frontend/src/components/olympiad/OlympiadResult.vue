<template>
  <div>
    <loader
      v-if="
        isLoading ||
        result == undefined ||
        answers == undefined ||
        olympiad == undefined
      "
    >
    </loader>
    <div v-else>
      <h1>Результаты</h1>
      <p v-if="result.won">Победитель!</p>
      <p>
        Ваш результат составляет {{ result.score }}/{{ totalScore() }}, что
        составляет {{ getPercent(result.score) }}%.
      </p>
      <p v-if="!result.won">
        К сожалению, вы не набрали необходмое количество баллов для победы. Не
        расстраивайтесь и принимайте участие в других олимпиадах нашей
        организации!
      </p>

      <div v-for="task in sortedTasks" :key="task.id">
        <h4>Задание {{ task.order }}.</h4>
        <p>{{ task.task }}</p>
        <p v-if="findAnswer(task.id) != undefined">
          Баллы: {{ findAnswer(task.id).score }}/{{ task.maxScore }}.
        </p>
        <p v-else>Баллы: 0/{{ task.maxScore }}.</p>
        <p>Ответ:</p>
        <p v-if="findAnswer(task.id) != undefined">
          {{ findAnswer(task.id).answer }}
        </p>
        <p v-else>Данное задание не было решено.</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  RESULT_WITH_ANSWERS,
  STUDENT_ANSWERS_WITH_TASK,
  OLYMPIAD_TASK_CHECK,
} from "@/graphql/queries/queries";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  components: { Loader },
  name: "OlympiadResult",
  apollo: {
    result: {
      query: RESULT_WITH_ANSWERS,
      variables() {
        return {
          userId: this.userId,
          olympiadId: this.$route.params.id,
        };
      },
    },
    answers: {
      query: STUDENT_ANSWERS_WITH_TASK,
      variables() {
        return {
          userId: this.userId,
          olympiadId: this.$route.params.id,
        };
      },
    },
    olympiad: {
      query: OLYMPIAD_TASK_CHECK,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
  },
  data() {
    return {};
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    sortedTasks() {
      return this.olympiad.olympiadTask.sort(this.sortByOrder);
    },
  },
  methods: {
    getPercent(result) {
      if (result == undefined) return 0;
      else {
        let x;
        x = result * 100;
        x = x / this.totalScore();
        return x.toFixed(2);
      }
    },
    totalScore() {
      let sum = 0;
      this.olympiad.olympiadTask.forEach((el) => (sum += +el.maxScore));
      return sum;
    },

    findAnswer(id) {
      return this.answers.find((el) => el.task.id == id);
    },
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
    },
  },
};
</script>
<style lang="scss"></style>
