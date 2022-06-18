<template>
  <div>
    <loader v-if="isLoading"></loader>
    <div v-else>
      <h1>Создание курса</h1>
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
              :class="{ 'is-invalid': submittedForm && $v.form.name.$error }"
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
              :class="{
                'is-invalid': submittedForm && !$v.form.subjects.required,
              }"
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
              v-model="form.duration"
              name="duration"
              class="form-control"
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
              :class="{ 'is-invalid': submittedForm && $v.form.form.$error }"
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
            <label class="form-name" for="dateEnd">Дата окончания</label><br />
            <input
              class="form-control"
              id="dateEnd"
              name="dateEnd"
              type="date"
              v-model="form.dateEnd"
              :class="{ 'is-invalid': submittedForm && $v.form.dateEnd.$error }"
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
              :class="{ 'is-invalid': submittedForm && $v.form.city.$error }"
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
              name="maxNumberMember"
              id="maxNumberMember"
              type="number"
              min="1"
              class="form-control"
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
      <button class="text-gradient to-block" @click="onAdd">
        Добавить
        <span class="text">Добавить</span>
      </button>
      <Transition name="fade">
        <div
          v-if="newObj"
          class="position-fixed my-sticker bottom-0 right-0 p-3"
          style="z-index: 1000; width: 300px; right: 0; bottom: 140px"
        >
          <div class="alert alert-primary" role="alert">
            Вы успешно создали курс!
            <router-link
              tag="a"
              class="text-decoration-none"
              :to="{ name: 'OrganizationCourses' }"
              >Перейти к списку курсов организации</router-link
            >.
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import {
  CREATE_COURSE,
  CREATE_COURSE_SUBJECT,
} from "@/graphql/mutations/mutations";
import { required, integer } from "vuelidate/lib/validators";
import Multiselect from "vue-multiselect";
import { CITIES, SUBJECTS } from "@/graphql/queries/queries";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "NewCourse",
  apollo: {
    subjects: {
      query: SUBJECTS,
    },
    cities: {
      query: CITIES,
    },
  },
  components: {
    Multiselect,
    Loader,
  },

  data() {
    return {
      createdId: undefined,
      form: {
        name: undefined,
        description: undefined,
        duration: undefined,
        form: undefined,
        dateStart: undefined,
        dateEnd: undefined,
        subjects: [],
        city: undefined,
        maxNumberMember: undefined,
      },
      submittedForm: false,
      newObj: false,
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
      subjects: { required },
      maxNumberMember: { integer },
      city: {},
    },
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    organizationId() {
      return jwt.decode(localStorage.getItem("token")).organization_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    citiesOption() {
      if (this.cities == undefined) return [];
      else return this.cities;
    },
  },
  methods: {
    onAdd() {
      this.submittedForm = true;
      this.$v.form.$touch();
      if (this.$v.form.$invalid) {
        return;
      }
      let cityId = this.form.city == undefined ? undefined : this.form.city.id;
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({
          mutation: CREATE_COURSE,
          variables: {
            name: this.form.name,
            form: this.form.form,
            organizationId: this.organizationId,
            description: this.form.description,
            duration: this.form.duration,
            dateStart: this.form.dateStart,
            dateEnd: this.form.dateEnd,
            cityId: cityId,
            maxNumberMember: this.form.maxNumberMember,
          },
        })
        .then((result) => {
          this.createdId = result.data.createCourse.course.id;
          this.form.subjects.forEach((element) => {
            this.$apollo
              .mutate({
                mutation: CREATE_COURSE_SUBJECT,
                variables: {
                  subjectId: element.id,
                  courseId: this.createdId,
                },
              })
              .then(() => {})
              .catch((error) => {
                console.error(error);
              });
          });

          this.form = {
            name: undefined,
            description: undefined,
            duration: undefined,
            form: undefined,
            dateStart: undefined,
            dateEnd: undefined,
            subjects: [],
            city: undefined,
            maxNumberMember: undefined,
          };

          this.submittedForm = false;
          this.newObj = true;
          setTimeout(() => {
            this.newObj = false;
          }, 5000);
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss">
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
