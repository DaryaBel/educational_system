<template>
  <div>
    <loader v-if="isLoading || publishedCourses == undefined"></loader>
    <div v-else>
      <h1>Образовательные курсы</h1>
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

        <multiselect
          :disabled="publishedCourses == undefined"
          v-model="findFormat"
          track-by="value"
          label="text"
          placeholder="Выберите формат проведения"
          :options="formats"
          :showLabels="false"
          :searchable="false"
          :allow-empty="true"
          :showPointer="false"
          :multiple="true"
          :close-on-select="false"
        >
          <span slot="noResult">Не найдено</span>
        </multiselect>

        <multiselect
          :disabled="
            publishedCourses == undefined || organizations == undefined
          "
          v-model="findOrganization"
          track-by="id"
          label="fullname"
          placeholder="Выберите организатора"
          :options="organizationsOption"
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
        <multiselect
          :disabled="
            publishedCourses == undefined ||
            cities == undefined ||
            !offlineFormat()
          "
          v-model="findCities"
          track-by="id"
          label="name"
          placeholder="Выберите город проведения"
          :options="citiesOption"
          :showLabels="false"
          :searchable="true"
          :allow-empty="true"
          :showPointer="false"
          :multiple="true"
          :close-on-select="false"
          :clear-on-select="false"
        >
          <span slot="noResult">Не найдено</span>
          <span slot="noOptions">Не найдено</span>
        </multiselect>
      </div>
      <div>
        <div v-for="course in filterItems" :key="course.id">
          <course-element :course="course" :canDelete="false"> </course-element>
        </div>
        <p v-if="filterItems.length == 0">Не найдено</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  CITIES,
  PUBLISHED_COURSES,
  SHORT_LIST_ORGANIZATIONS,
  SUBJECTS,
} from "@/graphql/queries/queries";
import CourseElement from "@/components/course/CourseElement.vue";
import Multiselect from "vue-multiselect";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "CourseList",
  apollo: {
    publishedCourses: {
      query: PUBLISHED_COURSES,
    },
    subjects: {
      query: SUBJECTS,
    },
    cities: {
      query: CITIES,
    },
    organizations: {
      query: SHORT_LIST_ORGANIZATIONS,
    },
  },
  components: {
    CourseElement,
    Loader,
    Multiselect,
  },
  data() {
    return {
      findString: "",
      findSubject: [],
      findCities: [],
      findOrganization: [],
      findFormat: [],
      formats: [
        { value: "ON", text: "Онлайн" },
        { value: "OFF", text: "Оффлайн" },
        { value: "BOTH", text: "В смешанном формате" },
      ],
    };
  },
  computed: {
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    organizationsOption() {
      if (this.organizations == undefined) return [];
      else return this.organizations;
    },
    citiesOption() {
      if (this.cities == undefined) return [];
      else return this.cities;
    },
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
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
        if (this.findFormat.length != 0) {
          courses = courses.filter((el) => {
            let flag = false;
            this.findFormat.forEach((format) => {
              if (el.form == format.value) flag = true;
            });
            return flag;
          });
        }
        if (this.findOrganization.length != 0) {
          courses = courses.filter((el) => {
            let flag = false;
            this.findOrganization.forEach((organization) => {
              if (el.organization.id == organization.id) flag = true;
            });
            return flag;
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
        if (this.findCities.length != 0) {
          courses = courses.filter((el) => {
            let flag = false;
            this.findCities.forEach((city) => {
              if (el.city.id == city.id) flag = true;
            });
            return flag;
          });
        }
      } else courses = [];
      return courses;
    },
  },

  methods: {
    offlineFormat() {
      if (this.findFormat.length == 0) return true;
      else {
        if (
          this.findFormat.find(
            (format) => "BOTH" == format.value || "OFF" == format.value
          ) != undefined
        )
          return true;
        else return false;
      }
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
