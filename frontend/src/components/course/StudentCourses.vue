<template>
  <div>
    <loader v-if="isLoading || studentCourses == undefined"></loader>
    <div v-else>
      <h1>Мои курсы</h1>
      <div class="row mb-5">
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <input
            placeholder="Поиск по названию и описанию"
            name="search"
            id="search"
            class="form-control"
            :disabled="studentCourses == undefined"
            type="text"
            v-model.trim="findString"
          />
        </div>
        <div class="col-lg-3 mb-2">
          <multiselect
            :disabled="studentCourses == undefined || subjects == undefined"
            v-model="findSubject"
            track-by="id"
            label="name"
            placeholder="Школьные предметы"
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
        <div class="col-lg-2 mb-2">
          <multiselect
            :disabled="studentCourses == undefined"
            v-model="findFormat"
            track-by="value"
            label="text"
            placeholder="Формат"
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
        </div>
        <div class="col-lg-3 mb-">
          <multiselect
            :disabled="
              studentCourses == undefined || organizations == undefined
            "
            v-model="findOrganization"
            track-by="id"
            label="fullname"
            placeholder="Организатор"
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
        </div>
      </div>

      <div class="mb-5">
        <div v-for="course in filterItems" :key="course.id">
          <course-element
            :course="course"
            :canDelete="true"
            @cancel="refreshList()"
          >
          </course-element>
        </div>
        <p v-if="filterItems.length == 0">Не найдено</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  STUDENT_COURSES,
  SHORT_LIST_ORGANIZATIONS,
  SUBJECTS,
} from "@/graphql/queries/queries";
import jwt from "jsonwebtoken";
import CourseElement from "@/components/course/CourseElement.vue";
import Multiselect from "vue-multiselect";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "StudentCourses",
  apollo: {
    studentCourses: {
      query: STUDENT_COURSES,
      variables() {
        return {
          userId: this.userId,
        };
      },
    },
    subjects: {
      query: SUBJECTS,
    },

    organizations: {
      query: SHORT_LIST_ORGANIZATIONS,
    },
  },
  components: {
    CourseElement,
    Multiselect,
    Loader,
  },
  data() {
    return {
      findString: "",
      findSubject: [],
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
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    organizationsOption() {
      if (this.organizations == undefined) return [];
      else return this.organizations;
    },

    filterItems() {
      let courses;
      if (
        this.studentCourses != null &&
        this.studentCourses != undefined &&
        this.studentCourses.length != 0
      ) {
        courses = this.studentCourses;
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
      } else courses = [];
      return courses;
    },
  },

  methods: {
    refreshList() {
      this.$apollo.queries.studentCourses.refresh();
      this.$apollo.queries.studentCourses.refetch();
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss">
div.col-lg-2 div.multiselect__tags,
div.col-lg-4 div.multiselect__tags,
div.col-lg-3 div.multiselect__tags {
  border: 1px solid #ced4da;
  color: #495057;
  font-weight: 400;
}

div.col-lg-2
  div.multiselect
  div.multiselect__tags
  div.multiselect__tags-wrap
  span.multiselect__tag,
div.col-lg-3
  div.multiselect
  div.multiselect__tags
  div.multiselect__tags-wrap
  span.multiselect__tag,
div.col-lg-4
  div.multiselect
  div.multiselect__tags
  div.multiselect__tags-wrap
  span.multiselect__tag {
  background: #924de9 !important;
  & .multiselect__tag-icon:focus,
  .multiselect__tag-icon:hover {
    background: #924de9 !important;
  }
  & span {
    color: white !important;
  }
}
</style>
