<template>
  <div>
    <h1>Вы действительно хотите опубликовать результаты олимпиады?</h1>
    <button @click="$emit('close')">Нет</button>
    <button
      @click="
        $emit('close');
        $emit('publish');
      "
    >
      Да
    </button>
  </div>
</template>
<script>
export default {
  name: "ModalPublishResult",
  methods: {},
};
</script>
