<template>
  <div style="width: 100% !important">
    <img
      :src="'http://localhost:8000/media/' + course.organization.logo"
      class="rounded img-fluid my-img mb-4"
      alt=""
    /><br />

    <router-link
      tag="a"
      class="text-decoration-none fs-2 mb-2"
      :to="{ name: 'Course', params: { id: course.id } }"
      >{{ course.name }}</router-link
    >

    <p class="mb-3">
      <span
        class="badge my-badge badge-secondary mr-2"
        v-for="subject in course.courseSubject"
        :key="subject.subject.id"
      >
        {{ subject.subject.name }}
      </span>
    </p>
    <p class="mb-1">{{ course.description }}</p>
    <span
      v-if="canDelete"
      @click="toCancelAppointment"
      class="text-danger"
      style="cursor: pointer"
    >
      Отменить запись на курс
    </span>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";

import { DELETE_STUDENT_COURSE } from "@/graphql/mutations/mutations.js";
export default {
  name: "CourseElement",
  props: ["course", "canDelete"],
  data() {
    return {};
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
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
img.my-img {
  border: 1px solid #dee2e6;
  width: 100% !important;
}
span.my-badge {
  padding: 4px 8px;
  background: linear-gradient(132.33deg, #d24074 -0.67%, #6518b4 102.54%);
}
</style>
