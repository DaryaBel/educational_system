<template>
  <div>
    <h1>Завершить выполнение заданий?</h1>
    <p>После завершения нельзя будет вносить изменения в ответы</p>
    <button @click="$emit('close')">Отменить</button>
    <button @click="finishOlympiad">Завершить</button>
  </div>
</template>

<script>
export default {
  name: "ModalOlympiad",
  methods: {
    finishOlympiad() {
      this.$emit("finish");
      this.$emit("close");
    },
  },
};
</script>

<style lang="scss"></style>
