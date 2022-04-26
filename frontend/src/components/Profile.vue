<template>
  <div>
    <h1>Личный кабинет</h1>
    <div class="form-group">
      <label class="form-name">Фамилия *</label><br />
      <input
        id="lastName"
        :disabled="signupLoading"
        type="text"
        v-model.trim="form.lastName"
        :class="{ 'is-invalid': submitted && v$.form.lastName.$error }"
      />
      <div v-if="submitted && v$.form.lastName.$error" class="invalid-feedback">
        <span v-if="v$.form.lastName.required.$invalid"
          >Данное поле обязательно</span
        >
      </div>
    </div>
    <div class="form-group">
      <label class="form-name">Имя *</label><br />
      <input
        id="firstName"
        :disabled="signupLoading"
        type="text"
        v-model.trim="form.firstName"
        :class="{ 'is-invalid': submitted && v$.form.firstName.$error }"
      />
      <div
        v-if="submitted && v$.form.firstName.$error"
        class="invalid-feedback"
      >
        <span v-if="v$.form.firstName.required.$invalid"
          >Данное поле обязательно</span
        >
      </div>
    </div>
    <div class="form-group">
      <label class="form-name">Отчество</label><br />
      <input
        id="patronymic"
        :disabled="signupLoading"
        type="text"
        v-model.trim="form.patronymic"
        :class="{ 'is-invalid': submitted && v$.form.patronymic.$error }"
      />
    </div>
    <div class="form-group">
      <label class="form-name">Дата рождения</label><br />
      <input
        id="birthdate"
        :disabled="signupLoading"
        type="date"
        v-model="form.birthdate"
        :max="new Date().toISOString().substr(0, 10)"
        :class="{ 'is-invalid': submitted && v$.form.birthdate.$error }"
      />
    </div>
    <div class="form-group">
      <label class="form-name">Город проживания </label><br />
      <select
        id="city"
        v-model="form.city"
        :disabled="signupLoading"
        :class="{ 'is-invalid': submitted && v$.form.city.$error }"
      >
        <option v-for="option in cityList" v-bind:key="option.id">
          {{ option.name }}
        </option>
      </select>
    </div>
    <div class="form-group">
      <label class="form-name">E-mail *</label><br />
      <input
        id="email"
        :disabled="signupLoading"
        type="text"
        v-model.trim="form.email"
        :class="{ 'is-invalid': submitted && v$.form.email.$error }"
      />
      <div v-if="submitted && v$.form.email.$error" class="invalid-feedback">
        <span v-if="v$.form.email.required.$invalid"
          >Данное поле обязательно</span
        >
        <span v-if="v$.form.email.email.$invalid">Некорректный email</span>
      </div>
    </div>
    <div class="form-group">
      <label class="form-name">Пароль *</label><br />
      <input
        id="password"
        :disabled="signupLoading"
        :type="passShow ? 'text' : 'password'"
        v-model="form.password"
        :class="{ 'is-invalid': submitted && v$.form.password.$error }"
      />
      <button @click="passShow = !passShow">Показать/спрятать</button>

      <div v-if="submitted && v$.form.password.$error" class="invalid-feedback">
        <span v-if="v$.form.password.required.$invalid"
          >Данное поле обязательно</span
        >
        <span v-if="v$.form.password.minLength.$invalid"
          >Пароль должен содержать не менее 6 символов</span
        >
      </div>
    </div>
    <div class="form-group">
      <label class="form-name">Повторите пароль *</label><br />
      <input
        id="confirmPassword"
        :disabled="signupLoading"
        :type="passShow2 ? 'text' : 'password'"
        v-model="form.confirmPassword"
        :class="{ 'is-invalid': submitted && v$.form.confirmPassword.$error }"
      />
      <button @click="passShow2 = !passShow2">Показать/спрятать</button>
      <div
        v-if="
          submitted && (v$.form.confirmPassword.$error || !passwordIsSame())
        "
        class="invalid-feedback"
      >
        <span v-if="v$.form.confirmPassword.required.$invalid"
          >Данное поле обязательно</span
        >
        <span v-else-if="passwordIsSame">Пароли не совпадают</span>
      </div>
    </div>
    <div class="form-group">
      <input
        type="checkbox"
        class="custom-checkbox"
        id="personalData"
        :disabled="signupLoading"
        v-model="form.personalData"
        name="personalData"
        :class="{ 'is-invalid': submitted && v$.form.personalData.$error }"
      />
      <label for="personalData"
        >Согласен(на) на обработку персональных данных</label
      >
      <div
        v-if="submitted && v$.form.personalData.$error"
        class="invalid-feedback"
      >
        <span v-if="v$.form.personalData.required.$invalid"
          >Данное поле обязательно</span
        >
      </div>
    </div>
    <p>* - обязательное поле</p>
    <button @click="onSignUp">Зарегистрироваться</button>
    <p>
      Есть аккаунт?
      <router-link tag="a" :to="{ name: 'LogIn' }">Авторизируйся!</router-link>
    </p>
    <p>
      <router-link tag="a" :to="{ name: 'SignUpEmployee' }"
        >Зарегистрироваться как представитель образовательной организации или
        компании</router-link
      >
    </p>
  </div>
</template>

<script>
import useVuelidate from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";
export default {
  name: "Profile",
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      changePassword: false,
      passShow: false,
      passShow2: false,
      form: {
        firstName: "",
        lastName: "",
        patronymic: "",
        birthdate: "",
        email: "",
        password: "",
        confirmPassword: "",
        personalData: "",
      },
      submitted: false,
      signupLoading: false,
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
      password: { required, minLength: minLength(6) },
      confirmPassword: {
        required,
      },
      personalData: { required },
    },
  },
  methods: {
    passwordIsSame() {
      return this.form.password === this.form.confirmPassword;
    },
    onSignUp() {
      this.signupLoading = true;
      this.submitted = true;
      this.v$.$touch();
      this.signupLoading = false;
      if (this.v$.$invalid) return;
      // to form submit after this
      console.log(this.form);
    },
  },
};
</script>

<style lang="scss"></style>
