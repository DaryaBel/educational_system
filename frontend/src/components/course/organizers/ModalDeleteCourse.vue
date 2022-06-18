<template>
  <div>
    <div class="position-fixed top-0 left-0 modal my-fade show d-block">
      <div class="modal-dialog modal-dialog-centered">
        <div class="modal-content">
          <div class="modal-header">
            <h3>Вы действительно хотите удалить курс "{{ courseName }}"?</h3>
          </div>
          <div class="modal-footer">
            <button class="gradient to-block mr-4" @click="$emit('close')">
              Нет
            </button>
            <button
              class="text-gradient to-block"
              @click="
                $emit('close');
                $emit('delete', courseId);
              "
            >
              Да
              <span class="text">Да</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  props: ["courseName", "courseId"],
  name: "ModalDeleteCourse",
  methods: {},
};
</script>
<style lang="scss" scoped>
.my-fade {
  background: rgba($color: #000000, $alpha: 0.5);
}
</style>
