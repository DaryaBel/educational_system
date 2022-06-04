<template>
  <div>
    <div
      v-if="
        olympiad == undefined ||
        answers == undefined ||
        result == undefined
      "
    >
      <p>Загрузка...</p>
    </div>
    <div v-else>
      <h1>{{ olympiad.name }}</h1>
      <p>
        Выполнено {{ answers.length }} из
        {{ olympiad.olympiadTask.length }}
      </p>
      <div>
        <button
          v-for="task in sortedTasks"
          @click="chosenTaskOrder = task.order"
          :key="task.id"
          :class="{
            'is-ready': isTaskReady(task.id),
          }"
        >
          {{ task.order }}
        </button>
      </div>
      <button @click="modal = true">Отправить работу</button>
      <div v-if="olympiad.olympiadTask != undefined">
        <task
          v-bind:task="chosenTaskObject"
          v-bind:oldAnswer="
            answers.find((el) => el.task.id == chosenTaskObject.id)
          "
          @answer="saveAnswer($event)"
        ></task>
        <div>
          <button :disabled="chosenTaskOrder == 1" @click="chosenTaskOrder--">
            Назад</button
          ><button
            :disabled="chosenTaskOrder == olympiad.olympiadTask.length"
            @click="chosenTaskOrder++"
          >
            Вперед
          </button>
        </div>
      </div>
      <modal-olympiad
        v-if="modal"
        @finish="finishOlympiad"
        @close="modal = false"
      ></modal-olympiad>
    </div>
  </div>
</template>

<script>
import Task from "@/components/olympiad/Task.vue";
import ModalOlympiad from "@/components/olympiad/ModalOlympiad.vue";
import {
  UPDATE_ANSWER,
  CREATE_ANSWER,
  DELETE_ANSWER,
  UPDATE_RESULT,
} from "@/graphql/mutations/mutations";
import {
  OLYMPIAD_PROCESS,
  STUDENT_ANSWERS,
  OLYMPIAD_STATUS,
} from "@/graphql/queries/queries";
export default {
  name: "OlympiadProcess",
  components: {
    Task,
    ModalOlympiad,
  },
  apollo: {
    result: {
      query: OLYMPIAD_STATUS,
      variables() {
        return {
          userId: this.userId,
          olympiadId: this.$route.params.id,
        };
      },
    },
    olympiad: {
      query: OLYMPIAD_PROCESS,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
    answers: {
      query: STUDENT_ANSWERS,
      variables() {
        return {
          olympiadId: this.$route.params.id,
          userId: this.userId,
        };
      },
    },
  },
  data() {
    return {
      modal: false,
      userId: 2,
      chosenTaskOrder: 1,
    };
  },
  computed: {
    sortedTasks() {
      if (Array.isArray(this.olympiad.olympiadTask))
        return this.olympiad.olympiadTask.sort(this.sortByOrder);
      else return this.olympiad.olympiadTask;
    },
    chosenTaskObject() {
      return this.olympiad.olympiadTask.find(
        (element) => this.chosenTaskOrder == element.order
      );
    },
  },
  methods: {
    finishOlympiad() {
      this.$apollo
        .mutate({
          mutation: UPDATE_RESULT,
          variables: {
            resultId: this.result.id,
            status: "SENT",
          },
        })
        .then(() => {
          this.$apollo.queries.result.refresh();
          this.$apollo.queries.result.refetch();
          this.$router.push({ name: "StudentOlympiads" });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    saveAnswer(event) {
      let neededAnswer = this.answers.find((el) => el.task.id == event.id);
      if (event.answer.trim() == "") {
        if (neededAnswer) {
          this.$apollo
            .mutate({
              mutation: DELETE_ANSWER,
              variables: {
                answerId: neededAnswer.id,
              },
            })
            .then(() => {
              this.$apollo.queries.answers.refresh();
              this.$apollo.queries.answers.refetch();
            })
            .catch((error) => {
              console.error(error);
            });
        }
      } else {
        if (neededAnswer) {
          this.$apollo
            .mutate({
              mutation: UPDATE_ANSWER,
              variables: {
                answerId: neededAnswer.id,
                answer: event.answer,
              },
            })
            .then(() => {
              this.$apollo.queries.answers.refresh();
              this.$apollo.queries.answers.refetch();
            })
            .catch((error) => {
              console.error(error);
            });
        } else {
          this.$apollo
            .mutate({
              mutation: CREATE_ANSWER,
              variables: {
                taskId: event.id,
                userId: this.userId,
                olympiadId: this.$route.params.id,
                answer: event.answer,
              },
            })
            .then(() => {
              this.$apollo.queries.answers.refresh();
              this.$apollo.queries.answers.refetch();
            })
            .catch((error) => {
              console.error(error);
            });
        }
      }
    },
    isTaskReady(id) {
      if (this.answers.find((el) => el.task.id == id)) return true;
      else return false;
    },
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
    },
  },
};
</script>

<style lang="scss">
.is-ready {
  background-color: aquamarine;
}
</style>
