<template>
  <div>
    <h1>Вы действительно хотите удалить курс "{{ courseName }}"?</h1>
    <button @click="$emit('close')">Нет</button>
    <button
      @click="
        $emit('close');
        $emit('delete', courseId);
      "
    >
      Да
    </button>
  </div>
</template>
<script>
export default {
  props: ["courseName", "courseId"],
  name: "ModalDeleteCourse",
  methods: {},
};
</script>
