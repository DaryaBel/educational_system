<template>
  <div class="border-line">
    <p>
      <router-link
        tag="a"
        :to="{ name: 'Olympiad', params: { id: olympiad.id } }"
        >{{ olympiad.name }}</router-link
      >
    </p>
    <p>
      <span
        v-for="subject in olympiad.olympiadSubject"
        :key="subject.subject.id"
      >
        {{ subject.subject.name }}
      </span>
    </p>
    <p>{{ olympiad.description }}</p>
  </div>
</template>

<script>
export default {
  name: "OlympiadElement",
  props: ["olympiad"],
  data() {
    return {
      userId: 2,
    };
  },
  methods: {},
};
</script>

<style lang="scss">
.border-line {
  border: 1px solid seagreen;
}
</style>
