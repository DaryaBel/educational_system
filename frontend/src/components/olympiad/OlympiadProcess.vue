<template>
  <div>
    <loader
      v-if="
        isLoading ||
        olympiad == undefined ||
        answers == undefined ||
        result == undefined
      "
    >
    </loader>
    <div v-else>
      <div class="position-relative">
        <h1>{{ olympiad.name }}</h1>
        <div class="position-absolute my-task-counter">
          <p>
            Выполнено {{ answers.length }} из
            {{ olympiad.olympiadTask.length }}
          </p>
          <button
            v-for="task in sortedTasks"
            @click="chosenTaskOrder = task.order"
            :key="task.id"
            class="number mr-3 mb-3"
            :class="{
              'is-ready': isTaskReady(task.id),
            }"
          >
            {{ task.order }}
          </button>
          <br />
          <button
            class="text-gradient"
            style="font-size: 16px"
            @click="modal = true"
          >
            Отправить работу
            <span style="font-size: 16px" class="text">Отправить работу</span>
          </button>
        </div>
      </div>

      <div v-if="olympiad.olympiadTask != undefined">
        <task
          v-bind:task="chosenTaskObject"
          v-bind:oldAnswer="
            answers.find((el) => el.task.id == chosenTaskObject.id)
          "
          @answer="saveAnswer($event)"
        ></task>
        <div>
          <button
            class="text-gradient btn-sm mr-2"
            :disabled="chosenTaskOrder == 1"
            @click="chosenTaskOrder--"
          >
            Назад
            <span class="text">Назад</span></button
          ><button
            class="text-gradient btn-sm mr-2"
            :disabled="chosenTaskOrder == olympiad.olympiadTask.length"
            @click="chosenTaskOrder++"
          >
            Вперед
            <span class="text">Вперед</span>
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
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "OlympiadProcess",
  components: {
    Task,
    ModalOlympiad,
    Loader,
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

      chosenTaskOrder: 1,
    };
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
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
      this.$store.commit("START_LOADING");
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
      this.$store.commit("STOP_LOADING");
    },
    saveAnswer(event) {
      let neededAnswer = this.answers.find((el) => el.task.id == event.id);
      if (event.answer.trim() == "") {
        if (neededAnswer) {
          this.$store.commit("START_LOADING");
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
          this.$store.commit("STOP_LOADING");
        }
      } else {
        if (neededAnswer) {
          this.$store.commit("START_LOADING");
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
          this.$store.commit("STOP_LOADING");
        } else {
          this.$store.commit("START_LOADING");
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
          this.$store.commit("STOP_LOADING");
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
.my-task-counter {
  top: 120px;
  right: 0;
  padding: 20px 15px;
  width: 280px;
  min-height: 100px;
  border: 1px solid #ced4da;
  border-radius: 8px;
  & button.number {
    color: #004e93;
    padding: 5px 14px !important;
    background: #ffffff;
    border: 1px solid #dee2e6;

    border-radius: 4px;
    &.is-ready {
      color: white;
      background: linear-gradient(
        51.06deg,
        #9358f7 0.87%,
        #9259f7 7.31%,
        #8e5df6 13.75%,
        #8862f5 20.19%,
        #806bf4 26.63%,
        #7575f2 33.07%,
        #6882f0 39.51%,
        #5990ee 45.95%,
        #4a9feb 52.39%,
        #3bade9 58.84%,
        #2ebae7 65.28%,
        #23c4e5 71.72%,
        #1bcde4 78.16%,
        #15d2e3 84.6%,
        #11d6e2 91.04%,
        #10d7e2 97.48%
      );
    }
  }
}
</style>
