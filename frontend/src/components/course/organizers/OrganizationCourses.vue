<template>
  <div>
    <h1>Курсы организации</h1>
    <div>
      <input
        placeholder="Поиск по названию и описанию"
        name="search"
        id="search"
        :disabled="publishedCourses == undefined"
        type="text"
        v-model.trim="findString"
      />
      <multiselect
        :disabled="publishedCourses == undefined || subjects == undefined"
        v-model="findSubject"
        track-by="id"
        label="name"
        placeholder="Выберите школьные предметы"
        :options="subjectsOption"
        :showLabels="false"
        :searchable="true"
        :allow-empty="true"
        :showPointer="false"
        :multiple="true"
        :close-on-select="false"
        :clear-on-select="false"
      >
        <span slot="noResult">Не найдено</span>
      </multiselect>
    </div>
    <div>
      <p v-if="publishedCourses == undefined">Загрузка...</p>
      <div v-else>
        <div v-for="course in filterItems" :key="course.id">
          <course-element :course="course" :delete="false"> </course-element>
        </div>
        <p v-if="filterItems.length == 0">Не найдено</p>
      </div>
    </div>
  </div>
</template>

<script>
import { PUBLISHED_COURSES, SUBJECTS } from "@/graphql/queries/queries";
import CourseElement from "@/components/course/CourseElement.vue";
import Multiselect from "vue-multiselect";

export default {
  name: "OrganizationCourses",
  apollo: {
    publishedCourses: {
      query: PUBLISHED_COURSES,
    },
    subjects: {
      query: SUBJECTS,
    },
  },
  components: {
    CourseElement,
    Multiselect,
  },
  data() {
    return {
      findString: "",
      findSubject: [],
      organizationId: 2,
      userId: 2,
    };
  },
  computed: {
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },

    filterItems() {
      let courses;
      if (
        this.publishedCourses != null &&
        this.publishedCourses != undefined &&
        this.publishedCourses.length != 0
      ) {
        courses = this.publishedCourses;
        if (this.findString != "") {
          courses = courses.filter((el) => {
            return (
              (el.name
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.name != "") ||
              (el.description
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.description != "")
            );
          });
        }

        if (this.findSubject.length != 0) {
          courses = courses.filter((el) => {
            let flag = false;
            let i = 0;
            let j = 0;
            while (!flag && j < el.courseSubject.length) {
              if (el.courseSubject[j].subject.id == this.findSubject[i].id)
                flag = true;
              if (i + 1 == this.findSubject.length) {
                i = 0;
                j++;
              } else i++;
            }
            return flag;
          });
        }
      } else courses = [];
      return courses;
    },
  },

  methods: {},
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
