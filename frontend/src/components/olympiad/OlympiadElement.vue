<template>
  <div style="width: 100% !important">
    <img
      :src="'http://localhost:8000/media/' + olympiad.organization.logo"
      class="rounded img-fluid my-img mb-4"
      alt=""
    /><br />
    <router-link
      tag="a"
      class="text-decoration-none fs-2 mb-2"
      :to="{ name: 'Olympiad', params: { id: olympiad.id } }"
      >{{ olympiad.name }}</router-link
    >

    <p class="mb-3">
      <span
        class="badge my-badge badge-secondary mr-2"
        v-for="subject in olympiad.olympiadSubject"
        :key="subject.subject.id"
      >
        {{ subject.subject.name }}
      </span>
    </p>
    <p class="mb-1">{{ olympiad.description }}</p>
    <p v-if="status != '-'">Статус: {{ status }}</p>
  </div>
</template>

<script>
export default {
  name: "OlympiadElement",
  props: ["olympiad", "status"],
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss">
img.my-img {
  border: 1px solid #dee2e6;
  width: 100% !important;
}
span.my-badge {
  padding: 4px 8px;
  background: linear-gradient(132.33deg, #d24074 -0.67%, #6518b4 102.54%);
}
</style>
