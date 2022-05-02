<template>
  <div>
    <h1 v-if="!timeIsOver">Завершить выполнение заданий?</h1>
    <h1 v-if="timeIsOver">Время на выполнение заданий истекло</h1>

    <p v-if="!timeIsOver">
      После завершения нельзя будет вносить изменения в ответы
    </p>
    <p v-if="timeIsOver">Решения заданий были отправлены на проверку</p>

    <button v-if="!timeIsOver" @click="$emit('close')">Отменить</button>
    <button v-if="!timeIsOver" @click="finishOlympiad">Завершить</button>
    <button v-if="timeIsOver" @click="finishOlympiad">Закрыть</button>
  </div>
</template>

<script>
export default {
  name: "ModalOlympiad",
  props: ["timeIsOver"],
  methods: {
    finishOlympiad() {
      this.$emit("finish");
      this.$emit("close");
    },
  },
};
</script>

<style lang="scss"></style>
