<template>
  <div class="border-line">
    <p>
      <router-link
        tag="a"
        :to="{ name: 'Course', params: { id: course.id } }"
        >{{ course.name }}</router-link
      >
    </p>
    <p>
      <span v-for="subject in course.courseSubject" :key="subject.subject.id">
        {{ subject.subject.name }}
      </span>
    </p>
    <p>{{ course.description }}</p>
  </div>
</template>

<script>
export default {
  name: "CourseList",
  props: ["course"],
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
