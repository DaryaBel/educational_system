<template lang="html">
  <div>
    <div class="container pt-3">
      <topbar></topbar>
      <div class="my-view">
        <router-view></router-view>
      </div>
      <div style="height: 100px; width: 100px"></div>

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

@font-face {
  font-family: "Inter", sans-serif;
  src: local("Inter"),
    url(./assets/fonts/Inter/Inter-Light.ttf) format("truetype");
  font-weight: 300;
}

@font-face {
  font-family: "Inter", sans-serif;
  src: local("Inter"),
    url(./assets/fonts/Inter/Inter-Regular.ttf) format("truetype");
  font-weight: normal;
}

@font-face {
  font-family: "Raleway", sans-serif;
  src: local("Raleway"),
    url(./assets/fonts/Raleway/Raleway-Bold.ttf) format("truetype");
  font-weight: bold;
}

* {
  font-family: "Inter", sans-serif;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  font-family: "Raleway", sans-serif;
}
.my-view {
  min-height: calc(100vh - 285px);
}
</style>
