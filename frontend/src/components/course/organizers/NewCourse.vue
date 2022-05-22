<template>
  <div>
    <p v-if="isLoading">Загрузка...</p>
    <div v-else>
      <h1>Создать курс</h1>
      <div class="form-group">
        <label for="name">Название *</label><br />
        <input
          id="name"
          name="name"
          type="text"
          v-model.trim="form.name"
          :class="{ 'is-invalid': submittedForm && v$.form.name.$error }"
        />
        <div
          v-if="submittedForm && v$.form.name.$error"
          class="invalid-feedback"
        >
          <span v-if="v$.form.name.required.$invalid"
            >Данное поле обязательно</span
          >
        </div>
      </div>
      <div class="form-group">
        <label for="description">Описание </label><br />
        <textarea
          name="description"
          id="description"
          cols="30"
          rows="10"
          v-model.trim="form.description"
          :class="{ 'is-invalid': submittedForm && v$.form.description.$error }"
        ></textarea>
      </div>
      <div class="form-group">
        <label for="subjects">Предметы *</label><br />
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
        <div
          v-if="submittedForm && v$.form.subjects.$error"
          class="invalid-feedback"
        >
          <span v-if="v$.form.subjects.required.$invalid"
            >Данное поле обязательно</span
          >
        </div>
      </div>
      <div class="form-group">
        <label for="duration">Длительность</label><br />
        <select
          v-model="form.duration"
          name="duration"
          id="duration"
          :class="{ 'is-invalid': submittedForm && v$.form.duration.$error }"
        >
          <option value="LESSMONTH">Меньше месяца</option>
          <option value="MONTH">1-2 месяца</option>
          <option value="FEWMONTH">От двух месяцев до полугода</option>
          <option value="HALFYEAR">От полугода до года</option>
          <option value="YEARANDMORE">Год и более</option>
        </select>
      </div>
      <div class="form-group">
        <label for="form">Формат проведения *</label><br />
        <select
          v-model="form.form"
          name="form"
          id="form"
          :class="{ 'is-invalid': submittedForm && v$.form.form.$error }"
        >
          <option value="ON">Онлайн</option>
          <option value="OFF">Оффлайн</option>
          <option value="BOTH">Смешанный</option>
        </select>
        <div
          v-if="submittedForm && v$.form.form.$error"
          class="invalid-feedback"
        >
          <span v-if="v$.form.form.required.$invalid"
            >Данное поле обязательно</span
          >
        </div>
      </div>
      <div class="form-group">
        <label for="dateStart">Дата начала</label><br />
        <input
          id="dateStart"
          name="dateStart"
          type="date"
          v-model="form.dateStart"
          :class="{ 'is-invalid': submittedForm && v$.form.dateStart.$error }"
        />
      </div>
      <div class="form-group">
        <label for="dateEnd">Дата окончания</label><br />
        <input
          id="dateEnd"
          name="dateEnd"
          type="date"
          v-model="form.dateEnd"
          :class="{ 'is-invalid': submittedForm && v$.form.dateEnd.$error }"
        />
      </div>
      <div class="form-group">
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
          :class="{ 'is-invalid': submittedForm && v$.form.city.$error }"
        >
          <span slot="noResult">Не найдено</span>
        </multiselect>
      </div>
      <div class="form-group">
        <label for="maxNumberMember">Максимальное количество слушателей </label
        ><br />
        <input
          name="maxNumberMember"
          id="maxNumberMember"
          type="number"
          min="1"
          step="1"
          v-model.trim="form.maxNumberMember"
          :class="{
            'is-invalid': submittedForm && v$.form.maxNumberMember.$error,
          }"
        />
      </div>

      <p>* - обязательное поле</p>
      <button @click="onAdd">Добавить</button>
    </div>
  </div>
</template>

<script>
import {
  CREATE_COURSE,
  CREATE_COURSE_SUBJECT,
} from "@/graphql/mutations/mutations";
import useVuelidate from "@vuelidate/core";
import { required, integer } from "@vuelidate/validators";
import Multiselect from "vue-multiselect";
import { CITIES, SUBJECTS } from "@/graphql/queries/queries";

export default {
  name: "NewCourse",
  setup() {
    return { v$: useVuelidate() };
  },
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
      userId: 2,
      organizationId: 4,
      submittedForm: false,
      isLoading: false,
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
      this.isLoading = true;
      this.submittedForm = true;
      this.v$.form.$touch();
      if (this.v$.form.$invalid) {
        this.isLoading = false;
        return;
      }
      let cityId = this.form.city == undefined ? undefined : this.form.city.id;

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
          this.isLoading = false;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
