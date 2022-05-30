<template>
  <div>
    <h1>Вы действительно хотите удалить олимпиаду "{{ olympiadName }}"?</h1>
    <button @click="$emit('close')">Нет</button>
    <button
      @click="
        $emit('close');
        $emit('delete', olympiadId);
      "
    >
      Да
    </button>
  </div>
</template>
<script>
export default {
  props: ["olympiadName", "olympiadId"],
  name: "ModalDeleteOlympiad",
  methods: {},
};
</script>
