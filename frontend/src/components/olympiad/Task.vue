<template>
  <div>
    <p class="fs-2 font-weight-normal">{{ task.order }} задание</p>
    <p>
      {{ task.task }}
    </p>
    <br />
    <form>
      <textarea
        class="form-control"
        style="width: 65%"
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
      answer: "",
    };
  },
};
</script>

<style lang="scss"></style>
