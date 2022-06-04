<template>
  <div>
    <div v-if="isLoading || organizations == undefined">Загрузка...</div>
    <div v-else>
      <h1>
        Регистрация для представителей компаний и образовательных организаций
      </h1>
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
          name="firstName"
          id="firstName"
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
        <label class="form-name">Организация *</label><br />
        <multiselect
          :disabled="isLoading"
          v-model="form.organization"
          track-by="id"
          label="fullname"
          placeholder="Выберите организацию"
          :options="organizationsOption"
          :showLabels="false"
          :searchable="true"
          :close-on-select="true"
          :allow-empty="false"
          :showPointer="false"
        >
          <span slot="noResult">Не найдено</span>
        </multiselect>

        <div
          v-if="submitted && $v.form.organization.$error"
          class="invalid-feedback"
        >
          <span v-if="!$v.form.organization.required"
            >Данное поле обязательно</span
          >
        </div>
      </div>
      <div class="form-group">
        <label for="position" class="form-name">Должность</label><br />
        <input
          id="position"
          name="position"
          :disabled="isLoading"
          type="text"
          v-model.trim="form.position"
          :class="{ 'is-invalid': submitted && $v.form.position.$error }"
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
          >Авторизируйтесь!</router-link
        >
      </p>
      <p>
        <router-link tag="a" :to="{ name: 'SignUp' }"
          >Зарегистрироваться как школьник</router-link
        >
      </p>
    </div>
  </div>
</template>

<script>
import { SHORT_LIST_ORGANIZATIONS } from "@/graphql/queries/queries";
import register from "@/graphql/mutations/register.gql";
import { CREATE_EMPLOYEE } from "@/graphql/mutations/mutations.js";
import { required, email, minLength } from "vuelidate/lib/validators";
import Multiselect from "vue-multiselect";
export default {
  name: "SignUpEmployee",
  components: {
    Multiselect,
  },
  apollo: {
    organizations: {
      query: SHORT_LIST_ORGANIZATIONS,
    },
  },
  data() {
    return {
      isSuccess: false,
      passShow: false,
      passShow2: false,
      form: {
        firstName: undefined,
        lastName: undefined,
        position: undefined,
        organization: undefined,
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
  computed: {
    organizationsOption() {
      if (this.organizations == undefined) return [];
      else return this.organizations;
    },
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
    errorsContain(error) {
      if (this.errors != null) return this.errors.includes(error);
      else return false;
    },
    createEmployee(userId) {
      this.$apollo
        .mutate({
          mutation: CREATE_EMPLOYEE,
          variables: {
            userId: userId,
            organizationId: this.form.organization.id,
            position: this.form.position,
          },
        })
        .then(() => {
          this.isLoading = false;
          this.form = {
            firstName: undefined,
            lastName: undefined,
            position: undefined,
            organization: undefined,
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
    passwordIsSame() {
      return this.form.password === this.form.confirmPassword;
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
            this.createEmployee(result.data.register.user.id);
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

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
