<template lang="html">
  <div>
    <div class="container pt-3">
      <topbar></topbar>
      <div class="my-view">
        <router-view></router-view>
      </div>

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

.my-view {
  min-height: calc(100vh - 285px);
}
</style>
