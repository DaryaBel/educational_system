<template>
  <div>
    <h1>Задание {{ task.order }}</h1>
    <p>
      {{ task.task }}
    </p>
    <h3>Ответ</h3>
    <br />
    <form>
      <textarea
        v-model.trim="answer"
        @change="$emit('answer', { answer: answer, id: task.id })"
        placeholder="Текст ответа"
      ></textarea>
    </form>

    <br />
  </div>
</template>

<script>
export default {
  name: "Task",
  props: ["task"],
  computed: {
    taskId() {
      return this.task.id;
    },
  },
  methods: {
    getAnswer() {
      if (
        this.task.taskAnswer != undefined &&
        this.task.taskAnswer.length != 0
      ) {
        let userAnswer = this.task.taskAnswer.find(
          (el) => el.student.user.id == this.userId
        );
        if (userAnswer != undefined) {
          if (userAnswer.answer != undefined) {
            this.answer = userAnswer.answer;
          } else this.answer = "";
        } else this.answer = "";
      } else this.answer = "";
    },
  },
  watch: {
    taskId: {
      handler: "getAnswer",
      immediate: true,
    },
  },
  data() {
    return {
      userId: 1,
      answer: "",
    };
  },
};
</script>

<style lang="scss"></style>
