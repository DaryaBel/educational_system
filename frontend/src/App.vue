<template lang="html">
  <div>
    <div class="container py-3">
      <topbar></topbar>
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import Topbar from "@/components/parts/Topbar.vue";

export default {
  name: "App",
  components: {
    Topbar,
  },
};
</script>

<style lang="scss">
@import "@/scss/app.scss";
</style>
