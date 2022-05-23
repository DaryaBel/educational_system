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
    <button v-if="canDelete" @click="toCancelAppointment">
      Отменить запись на курс
    </button>
  </div>
</template>

<script>
import { DELETE_STUDENT_COURSE } from "@/graphql/mutations/mutations.js";
export default {
  name: "CourseElement",
  props: ["course", "canDelete"],
  data() {
    return {
      userId: 2,
    };
  },
  methods: {
    toCancelAppointment() {
      this.$apollo
        .mutate({
          mutation: DELETE_STUDENT_COURSE,
          variables: {
            courseId: this.course.id,
            userId: this.userId,
          },
        })
        .then(() => {
          this.$emit("cancel");
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>

<style lang="scss">
.border-line {
  border: 1px solid seagreen;
}
</style>
