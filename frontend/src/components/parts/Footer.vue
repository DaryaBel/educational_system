<template>
  <nav
    class="my-back border-top pt-4 px-5 navbar fixed-bottom navbar-expand-sm d-flex flex-column align-items-center justify-content-center"
    style="position: relative"
  >
    <p class="fs-3 text-center">
      Интернет портал для подбора образовательных курсов и проведения онлайн
      олимпиад для школьников старших классов “Пора”
    </p>
    <a href="/admin" class="text-decoration-none">Административная панель</a>
    <p class="text-center">2022. Все права защищены.</p>
  </nav>
</template>

<script>
export default {
  name: "Footer",
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped>
.my-back {
  background: white;
}
</style>
