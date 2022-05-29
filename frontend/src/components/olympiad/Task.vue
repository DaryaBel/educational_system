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
  props: ["task", "oldAnswer"],
  computed: {
    taskId() {
      return this.task.id;
    },
  },
  methods: {
    getAnswer() {
      if (this.oldAnswer != undefined) {
        if (this.oldAnswer != undefined) {
          this.answer = this.oldAnswer.answer;
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
