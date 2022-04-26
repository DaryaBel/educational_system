<template>
  <div>
    <h1>
      Регистрация для представителей компаний и образовательных организаций
    </h1>
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
      <label class="form-name">Организация *</label><br />
      <select
        id="organization"
        v-model="form.organization"
        :disabled="signupLoading"
        :class="{ 'is-invalid': submitted && v$.form.organization.$error }"
      >
        <option v-for="option in organizationList" v-bind:key="option.id">
          {{ option.fullname }}
        </option>
      </select>
      <div
        v-if="submitted && v$.form.organization.$error"
        class="invalid-feedback"
      >
        <span v-if="v$.form.organization.required.$invalid"
          >Данное поле обязательно</span
        >
      </div>
    </div>
    <div class="form-group">
      <label class="form-name">Должность</label><br />
      <input
        id="position"
        :disabled="signupLoading"
        type="text"
        v-model.trim="form.position"
        :class="{ 'is-invalid': submitted && v$.form.position.$error }"
      />
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
      <router-link tag="a" :to="{ name: 'LogIn' }"
        >Авторизируйтесь!</router-link
      >
    </p>
    <p>
      <router-link tag="a" :to="{ name: 'SignUp' }"
        >Зарегистрироваться как школьник</router-link
      >
    </p>
  </div>
</template>

<script>
import useVuelidate from "@vuelidate/core";
import { required, email, minLength } from "@vuelidate/validators";
export default {
  name: "SignUpEmployee",
  setup() {
    return { v$: useVuelidate() };
  },
  data() {
    return {
      passShow: false,
      passShow2: false,
      form: {
        firstName: "",
        lastName: "",
        position: "",
        organization: "",
        email: "",
        password: "",
        confirmPassword: "",
        personalData: "",
      },
      submitted: false,
      signupLoading: false,
      organizationList: [
        { fullname: "Один", id: "1" },
        { fullname: "Два", id: "2" },
        { fullname: "Три", id: "5" },
      ],
    };
  },
  validations: {
    form: {
      firstName: { required },
      lastName: { required },
      position: {},
      organization: { required },
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

<style lang="scss" scoped></style>
