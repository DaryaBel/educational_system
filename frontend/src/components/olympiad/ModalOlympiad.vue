<template>
  <div>
    <div class="position-fixed top-0 left-0 modal my-fade show d-block">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Завершить выполнение заданий?</h3>
          </div>
          <div class="modal-body">
            <p>После завершения нельзя будет вносить изменения в ответы</p>
          </div>
          <div class="modal-footer">
            <button class="gradient to-block mr-4" @click="$emit('close')">
              Отменить
            </button>
            <button class="text-gradient to-block" @click="finishOlympiad">
              Завершить
              <span class="text">Завершить</span>
            </button>
          </div>
        </div>
      </div>
    </div>
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

<style lang="scss">
.my-fade {
  background: rgba($color: #000000, $alpha: 0.5);
}
</style>
