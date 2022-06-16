<template>
  <div>
    <div class="d-flex justify-content-center">
      <div
        class="spinner-border text-primary"
        style="
          position: absolute;
          top: 50%;
          left: 50%;
          margin-top: -2.5rem;
          margin-left: -1.5rem;
          width: 3rem;
          height: 3rem;
        "
        role="status"
      >
        <span class="sr-only">Загрузка...</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Loader",
  methods: {},
};
</script>

<style lang="scss"></style>
