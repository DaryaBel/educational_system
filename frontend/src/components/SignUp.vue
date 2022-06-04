<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else>
      <h1>Регистрация</h1>
      <div class="form-group">
        <label for="lastName" class="form-name">Фамилия *</label><br />
        <input
          id="lastName"
          name="lastName"
          :disabled="isLoading"
          type="text"
          v-model.trim="form.lastName"
          :class="{ 'is-invalid': submitted && $v.form.lastName.$error }"
        />
        <div
          v-if="submitted && $v.form.lastName.$error"
          class="invalid-feedback"
        >
          <span v-if="!$v.form.lastName.required">Данное поле обязательно</span>
        </div>
      </div>
      <div class="form-group">
        <label for="firstName" class="form-name">Имя *</label><br />
        <input
          id="firstName"
          name="firstName"
          :disabled="isLoading"
          type="text"
          v-model.trim="form.firstName"
          :class="{ 'is-invalid': submitted && $v.form.firstName.$error }"
        />
        <div
          v-if="submitted && $v.form.firstName.$error"
          class="invalid-feedback"
        >
          <span v-if="!$v.form.firstName.required"
            >Данное поле обязательно</span
          >
        </div>
      </div>
      <div class="form-group">
        <label for="patronymic" class="form-name">Отчество</label><br />
        <input
          id="patronymic"
          name="patronymic"
          :disabled="isLoading"
          type="text"
          v-model.trim="form.patronymic"
          :class="{ 'is-invalid': submitted && $v.form.patronymic.$error }"
        />
      </div>
      <div class="form-group">
        <label for="birthdate" class="form-name">Дата рождения</label><br />
        <input
          id="birthdate"
          name="birthdate"
          :disabled="isLoading"
          type="date"
          v-model="form.birthdate"
          :max="new Date().toISOString().substr(0, 10)"
          :class="{ 'is-invalid': submitted && $v.form.birthdate.$error }"
        />
      </div>
      <div class="form-group">
        <label for="email" class="form-name">E-mail *</label><br />
        <input
          id="email"
          name="email"
          :disabled="isLoading"
          type="text"
          v-model.trim="form.email"
          :class="{ 'is-invalid': submitted && $v.form.email.$error }"
        />
        <div v-if="submitted && $v.form.email.$error" class="invalid-feedback">
          <span v-if="!$v.form.email.required">Данное поле обязательно</span>
          <span v-if="!$v.form.email.email">Некорректный email</span>
        </div>
      </div>
      <div class="form-group">
        <label for="password" class="form-name">Пароль *</label><br />
        <input
          id="password"
          name="password"
          :disabled="isLoading"
          :type="passShow ? 'text' : 'password'"
          v-model="form.password"
          :class="{ 'is-invalid': submitted && $v.form.password.$error }"
        />
        <button @click="passShow = !passShow">Показать/спрятать</button>

        <div
          v-if="submitted && $v.form.password.$error"
          class="invalid-feedback"
        >
          <span v-if="!$v.form.password.required">Данное поле обязательно</span>
          <span v-if="$v.form.password.minLength.$invalid"
            >Пароль должен содержать не менее 6 символов</span
          >
        </div>
      </div>
      <div class="form-group">
        <label for="confirmPassword" class="form-name">Повторите пароль *</label
        ><br />
        <input
          id="confirmPassword"
          name="confirmPassword"
          :disabled="isLoading"
          :type="passShow2 ? 'text' : 'password'"
          v-model="form.confirmPassword"
          :class="{ 'is-invalid': submitted && $v.form.confirmPassword.$error }"
        />
        <button @click="passShow2 = !passShow2">Показать/спрятать</button>
        <div
          v-if="
            submitted && ($v.form.confirmPassword.$error || !passwordIsSame())
          "
          class="invalid-feedback"
        >
          <span v-if="!$v.form.confirmPassword.required"
            >Данное поле обязательно</span
          >
          <span v-else-if="!passwordIsSame()">Пароли не совпадают</span>
        </div>
      </div>
      <div class="form-group">
        <input
          type="checkbox"
          class="custom-checkbox"
          id="personalData"
          :disabled="isLoading"
          v-model="form.personalData"
          name="personalData"
          :class="{ 'is-invalid': submitted && $v.form.personalData.$error }"
        />
        <label for="personalData"
          >Согласен(на) на обработку персональных данных</label
        >
        <div
          v-if="submitted && $v.form.personalData.$error"
          class="invalid-feedback"
        >
          <span v-if="!$v.form.personalData.required"
            >Данное поле обязательно</span
          >
        </div>
      </div>
      <div class="errors">
        <div class="error-message" v-if="errorsContain('emailAlreadyExists')">
          Пользователь с указанным email уже существует.
        </div>
        <div class="error-message" v-if="errorsContain('commonError')">
          Произошла ошибка. Повторите попытку позднее.
        </div>
      </div>
      <p>* - обязательное поле</p>
      <button @click="onSignUp">Зарегистрироваться</button>
      <p>
        Есть аккаунт?
        <router-link tag="a" :to="{ name: 'LogIn' }"
          >Авторизируйся!</router-link
        >
      </p>
      <p>
        <router-link tag="a" :to="{ name: 'SignUpEmployee' }"
          >Зарегистрироваться как представитель образовательной организации или
          компании</router-link
        >
      </p>
    </div>
  </div>
</template>

<script>
import register from "@/graphql/mutations/register.gql";
import { CREATE_STUDENT } from "@/graphql/mutations/mutations.js";
import { required, email, minLength } from "vuelidate/lib/validators";
export default {
  name: "SignUp",
  data() {
    return {
      isSuccess: false,
      passShow: false,
      passShow2: false,
      form: {
        firstName: undefined,
        lastName: undefined,
        patronymic: undefined,
        birthdate: undefined,
        email: undefined,
        password: undefined,
        confirmPassword: undefined,
        personalData: undefined,
      },
      submitted: false,
      isLoading: false,
      errors: [],
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
    errorsContain(error) {
      if (this.errors != null) return this.errors.includes(error);
      else return false;
    },
    passwordIsSame() {
      return this.form.password === this.form.confirmPassword;
    },
    createStudent(userId) {
      this.$apollo
        .mutate({
          mutation: CREATE_STUDENT,
          variables: {
            userId: userId,
            patronymic: this.form.patronymic,
            birthdate: this.form.birthdate,
          },
        })
        .then(() => {
          this.isLoading = false;
          this.form = {
            firstName: undefined,
            lastName: undefined,
            patronymic: undefined,
            birthdate: undefined,
            email: undefined,
            password: undefined,
            confirmPassword: undefined,
            personalData: undefined,
          };
          this.$router.push({
            name: "LogIn",
          });
        })
        .catch((error) => {
          console.error(error);
        });
    },
    onSignUp() {
      this.isLoading = true;
      this.submitted = true;
      this.$v.$touch();
      if (this.$v.form.$invalid) {
        this.isLoading = false;
        return;
      }
      this.$apollo
        .mutate({
          mutation: register,
          variables: {
            lastName: this.form.lastName,
            firstName: this.form.firstName,
            email: this.form.email,
            password: this.form.password,
          },
        })
        .then((result) => {
          this.isSuccess = result.data.register.success;
          this.errors = result.data.register.errors;
          this.isLoading = false;
          if (this.isSuccess) {
            this.createStudent(result.data.register.user.id);
          }
        })
        .catch((error) => {
          console.log("error", error);
          this.errors = ["commonError"];
        });
    },
  },
};
</script>

<style lang="scss">
input[type="checkbox"]:checked,
input[type="checkbox"]:not(:checked) {
  position: absolute;
  left: -9999px;
}

input[type="checkbox"]:checked + label,
input[type="checkbox"]:not(:checked) + label {
  display: inline-block;
  position: relative;
  padding-left: 28px;
  line-height: 20px;
}

input[type="checkbox"]:checked + label:before,
input[type="checkbox"]:not(:checked) + label:before {
  content: "";
  position: absolute;
  left: 0px;
  top: 0px;
  width: 18px;
  height: 18px;
  border: 1px solid rgb(118, 118, 118);
  border-radius: 3px;
  background-color: white;
}

input[type="checkbox"]:checked + label:after,
input[type="checkbox"]:not(:checked) + label:after {
  content: "";
  position: absolute;
  -webkit-transition: all 0.2s ease;
  -moz-transition: all 0.2s ease;
  -o-transition: all 0.2s ease;
  transition: all 0.2s ease;
}

input[type="checkbox"]:checked + label:after,
input[type="checkbox"]:not(:checked) + label:after {
  left: 4px;
  top: 5px;
  width: 9px;
  height: 4px;
  border-left: 3px solid #13a2ff;
  border-bottom: 3px solid #13a2ff;
  -webkit-transform: rotate(-45deg);
  -moz-transform: rotate(-45deg);
  -o-transform: rotate(-45deg);
  -ms-transform: rotate(-45deg);
  transform: rotate(-45deg);
}

input[type="checkbox"]:not(:checked) + label:after {
  opacity: 0;
}

input[type="checkbox"]:checked + label:after {
  opacity: 1;
}
</style>
