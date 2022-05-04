<template>
  <div>
    <h1>{{ olympiad.name }}</h1>
    <p>{{ countdown }}</p>
    <p>
      Выполнено {{ sumReadyTask(olympiad.olympiadTask) }} из
      {{ olympiad.olympiadTask.length }}
    </p>
    <div>
      <button
        v-for="task in sortedTasks"
        @click="chosenTaskOrder = task.order"
        :key="task.id"
        :class="{
          'is-ready':
            task.taskAnswer != undefined && task.taskAnswer.find(isTaskReady),
        }"
      >
        {{ task.order }}
      </button>
    </div>
    <button @click="modal = true">Отправить работу</button>
    <div v-if="olympiad.olympiadTask != undefined">
      <task v-bind:task="chosenTaskObject" @answer="saveAnswer($event)"></task>
      <div>
        <button :disabled="chosenTaskOrder == 1" @click="chosenTaskOrder--">
          Left</button
        ><button
          :disabled="chosenTaskOrder == olympiad.olympiadTask.length"
          @click="chosenTaskOrder++"
        >
          Right
        </button>
      </div>
    </div>
    <modal-olympiad
      v-if="modal"
      @finish="finishOlympiad"
      @close="modal = false"
      v-bind:timeIsOver="countdown != '00:00:00'"
    ></modal-olympiad>
  </div>
</template>

<script>
import Task from "@/components/olympiad/Task.vue";
import ModalOlympiad from "@/components/olympiad/ModalOlympiad.vue";
export default {
  name: "OlympiadProcess",
  components: {
    Task,
    ModalOlympiad,
  },
  data() {
    return {
      wasSent: false,
      modal: true,
      userId: 2,
      chosenTaskOrder: 1,
      olympiad: {
        name: 'Олимпиада "Инновационный полет"',
        time_to_pass: "8147.0",
        olympiadTask: [
          {
            id: 1,
            task: "Опишите мировую экономику",
            order: 2,
            taskAnswer: [
              {
                answer: "",
                student: {
                  user: {
                    id: 2,
                  },
                },
              },
              {
                answer: "kjhkhhkj",
                student: {
                  user: {
                    id: 1,
                  },
                },
              },
            ],
          },
          { id: 2, task: "Посчитайте 2+2", order: 1 },
          { id: 3, task: "Посчитайте 55+25", order: 3 },
        ],
      },
    };
  },
  computed: {
    countdown() {
      let finish = new Date(1651355884000);
      let now = new Date();
      let delta = new Date(finish - now);
      if (now.getMilliseconds() < finish.getMilliseconds())
        return delta.toISOString().slice(0, -5).slice(11, 19);
      else return "00:00:00";
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
      if (!this.wasSent) {
        // отправить решение
        // поставить статус как отправлено
      }
      this.$router.push({ name: "StudentOlympiads" });
    },
    saveAnswer(event) {
      console.log(event);
    },
    sumReadyTask(tasks) {
      let sum = 0;
      tasks.forEach((task) => {
        if (
          task.taskAnswer != undefined &&
          task.taskAnswer.find(this.isTaskReady) != undefined
        )
          sum++;
      });
      return sum;
    },
    isTaskReady(element, index, array) {
      if (element.student.user.id == this.userId && element.answer.trim() != "")
        return true;
      else return false;
    },
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
    },
    formatTime(time) {
      if (!time) return null;
      time = Math.trunc(time);
      let seconds;
      let minutes;
      let hours;
      seconds = time % 60;
      time = (time - seconds) / 60;
      minutes = time % 60;
      hours = (time - minutes) / 60;
      let result;
      result = "";
      if (hours != 0) {
        result = result + ` ${hours} ${this.formOfWord(hours, 2)}`;
      }
      if (minutes != 0) {
        result = result + ` ${minutes} ${this.formOfWord(minutes, 3)}`;
      }
      if (seconds != 0) {
        result = result + ` ${seconds} ${this.formOfWord(seconds, 4)}`;
      }
      return result;
    },
    formOfWord(length, word) {
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

<style lang="scss">
.is-ready {
  background-color: aquamarine;
}
</style>
