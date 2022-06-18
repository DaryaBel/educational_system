<template>
  <div>
    <loader v-if="isLoading || organizationCourses == undefined"></loader>
    <div v-else>
      <h1>Курсы организации</h1>
      <button @click="onLink()" class="mb-3 text-gradient to-block">
        Добавить новый курс
        <span class="text">Добавить новый курс</span>
      </button>
      <div class="row mb-3">
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <input
            placeholder="Поиск по названию и описанию"
            name="search"
            id="search"
            class="form-control"
            :disabled="organizationCourses == undefined"
            type="text"
            v-model.trim="findString"
          />
        </div>
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <span class="mr-2">Опубликован?</span>
          <select
            name="published"
            class="form-control"
            id="published"
            v-model="published"
          >
            <option value="all">Все</option>
            <option value="yes">Да</option>
            <option value="no">Нет</option>
          </select>
        </div>
      </div>
      <div>
        <p v-if="filterItems.length == 0">Не найдено</p>
        <table v-else class="table">
          <tr>
            <th scope="col">Название</th>
            <th scope="col">Предметы</th>
            <th scope="col">Форма проведения</th>
            <th scope="col">Опубликовано</th>
            <th scope="col"></th>
          </tr>
          <tr v-for="course in filterItems" :key="course.id">
            <td>
              <router-link
                tag="a"
                class="text-decoration-none"
                :to="{
                  name: 'OrganizationCourse',
                  params: { id: course.id },
                }"
                >{{ course.name }}</router-link
              >
            </td>
            <td>
              <span
                v-for="subject in course.courseSubject"
                :key="subject.subject.id"
              >
                {{ subject.subject.name }} <br />
              </span>
            </td>
            <td>{{ whatIsStudyingForm(course.form) }}</td>
            <td>{{ course.published ? "Да" : "Нет" }}</td>
            <td>
              <button
                class="mb-2 btn-sm text-gradient"
                @click="
                  openModal();
                  modal = true;
                  modalId = course.id;
                  modalName = course.name;
                "
              >
                Удалить
                <span class="text">Удалить</span>
              </button>
              <br />
              <button
                class="gradient btn-sm"
                v-if="!course.published"
                @click="toPublish(course.id, true)"
              >
                Опубликовать
              </button>
              <button
                class="gradient btn-sm"
                v-if="course.published"
                @click="toPublish(course.id, false)"
              >
                Снять с публикации
              </button>
            </td>
          </tr>
        </table>
        <modal-delete-course
          v-if="modal"
          @delete="deleteCourse"
          @close="
            modal = false;
            modalId = 0;
            modalName = '';
            closeModal();
          "
          :courseId="modalId"
          :courseName="modalName"
        ></modal-delete-course>
      </div>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import { PUBLISH_COURSE, DELETE_COURSE } from "@/graphql/mutations/mutations";
import { ORGANIZATION_COURSES } from "@/graphql/queries/queries";
import ModalDeleteCourse from "@/components/course/organizers/ModalDeleteCourse.vue";
import Loader from "@/components/parts/Loader.vue";
export default {
  name: "OrganizationCourses",
  apollo: {
    organizationCourses: {
      query: ORGANIZATION_COURSES,
      variables() {
        return {
          organizationId: this.organizationId,
        };
      },
    },
  },
  components: {
    ModalDeleteCourse,
    Loader,
  },

  data() {
    return {
      modal: false,
      modalId: 0,
      modalName: "",
      findString: "",
      published: "all",
    };
  },
  computed: {
    organizationId() {
      return jwt.decode(localStorage.getItem("token")).organization_id;
    },

    isLoading() {
      return this.$store.state.isLoading;
    },
    filterItems() {
      let courses;
      if (
        this.organizationCourses != null &&
        this.organizationCourses != undefined &&
        this.organizationCourses.length != 0
      ) {
        courses = this.organizationCourses;
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
        if (this.published != "all") {
          courses = courses.filter((el) => {
            let publishedBoolean = this.published == "yes" ? true : false;
            return el.published == publishedBoolean;
          });
        }
      } else courses = [];
      return courses;
    },
  },

  methods: {
    whatIsStudyingForm(studyingForm) {
      if (studyingForm == "ON") return "онлайн";
      if (studyingForm == "OFF") return "оффлайн";
      if (studyingForm == "BOTH") return "в смешанном формате";
      return "";
    },
    toPublish(courseId, published) {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: PUBLISH_COURSE,
          variables: {
            courseId: courseId,
            published: published,
          },
        })
        .then(() => {
          this.$apollo.queries.organizationCourses.refresh();
          this.$apollo.queries.organizationCourses.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    openModal() {
      document.documentElement.style.overflow = "hidden";
    },
    closeModal() {
      document.documentElement.style.overflow = "auto";
    },
    onLink() {
      this.$router.push({ name: "NewCourse" });
    },
    deleteCourse(courseId) {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: DELETE_COURSE,
          variables: {
            courseId: courseId,
          },
        })
        .then(() => {
          this.$apollo.queries.organizationCourses.refresh();
          this.$apollo.queries.organizationCourses.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
  },
};
</script>

<style lang="scss"></style>
