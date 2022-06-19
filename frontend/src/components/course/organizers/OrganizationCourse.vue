<template>
  <div>
    <loader v-if="isLoading || course == undefined"></loader>
    <div v-else>
      <div v-if="!edit">
        <div class="position-relative">
          <h1 class="mb-3">
            {{ course.name }}
          </h1>
          <p
            class="position-absolute"
            style="font-size: 20px; top: -20px; right: 0"
            v-if="course.published"
          >
            <span class="badge badge-primary mr-2"> Опубликовано </span>
          </p>
          <p
            class="position-absolute"
            style="font-size: 20px; top: -20px; right: 0"
            v-if="!course.published"
          >
            <span class="badge badge-danger mr-2"> Не опубликовано </span>
          </p>
        </div>
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

        <p v-if="whatIsStudyingForm(course.form) != ''">
          Курс проводится {{ whatIsStudyingForm(course.form) }}.
        </p>
        <p v-if="whatIsDurationType(course.duration) != ''">
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
        <p v-if="course.maxNumberMember != undefined">
          Ограничения по количеству зарегистрированных участников:
          {{ course.maxNumberMember }} .
        </p>
        <p>
          <a
            @click="onLink"
            style="cursor: pointer"
            class="text-decoration-none"
            >Посмотреть записавшихся на курс</a
          >
        </p>
        <p>Действия:</p>
        <button
          @click="
            modal = true;
            modalId = course.id;
            modalName = course.name;
          "
          class="text-gradient btn-sm mr-2"
        >
          Удалить
          <span class="text">Удалить</span>
        </button>
        <button
          class="gradient btn-sm mr-2"
          v-if="!course.published"
          @click="onEdit"
        >
          Отредактировать
        </button>
        <button
          v-if="!course.published"
          @click="toPublish(course.id, true)"
          class="text-gradient btn-sm mr-2"
        >
          Опубликовать
          <span class="text">Опубликовать</span>
        </button>
        <button
          v-if="course.published"
          @click="toPublish(course.id, false)"
          class="text-gradient btn-sm"
        >
          Снять с публикации
          <span class="text">Снять с публикации</span>
        </button>
      </div>
      <div v-else>
        <h1>Редактирование курса</h1>
        <form>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="name">Название *</label><br />
              <input
                id="name"
                name="name"
                type="text"
                class="form-control"
                v-model.trim="form.name"
                :class="{
                  'is-invalid': submittedForm && $v.form.name.$error,
                }"
              />
              <p
                v-if="submittedForm && !$v.form.name.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="description">Описание </label><br />
              <textarea
                class="form-control"
                name="description"
                id="description"
                cols="30"
                rows="10"
                v-model.trim="form.description"
                :class="{
                  'is-invalid': submittedForm && $v.form.description.$error,
                }"
              ></textarea>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="subjects">Предметы *</label><br />
              <multiselect
                :disabled="subjects == undefined"
                v-model="form.subjects"
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
              <div class="is-invalid"></div>
              <p
                v-if="submittedForm && !$v.form.subjects.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="duration">Длительность</label><br />
              <select
                class="form-control"
                v-model="form.duration"
                name="duration"
                id="duration"
                :class="{
                  'is-invalid': submittedForm && $v.form.duration.$error,
                }"
              >
                <option value="LESSMONTH">Меньше месяца</option>
                <option value="MONTH">1-2 месяца</option>
                <option value="FEWMONTH">От двух месяцев до полугода</option>
                <option value="HALFYEAR">От полугода до года</option>
                <option value="YEARANDMORE">Год и более</option>
              </select>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="form">Формат проведения *</label
              ><br />
              <select
                class="form-control"
                v-model="form.form"
                name="form"
                id="form"
                :class="{
                  'is-invalid': submittedForm && $v.form.form.$error,
                }"
              >
                <option value="ON">Онлайн</option>
                <option value="OFF">Оффлайн</option>
                <option value="BOTH">Смешанный</option>
              </select>
              <p
                v-if="submittedForm && !$v.form.form.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="dateStart">Дата начала</label><br />
              <input
                class="form-control"
                id="dateStart"
                name="dateStart"
                type="date"
                v-model="form.dateStart"
                :class="{
                  'is-invalid': submittedForm && $v.form.dateStart.$error,
                }"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="dateEnd">Дата окончания</label
              ><br />
              <input
                class="form-control"
                id="dateEnd"
                name="dateEnd"
                type="date"
                v-model="form.dateEnd"
                :class="{
                  'is-invalid': submittedForm && $v.form.dateEnd.$error,
                }"
              />
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name">Город проведения </label><br />
              <multiselect
                v-model="form.city"
                track-by="id"
                label="name"
                placeholder="Выберите город"
                :options="citiesOption"
                :showLabels="false"
                :searchable="true"
                :allow-empty="true"
                :showPointer="false"
                :multiple="false"
                :close-on-select="true"
                :class="{
                  'is-invalid': submittedForm && $v.form.city.$error,
                }"
              >
                <span slot="noResult">Не найдено</span>
              </multiselect>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="maxNumberMember"
                >Максимальное количество слушателей </label
              ><br />
              <input
                class="form-control"
                name="maxNumberMember"
                id="maxNumberMember"
                type="number"
                min="1"
                step="1"
                v-model.trim="form.maxNumberMember"
                :class="{
                  'is-invalid': submittedForm && $v.form.maxNumberMember.$error,
                }"
              />
            </div>
          </div>
        </form>

        <p>* - обязательное поле</p>
        <button class="gradient" @click="onEdit">Сохранить</button>

        <modal-delete-course
          v-if="modal"
          @delete="deleteCourse"
          @close="
            modal = false;
            modalId = 0;
            modalName = '';
          "
          :courseId="modalId"
          :courseName="modalName"
        ></modal-delete-course>
      </div>
    </div>
  </div>
</template>

<script>
import {
  PUBLISH_COURSE,
  UPDATE_COURSE,
  DELETE_COURSE,
  CREATE_COURSE_SUBJECT,
  DELETE_COURSE_SUBJECT,
} from "@/graphql/mutations/mutations";
import ModalDeleteCourse from "@/components/course/organizers/ModalDeleteCourse.vue";
import { required, integer } from "vuelidate/lib/validators";
import Multiselect from "vue-multiselect";
import { CITIES, COURSE, SUBJECTS } from "@/graphql/queries/queries";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "OrganizationCourse",
  apollo: {
    course: {
      query: COURSE,
      variables() {
        return {
          courseId: this.$route.params.id,
        };
      },
    },
    subjects: {
      query: SUBJECTS,
    },
    cities: {
      query: CITIES,
    },
  },
  components: {
    Multiselect,
    ModalDeleteCourse,
    Loader,
  },
  data() {
    return {
      modal: false,
      modalId: 0,
      modalName: "",
      form: {
        name: undefined,
        description: undefined,
        duration: undefined,
        form: undefined,
        dateStart: undefined,
        dateEnd: undefined,
        city: { id: undefined, name: undefined },
        subjects: [],
        maxNumberMember: undefined,
      },
      edit: false,

      submittedForm: false,
    };
  },
  validations: {
    form: {
      name: { required },
      description: {},
      duration: {},
      form: { required },
      dateStart: {},
      dateEnd: {},
      maxNumberMember: { integer },
      subjects: { required },
      city: {},
    },
  },
  computed: {
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    citiesOption() {
      if (this.cities == undefined) return [];
      else return this.cities;
    },

    isLoading() {
      return this.$store.state.isLoading;
    },
  },
  methods: {
    deleteCourse() {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: DELETE_COURSE,
          variables: {
            courseId: this.$route.params.id,
          },
        })
        .then(() => {
          this.$router.push({
            name: "OrganizationCourses",
          });
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
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
          this.$apollo.queries.course.refresh();
          this.$apollo.queries.course.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    onLink() {
      this.$router.push({
        name: "CourseMembers",
        params: { id: this.course.id },
      });
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
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
    onEdit() {
      if (this.edit) {
        this.submittedForm = true;
        this.$v.form.$touch();
        if (this.$v.form.$invalid) {
          return;
        }
        let cityId =
          this.form.city == undefined ? undefined : this.form.city.id;
        let subjectsArr = [];
        if (
          this.course.courseSubject != null &&
          this.course.courseSubject != undefined &&
          this.course.courseSubject.length != 0
        ) {
          this.course.courseSubject.forEach((element) => {
            subjectsArr.push(element.subject);
          });
        }
        let newSubjects = this.form.subjects.filter((sub) =>
          subjectsArr.every((item) => item.id !== sub.id)
        );
        let deletedSubjects = subjectsArr.filter((sub) =>
          this.form.subjects.every((item) => item.id !== sub.id)
        );
        this.$store.commit("START_LOADING");

        this.$apollo
          .mutate({
            mutation: UPDATE_COURSE,
            variables: {
              courseId: this.course.id,
              name: this.form.name,
              form: this.form.form,
              description: this.form.description,
              duration: this.form.duration,
              dateStart: this.form.dateStart,
              dateEnd: this.form.dateEnd,
              cityId: cityId,
              maxNumberMember: this.form.maxNumberMember,
            },
          })
          .then(() => {
            newSubjects.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: CREATE_COURSE_SUBJECT,
                  variables: {
                    subjectId: element.id,
                    courseId: this.course.id,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });
            deletedSubjects.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: DELETE_COURSE_SUBJECT,
                  variables: {
                    subjectId: element.id,
                    courseId: this.course.id,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });

            this.$apollo.queries.course.refresh();
            this.$apollo.queries.course.refetch();

            this.edit = false;
            this.submittedForm = false;
          })
          .catch((error) => {
            console.error(error);
          });
        this.$store.commit("STOP_LOADING");
      } else {
        this.$store.commit("START_LOADING");

        this.edit = true;
        this.form.name = this.course.name;
        this.form.form = this.course.form;
        this.form.description = this.course.description;
        this.form.duration = this.course.duration;
        this.form.dateStart = this.course.dateStart;
        this.form.dateEnd = this.course.dateEnd;
        this.form.maxNumberMember = this.course.maxNumberMember;
        if (this.course.city != null && this.course.city != undefined) {
          this.form.city.id = this.course.city.id;
          this.form.city.name = this.course.city.name;
        }
        if (
          this.course.courseSubject != null &&
          this.course.courseSubject != undefined &&
          this.course.courseSubject.length != 0
        ) {
          let subjectsArr = [];
          this.course.courseSubject.forEach((element) => {
            subjectsArr.push(element.subject);
          });
          this.form.subjects = subjectsArr;
          this.$store.commit("STOP_LOADING");
        }
      }
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
