<template>
  <div>
    <loader v-if="isLoading || course == undefined"> </loader>
    <div v-else>
      <h1>{{ course.name }}</h1>
      <img
        class="rounded img-fluid mb-4"
        :src="'http://localhost:8000/media/' + course.organization.logo"
        alt=""
        style="max-width: 400px; border: 1px solid #dee2e6"
      />
      <p>
        <span
          class="badge my-badge badge-secondary mr-2"
          v-for="subject in course.courseSubject"
          :key="subject.subject.id"
        >
          {{ subject.subject.name }}
        </span>
      </p>
      <p>{{ course.description }}</p>

      <p>
        Организатор: {{ organizationType() }}
        {{ course.organization.shortname }}.
      </p>

      <p v-if="whatIsStudyingForm(course.form) != ''">
        Курс проводится {{ whatIsStudyingForm(course.form) }}.
      </p>

      <p
        v-if="
          whatIsDurationType(course.duration) != '' &&
          whatIsDurationType(course.duration) != undefined
        "
      >
        Длительность: {{ whatIsDurationType(course.duration) }}.
      </p>

      <p
        v-if="
          formatDate(course.dateEnd) != null ||
          formatDate(course.dateStart) != null ||
          course.city != undefined
        "
      >
        Курс проводится<span v-if="formatDate(course.dateStart) != null">
          c {{ formatDate(course.dateStart) }}</span
        >
        <span v-if="formatDate(course.dateEnd) != null">
          до {{ formatDate(course.dateEnd) }}</span
        >
        <span
          v-if="
            course.city != undefined &&
            course.city.name != undefined &&
            course.city.name != ''
          "
        >
          в городе {{ course.city.name }}</span
        >.
      </p>
      <div v-if="isStudent">
        <div v-if="countCourseMember == undefined">
          <loader></loader>
        </div>
        <div v-else>
          <div v-if="!isStudentCourseMember">
            <p
              v-if="
                course.maxNumberMember != undefined &&
                course.maxNumberMember - countCourseMember < 10 &&
                course.maxNumberMember - countCourseMember > 0
              "
            >
              Осталось {{ course.maxNumberMember - countCourseMember }}
              <span
                v-if="(course.maxNumberMember - countCourseMember) % 10 >= 5"
                >свободных мест</span
              >
              <span
                v-if="(course.maxNumberMember - countCourseMember) % 10 >= 2"
                >свободных места</span
              >
              <span
                v-if="(course.maxNumberMember - countCourseMember) % 10 == 1"
                >свободное место</span
              >.
            </p>
            <p v-if="course.maxNumberMember - countCourseMember == 0">
              К сожалению, мест не осталось.
            </p>

            <button
              v-if="course.maxNumberMember - countCourseMember != 0"
              @click="toTakePart"
              class="text-gradient to-block"
            >
              Записаться на курс
              <span class="text">Записаться на курс</span>
            </button>
          </div>
          <div v-if="isStudentCourseMember">
            <button @click="toCancelAppointment" class="text-gradient to-block">
              Отменить запись на курс
              <span class="text">Отменить запись на курс</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Loader from "@/components/parts/Loader.vue";

import jwt from "jsonwebtoken";
import {
  CREATE_STUDENT_COURSE,
  DELETE_STUDENT_COURSE,
} from "@/graphql/mutations/mutations.js";
import {
  COURSE,
  IS_STUDENT_COURSE_MEMBER,
  NUMBER_MEMBER_COURSE,
} from "@/graphql/queries/queries.js";
export default {
  name: "Course",
  apollo: {
    course: {
      query: COURSE,
      variables() {
        return {
          courseId: this.$route.params.id,
        };
      },
    },
    countCourseMember: {
      query: NUMBER_MEMBER_COURSE,
      variables() {
        return {
          courseId: this.$route.params.id,
        };
      },
    },
    isStudentCourseMember: {
      query: IS_STUDENT_COURSE_MEMBER,
      variables() {
        return {
          userId: this.userId,
          courseId: this.$route.params.id,
        };
      },
    },
  },
  components: { Loader },
  data() {
    return {};
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    isStudent() {
      return this.$store.state.isStudent;
    },
  },
  methods: {
    toTakePart() {
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({
          mutation: CREATE_STUDENT_COURSE,
          variables: {
            courseId: this.$route.params.id,
            userId: this.userId,
          },
        })
        .then(() => {
          this.$apollo.queries.isStudentCourseMember.refresh();
          this.$apollo.queries.isStudentCourseMember.refetch();
          this.makeToast(true);
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    makeToast(flag) {
      let text = "Вы успешно записались на курс!";
      if (!flag) text = "Запись на курс успешно отменена";
      this.$bvToast.toast(text, {
        title: "",
        autoHideDelay: 5000,
        appendToast: true,
      });
    },
    toCancelAppointment() {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: DELETE_STUDENT_COURSE,
          variables: {
            courseId: this.$route.params.id,
            userId: this.userId,
          },
        })
        .then(() => {
          this.$apollo.queries.isStudentCourseMember.refresh();
          this.$apollo.queries.isStudentCourseMember.refetch();
          this.$apollo.queries.countCourseMember.refresh();
          this.$apollo.queries.countCourseMember.refetch();
          this.makeToast(false);
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    whatIsStudyingForm(studyingForm) {
      if (studyingForm == "ON") return "онлайн";
      if (studyingForm == "OFF") return "оффлайн";
      if (studyingForm == "BOTH") return "в смешанном формате";
      return "";
    },
    whatIsDurationType(duration) {
      if (duration == "LESSMONTH") return "меньше месяца";
      if (duration == "MONTH") return "1-2 месяца";
      if (duration == "FEWMONTH") return "от двух месяцев до полугода";
      if (duration == "HALFYEAR") return "от полугода до года";
      if (duration == "YEARANDMORE") return "год и более";
      return "";
    },
    organizationType() {
      if (this.course.organization.kind == "UNIVERSITY")
        return "образовательная организация";
      if (this.course.organization.kind == "COMPANY") return "компания";
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
  },
};
</script>

<style lang="scss">
span.my-badge {
  padding: 4px 8px;
  background: linear-gradient(132.33deg, #d24074 -0.67%, #6518b4 102.54%);
}
</style>
