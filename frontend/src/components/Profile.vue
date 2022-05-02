<template>
  <div>
    <h1>Личный кабинет</h1>
    <div class="form-group">
      <label class="form-name"
        >Фамилия <span v-if="edit && isStudent()">*</span></label
      ><br />
      <p v-if="!edit || !isStudent()">{{ user.lastName }}</p>
      <input
        v-else-if="isStudent()"
        id="lastName"
        :disabled="isLoading"
        type="text"
        v-model.trim="form.lastName"
        :class="{ 'is-invalid': submittedForm && v$.form.lastName.$error }"
      />
      <div
        v-if="submittedForm && v$.form.lastName.$error && isStudent()"
        class="invalid-feedback"
      >
        <span v-if="v$.form.lastName.required.$invalid"
          >Данное поле обязательно</span
        >
      </div>
    </div>
    <div class="form-group">
      <label class="form-name"
        >Имя <span v-if="edit && isStudent()">*</span></label
      ><br />
      <p v-if="!edit || !isStudent()">{{ user.firstName }}</p>
      <input
        v-else-if="isStudent()"
        id="firstName"
        :disabled="isLoading"
        type="text"
        v-model.trim="form.firstName"
        :class="{ 'is-invalid': submittedForm && v$.form.firstName.$error }"
      />
      <div
        v-if="submittedForm && v$.form.firstName.$error && isStudent()"
        class="invalid-feedback"
      >
        <span v-if="v$.form.firstName.required.$invalid"
          >Данное поле обязательно</span
        >
      </div>
    </div>
    <div class="form-group" v-if="isStudent()">
      <label class="form-name">Отчество</label><br />
      <p v-if="!edit">{{ user.patronymic }}</p>
      <input
        v-else
        id="patronymic"
        :disabled="isLoading"
        type="text"
        v-model.trim="form.patronymic"
        :class="{ 'is-invalid': submittedForm && v$.form.patronymic.$error }"
      />
    </div>
    <div class="form-group" v-if="isStudent()">
      <label class="form-name">Дата рождения</label><br />
      <p v-if="!edit">{{ user.birthdate }}</p>
      <input
        v-else
        id="birthdate"
        :disabled="isLoading"
        type="date"
        v-model="form.birthdate"
        :max="new Date().toISOString().substr(0, 10)"
        :class="{ 'is-invalid': submittedForm && v$.form.birthdate.$error }"
      />
    </div>
    <div class="form-group" v-if="isStudent()">
      <label class="form-name">Город проживания </label><br />
      <p v-if="!edit">{{ user.city }}</p>
      <model-select
        v-else
        class="search-select"
        ref="modelSelect"
        :isDisabled="isLoading"
        :options="cityList"
        :isError="submittedForm && v$.form.city.$error"
        v-model="form.city"
      ></model-select>
    </div>
    <div class="form-group" v-if="!isStudent()">
      <label class="form-name">Организация </label><br />
      <p>{{ user.organization }}</p>
    </div>
    <div class="form-group" v-if="!isStudent()">
      <label class="form-name">Должность</label><br />
      <p v-if="!edit">{{ user.position }}</p>
      <input
        v-else
        id="position"
        :disabled="isLoading"
        type="text"
        v-model.trim="formEmployee.position"
      />
    </div>
    <div class="form-group">
      <label class="form-name"
        >E-mail <span v-if="edit && isStudent()">*</span></label
      ><br />
      <p v-if="!edit || !isStudent()">{{ user.email }}</p>
      <input
        v-else-if="isStudent()"
        id="email"
        :disabled="isLoading"
        type="text"
        v-model.trim="form.email"
        :class="{ 'is-invalid': submittedForm && v$.form.email.$error }"
      />
      <div
        v-if="submittedForm && v$.form.email.$error && isStudent()"
        class="invalid-feedback"
      >
        <span v-if="v$.form.email.required.$invalid"
          >Данное поле обязательно</span
        >
        <span v-if="v$.form.email.email.$invalid">Некорректный email</span>
      </div>
    </div>
    <div v-if="edit">
      <p v-if="!changePassword" @click="changePassword = true">
        Изменить пароль
      </p>
      <div v-else>
        <div class="form-group">
          <label class="form-name">Пароль</label><br />
          <input
            id="password"
            :disabled="isLoading"
            :type="passShow ? 'text' : 'password'"
            v-model="password.password"
            :class="{
              'is-invalid': submittedPassword && v$.password.password.$error,
            }"
          />
          <button @click="passShow = !passShow">Показать/спрятать</button>

          <div
            v-if="submittedPassword && v$.password.password.$error"
            class="invalid-feedback"
          >
            <span v-if="v$.password.password.minLength.$invalid"
              >Пароль должен содержать не менее 6 символов</span
            >
          </div>
        </div>
        <div class="form-group">
          <label class="form-name">Повторите пароль</label><br />
          <input
            id="confirmPassword"
            :disabled="isLoading"
            :type="passShow2 ? 'text' : 'password'"
            v-model="password.confirmPassword"
            :class="{
              'is-invalid':
                submittedPassword && v$.password.confirmPassword.$error,
            }"
          />
          <button @click="passShow2 = !passShow2">Показать/спрятать</button>
          <div
            v-if="submittedPassword && !passwordIsSame()"
            class="invalid-feedback"
          >
            <span>Пароли не совпадают</span>
          </div>
        </div>
      </div>
    </div>

    <p v-if="edit">* - обязательное поле</p>
    <button v-if="edit" @click="onEdit">Сохранить</button>
    <button v-if="!edit" @click="onEdit">Изменить</button>
    <p>
      <router-link tag="a" :to="{ name: 'DeleteAccount' }"
        >Удалить аккаунт</router-link
      >
    </p>
  </div>
</template>

<script>
import useVuelidate from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";
import { ModelListSelect } from "vue-search-select";
import { ModelSelect } from "vue-search-select";
import "vue-search-select/dist/VueSearchSelect.css";

export default {
  name: "Profile",
  setup() {
    return { v$: useVuelidate() };
  },
  components: {
    ModelListSelect,
    ModelSelect,
  },
  data() {
    return {
      user: {
        firstName: "Дарья",
        lastName: "Беляева",
        patronymic: "Владиславовна",
        birthdate: "2000-11-24",
        email: "d.belyaeva@gmail.com",
        password: "",
        confirmPassword: "",
        city: "2",
        role: 2,
        position: "Отдел кадров",
        organization: "CUSTIS",
      },
      form: {
        firstName: "",
        lastName: "",
        patronymic: "",
        birthdate: "",
        email: "",
        city: "",
      },
      formEmployee: {
        position: "",
      },
      password: {
        password: "",
        confirmPassword: "",
      },
      edit: false,
      changePassword: false,
      passShow: false,
      passShow2: false,
      submittedForm: false,
      submittedPassword: false,
      isLoading: false,
      cityList: [
        { text: "Один", value: "1" },
        { text: "Два", value: "2" },
        { text: "Три", value: "5" },
      ],
    };
  },
  validations: {
    form: {
      firstName: { required },
      lastName: { required },
      patronymic: {},
      birthdate: {},
      email: {
        required,
        email,
      },
      city: {},
    },
    password: {
      password: { minLength: minLength(6) },
      confirmPassword: {},
    },
  },
  methods: {
    passwordIsSame() {
      return this.password.password === this.password.confirmPassword;
    },
    isStudent() {
      return this.user.role == 1;
    },
    onEdit() {
      if (this.isStudent()) {
        if (!this.edit) {
          // Если нажата кнопка редактировать, значения полей переносится в форму
          this.edit = true;
          this.form.lastName = this.user.lastName;
          this.form.firstName = this.user.firstName;
          this.form.patronymic = this.user.patronymic;
          this.form.birthdate = this.user.birthdate;
          this.form.city = this.user.city;
          this.form.email = this.user.email;
        } else {
          // Поставить загрузку
          this.isLoading = true;
          // Основная форма была отправлена
          this.submittedForm = true;
          this.v$.form.$touch();
          // Проверка: корректно ли заполнена основная форма
          if (this.v$.form.$invalid) {
            this.isLoading = false;
            return;
          }
          // Если была нажата кнопка Изменить пароль
          if (this.changePassword) {
            // Форма пароля была отправлена
            this.submittedPassword = true;
            this.v$.password.$touch();
            // Корректно ли заполнена форма
            if (this.v$.password.$invalid || !this.passwordIsSame()) {
              this.isLoading = false;
              return;
            }
          }

          this.user.lastName = this.form.lastName;
          this.user.firstName = this.form.firstName;
          this.user.patronymic = this.form.patronymic;
          this.user.birthdate = this.form.birthdate;
          this.user.city = this.form.city;
          this.user.email = this.form.email;
          this.changePassword = false;
          this.edit = false;
          this.isLoading = false;
        }
      } else {
        if (!this.edit) {
          // Если нажата кнопка редактировать, значения полей переносится в форму
          this.edit = true;
          this.formEmployee.position = this.user.position;
        } else {
          // Поставить загрузку
          this.isLoading = true;
          // Если была нажата кнопка Изменить пароль
          if (this.changePassword) {
            // Форма пароля была отправлена
            this.submittedPassword = true;
            this.v$.password.$touch();
            // Корректно ли заполнена форма
            if (this.v$.password.$invalid || !this.passwordIsSame()) {
              this.isLoading = false;
              return;
            }
          }

          this.user.position = this.formEmployee.position;
          this.changePassword = false;
          this.edit = false;
          this.isLoading = false;
        }
      }
    },
  },
};
</script>

<style lang="scss"></style>
