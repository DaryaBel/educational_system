<template lang="html">
  <div>
    <div class="container py-3">
      <topbar></topbar>
      <router-view></router-view>

      <bottombar></bottombar>
    </div>
  </div>
</template>

<script>
import Topbar from "@/components/parts/Topbar.vue";
import Bottombar from "@/components/parts/Footer.vue";

export default {
  name: "App",
  components: {
    Topbar,
    Bottombar,
  },
};
</script>

<style lang="scss">
@import "@/scss/app.scss";
</style>
