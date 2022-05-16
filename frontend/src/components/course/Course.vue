<template>
  <div>
    <div v-if="course == undefined">
      <p>Загрузка...</p>
    </div>
    <div v-else>
      <h1>{{ course.name }}</h1>
      <p>
        <span v-for="subject in course.courseSubject" :key="subject.subject.id">
          {{ subject.subject.name }}
        </span>
      </p>
      <img src="https://picsum.photos/200" alt="" />
      <p>{{ course.description }}</p>
      <p>
        Организатор: {{ organizationType() }}
        {{ course.organization.shortname }}.
      </p>
      <p v-if="whatIsStudyingForm(course.form) != ''">
        Курс проводится {{ whatIsStudyingForm(course.form) }}.
      </p>
      <p v-if="whatIsDurationType(course.duration) != ''">
        Длительность: {{ whatIsDurationType(course.duration) }}.
      </p>
      <p
        v-if="
          formatDate(course.dateEnd) != null ||
          formatDate(course.dateStart) != null
        "
      >
        Курс проводится<span v-if="formatDate(course.dateStart) != null">
          c {{ formatDate(course.dateStart) }}</span
        >
        <span v-if="formatDate(course.dateEnd) != null">
          до {{ formatDate(course.dateEnd) }}</span
        >.
      </p>
      <div>
        <div
          v-if="
            countCourseMember == undefined || isStudentCourseMember == undefined
          "
        >
          <p>Загрузка...</p>
        </div>
        <div v-else>
          <div v-if="!isStudentCourseMember">
            <p
              v-if="
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
            >
              Записаться на курс
            </button>
          </div>
          <div v-if="isStudentCourseMember">
            <button @click="toCancelAppointment">
              Отменить запись на курс
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  CREATE_STUDENT_COURSE,
  DELETE_STUDENT_COURSE,
} from "@/graphql/mutations/mutations.js";
import {
  COURSE_FOR_STUDENT,
  IS_STUDENT_COURSE_MEMBER,
  NUMBER_MEMBER_COURSE,
} from "@/graphql/queries/queries.js";
export default {
  name: "Course",
  apollo: {
    course: {
      query: COURSE_FOR_STUDENT,
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
  data() {
    return {
      userId: 2,
      status: "",
      takePart: false,
    };
  },
  methods: {
    toTakePart() {
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
          // this.$toast.success("Вы успешно записались на курс!", {
          //   position: "bottom-right",
          //   duration: 5000,
          //   dismissible: false,
          //   pauseOnHover: false,
          // });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    toCancelAppointment() {
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
        })
        .catch((error) => {
          console.error(error);
        });
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

<style lang="scss"></style>
