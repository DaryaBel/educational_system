<template>
  <div>
    <p
      v-if="
        isLoading ||
        result == undefined ||
        answers == undefined ||
        olympiad == undefined
      "
    >
      Загрузка...
    </p>
    <div v-else>
      <div>
        <h1>Решение</h1>
        <p>
          {{ result.student.user.lastName }}
          {{ result.student.user.firstName }}
          {{ result.student.patronymic }}
        </p>
        <p v-if="result.score == undefined">
          Необходимое количество процентов для победы:
          {{ olympiad.percentToWin }}%.
        </p>
        <p v-if="result.score != undefined">
          Результат участника - {{ result.score }}/{{ totalScore() }}, что
          составляет {{ getPercent(result.score) }}%.
          <span v-if="result.won">Победитель!</span>
          <span v-else>Баллов для победы недостаточно.</span>
        </p>
        <div v-for="task in sortedTasks" :key="task.id">
          <h4>Задание {{ task.order }}.</h4>
          <p>{{ task.task }}</p>
          <p>Максиальный балл: {{ task.maxScore }}</p>
          <div v-if="findAnswer(task.id) != undefined">
            <p>Ответ:</p>
            <p>
              {{ findAnswer(task.id).answer }}
            </p>
            <p v-if="findAnswer(task.id).score != undefined">
              Баллы: {{ findAnswer(task.id).score }}/{{ task.maxScore }}.
            </p>
            <div v-else>
              <label for="score">Количество баллов:</label><br />

              <input
                name="score"
                id="score"
                type="number"
                min="1"
                step="1"
                :max="task.maxScore"
                v-model.trim="task.score"
                @change="getScore(findAnswer(task.id).id, task.score)"
                :class="{
                  'is-invalid':
                    submittedForm && !isScoreValid(findAnswer(task.id)),
                }"
              />
              <div
                v-if="submittedForm && !isScoreValid(findAnswer(task.id))"
                class="invalid-feedback"
              >
                <span
                  >Оцените решение баллами в диапазоне от 1 до
                  {{ task.maxScore }}!</span
                >
              </div>
            </div>
          </div>

          <div v-else>
            <p>Данное задание не было решено.</p>
            <p>Баллы: 0/{{ task.maxScore }}.</p>
          </div>
        </div>

        <div v-if="result.score == undefined">
          <p v-if="areScoresValid">
            Итого: {{ totalLocalScore() }} б., что составляет
            {{ getPercent(totalLocalScore()) }}%.
            <span
              v-if="getPercent(totalLocalScore()) - olympiad.percentToWin >= 0"
              >Участник победил.</span
            >
          </p>
          <button @click="saveScore()">Сохранить</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  UPDATE_RESULT_WITH_SCORES,
  SAVE_SCORE_FOR_ANSWER,
} from "@/graphql/mutations/mutations";
import {
  RESULT_WITH_ANSWERS,
  STUDENT_ANSWERS_WITH_TASK,
  OLYMPIAD_TASK_CHECK,
} from "@/graphql/queries/queries";

export default {
  name: "StudentAnswers",
  apollo: {
    result: {
      query: RESULT_WITH_ANSWERS,
      variables() {
        return {
          userId: this.$route.params.user,
          olympiadId: this.$route.params.id,
        };
      },
    },
    answers: {
      query: STUDENT_ANSWERS_WITH_TASK,
      variables() {
        return {
          userId: this.$route.params.user,
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
    return {
      points: [],
      userId: 2,
      organizationId: 4,
      submittedForm: false,
      isLoading: false,
    };
  },
  computed: {
    areScoresValid() {
      if (this.answers.length == this.points.length) {
        let flag = false;
        this.answers.forEach((el) => {
          if (!this.isScoreValid(el)) flag = true;
        });
        return !flag;
      } else {
        return false;
      }
    },
    sortedTasks() {
      return this.olympiad.olympiadTask.sort(this.sortByOrder);
    },
  },
  methods: {
    isScoreValid(answer) {
      let index = this.points.findIndex((item) => item.id == answer.id);
      if (index == -1) return false;
      else {
        if (
          this.points[index].score == undefined ||
          !Number.isInteger(+this.points[index].score) ||
          this.points[index].score <= 0 ||
          this.points[index].score > answer.task.maxScore
        ) {
          return false;
        } else {
          return true;
        }
      }
    },
    getScore(answerId, score) {
      let index = this.points.findIndex((el) => el.id == answerId);
      if (index == -1) {
        let obj = {
          id: answerId,
          score: score,
        };
        this.points.push(obj);
      } else this.points[index].score = score;
    },
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
    totalLocalScore() {
      let sum = 0;
      this.points.forEach((el) => {
        sum += +el.score;
      });
      return sum;
    },
    findAnswer(id) {
      return this.answers.find((el) => el.task.id == id);
    },
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
    },
    saveScore() {
      this.isLoading = true;
      this.submittedForm = true;
      if (!this.areScoresValid) {
        console.log("error");
        this.isLoading = false;
        return;
      }
      let won =
        this.getPercent(this.totalLocalScore()) - this.olympiad.percentToWin >=
        0;
      this.$apollo
        .mutate({
          mutation: UPDATE_RESULT_WITH_SCORES,
          variables: {
            resultId: this.result.id,
            status: "CHECKED",
            won: won,
            score: this.totalLocalScore(),
          },
        })
        .then(() => {
          this.points.forEach((el) => {
            this.$apollo
              .mutate({
                mutation: SAVE_SCORE_FOR_ANSWER,
                variables: {
                  answerId: el.id,
                  score: el.score,
                },
              })
              .then(() => {
                this.$apollo.queries.answers.refresh();
                this.$apollo.queries.answers.refetch();
                this.$apollo.queries.result.refresh();
                this.$apollo.queries.result.refetch();
                this.submittedForm = false;
                this.isLoading = false;
              })
              .catch((error) => {
                console.error(error);
              });
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
<style lang="scss"></style>
