<template>
  <div>
    <loader v-if="isLoading || organizations == undefined"></loader>
    <div v-else>
      <h1>Регистрация</h1>
      <form>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="lastName" class="form-name">Фамилия *</label><br />
            <input
              id="lastName"
              name="lastName"
              class="form-control"
              :disabled="isLoading"
              type="text"
              v-model.trim="form.lastName"
              :class="{ 'is-invalid': submitted && $v.form.lastName.$error }"
            />
            <p
              v-if="submitted && !$v.form.lastName.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="firstName" class="form-name">Имя *</label><br />
            <input
              name="firstName"
              id="firstName"
              class="form-control"
              :disabled="isLoading"
              type="text"
              v-model.trim="form.firstName"
              :class="{ 'is-invalid': submitted && $v.form.firstName.$error }"
            />
            <p
              v-if="submitted && !$v.form.firstName.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
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
            <div class="is-invalid"></div>
            <p
              v-if="submitted && !$v.form.organization.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="position" class="form-name">Должность</label><br />
            <input
              id="position"
              class="form-control"
              name="position"
              :disabled="isLoading"
              type="text"
              v-model.trim="form.position"
              :class="{ 'is-invalid': submitted && $v.form.position.$error }"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="email" class="form-name">E-mail *</label><br />
            <input
              id="email"
              name="email"
              :disabled="isLoading"
              type="text"
              class="form-control"
              v-model.trim="form.email"
              :class="{ 'is-invalid': submitted && $v.form.email.$error }"
            />
            <p
              v-if="submitted && !$v.form.email.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
            <p
              v-if="submitted && !$v.form.email.email"
              class="invalid-feedback"
            >
              Некорректный email
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="password" class="form-name">Пароль *</label><br />
            <div style="position: relative">
              <input
                style="position: relative"
                id="password"
                class="form-control"
                name="password"
                :disabled="isLoading"
                :type="passShow ? 'text' : 'password'"
                v-model="form.password"
                :class="{ 'is-invalid': submitted && $v.form.password.$error }"
              />
              <p
                v-if="submitted && !$v.form.password.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
              <p
                v-if="submitted && !$v.form.password.minLength"
                class="invalid-feedback"
              >
                Пароль должен содержать не менее 6 символов
              </p>
              <svg
                v-if="!passShow"
                @click="passShow = !passShow"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                style="cursor: pointer"
                fill="currentColor"
                :class="{
                  'd-none':
                    submitted &&
                    (!$v.form.password.required || !$v.form.password.minLength),
                }"
                class="bi bi-eye my-icon-eye"
                viewBox="0 0 16 16"
              >
                <path
                  d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"
                />
                <path
                  d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"
                />
              </svg>
              <svg
                v-if="passShow"
                @click="passShow = !passShow"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                style="cursor: pointer"
                :class="{
                  'd-none':
                    submitted &&
                    (!$v.form.password.required || !$v.form.password.minLength),
                }"
                class="bi bi-eye-slash my-icon-eye"
                viewBox="0 0 16 16"
              >
                <path
                  d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"
                />
                <path
                  d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"
                />
                <path
                  d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="confirmPassword" class="form-name"
              >Повторите пароль *</label
            ><br />
            <div style="position: relative">
              <input
                class="form-control"
                id="confirmPassword"
                name="confirmPassword"
                :disabled="isLoading"
                :type="passShow2 ? 'text' : 'password'"
                v-model="form.confirmPassword"
                :class="{
                  'is-invalid':
                    submitted &&
                    ($v.form.confirmPassword.$error || !passwordIsSame),
                }"
              />
              <p
                v-if="submitted && !$v.form.confirmPassword.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>

              <p
                v-else-if="submitted && !passwordIsSame"
                class="invalid-feedback"
              >
                Пароли не совпадают
              </p>
              <svg
                v-if="!passShow2"
                @click="passShow2 = !passShow2"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                style="cursor: pointer"
                fill="currentColor"
                :class="{
                  'd-none':
                    submitted &&
                    (!$v.form.confirmPassword.required || !passwordIsSame),
                }"
                class="bi bi-eye my-icon-eye"
                viewBox="0 0 16 16"
              >
                <path
                  d="M16 8s-3-5.5-8-5.5S0 8 0 8s3 5.5 8 5.5S16 8 16 8zM1.173 8a13.133 13.133 0 0 1 1.66-2.043C4.12 4.668 5.88 3.5 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.133 13.133 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755C11.879 11.332 10.119 12.5 8 12.5c-2.12 0-3.879-1.168-5.168-2.457A13.134 13.134 0 0 1 1.172 8z"
                />
                <path
                  d="M8 5.5a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM4.5 8a3.5 3.5 0 1 1 7 0 3.5 3.5 0 0 1-7 0z"
                />
              </svg>
              <svg
                v-if="passShow2"
                @click="passShow2 = !passShow2"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                fill="currentColor"
                style="cursor: pointer"
                :class="{
                  'd-none':
                    submitted &&
                    (!$v.form.confirmPassword.required || !passwordIsSame),
                }"
                class="bi bi-eye-slash my-icon-eye"
                viewBox="0 0 16 16"
              >
                <path
                  d="M13.359 11.238C15.06 9.72 16 8 16 8s-3-5.5-8-5.5a7.028 7.028 0 0 0-2.79.588l.77.771A5.944 5.944 0 0 1 8 3.5c2.12 0 3.879 1.168 5.168 2.457A13.134 13.134 0 0 1 14.828 8c-.058.087-.122.183-.195.288-.335.48-.83 1.12-1.465 1.755-.165.165-.337.328-.517.486l.708.709z"
                />
                <path
                  d="M11.297 9.176a3.5 3.5 0 0 0-4.474-4.474l.823.823a2.5 2.5 0 0 1 2.829 2.829l.822.822zm-2.943 1.299.822.822a3.5 3.5 0 0 1-4.474-4.474l.823.823a2.5 2.5 0 0 0 2.829 2.829z"
                />
                <path
                  d="M3.35 5.47c-.18.16-.353.322-.518.487A13.134 13.134 0 0 0 1.172 8l.195.288c.335.48.83 1.12 1.465 1.755C4.121 11.332 5.881 12.5 8 12.5c.716 0 1.39-.133 2.02-.36l.77.772A7.029 7.029 0 0 1 8 13.5C3 13.5 0 8 0 8s.939-1.721 2.641-3.238l.708.709zm10.296 8.884-12-12 .708-.708 12 12-.708.708z"
                />
              </svg>
            </div>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <div class="form-check">
              <input
                class="form-check-input"
                type="checkbox"
                id="personalData"
                :disabled="isLoading"
                v-model="form.personalData"
                name="personalData"
                :class="{
                  'is-invalid': submitted && !$v.form.personalData.$model,
                }"
              />
              <label class="form-check-label" for="personalData">
                Согласен(на) на обработку персональных данных</label
              >
              <p
                v-if="submitted && !$v.form.personalData.$model"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
            </div>
          </div>
        </div>
      </form>
      <p v-if="errorsContain('emailAlreadyExists')" class="errors fs-2">
        Пользователь с указанным email уже существует.
      </p>
      <p v-if="errorsContain('commonError')" class="errors fs-2">
        Произошла ошибка. Повторите попытку позднее.
      </p>
      <p>* - обязательное поле</p>
      <div>
        <button class="text-gradient to-block" @click="onSignUp">
          Зарегистрироваться
          <span class="text">Зарегистрироваться</span>
        </button>
      </div>
      <br />
      <p>
        Есть аккаунт?
        <router-link
          tag="a"
          class="text-decoration-none"
          :to="{ name: 'LogIn' }"
          >Авторизируйтесь!</router-link
        >
      </p>
      <p>
        <router-link
          tag="a"
          class="text-decoration-none"
          :to="{ name: 'SignUp' }"
          >Зарегистрироваться как школьник</router-link
        >
      </p>
    </div>
  </div>
</template>

<script>
import login from "@/graphql/mutations/login.gql";
import jwt from "jsonwebtoken";
import { SHORT_LIST_ORGANIZATIONS } from "@/graphql/queries/queries";
import register from "@/graphql/mutations/register.gql";
import { CREATE_EMPLOYEE } from "@/graphql/mutations/mutations.js";
import { required, email, minLength } from "vuelidate/lib/validators";
import Multiselect from "vue-multiselect";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "SignUpEmployee",
  components: {
    Multiselect,
    Loader,
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
      errors: [],
    };
  },
  computed: {
    passwordIsSame() {
      return this.form.password === this.form.confirmPassword;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
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
    onLogin() {
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({
          mutation: login,
          variables: {
            email: this.form.email,
            password: this.form.password,
          },
        })
        .then((data) => {
          localStorage.setItem("token", data.data.login.token);
          let objJWT = jwt.decode(data.data.login.token);
          this.$store.commit("SET_IS_AUTHENTICATED", true);
          this.$store.commit("SET_GOT_VERIFIED_AUTH", true);
          this.$store.commit("SET_USER_ID", objJWT.user_id);
          this.$store.commit("SET_ORGANIZER", objJWT.is_organizer);
          this.$store.commit("MODERATE_ORGANIZER", false);
          this.$store.commit("SET_STUDENT", objJWT.is_student);
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
          this.$router.push({ name: "OrganizationOlympiads" });
        })
        .catch((error) => {
          console.log("error", error);
        })
        .finally(() => {
          this.$store.commit("STOP_LOADING");
        });
    },
    createEmployee(userId) {
      this.$store.commit("START_LOADING");
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
          this.onLogin();
        })
        .catch((error) => {
          console.error(error);
        })
        .finally(() => {
          this.$store.commit("STOP_LOADING");
        });
    },

    onSignUp() {
      this.submitted = true;
      this.$v.$touch();
      if (this.$v.form.$invalid) {
        return;
      }
      this.$store.commit("START_LOADING");
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
          if (this.isSuccess) {
            this.createEmployee(result.data.register.user.id);
          }
        })
        .catch((error) => {
          console.log("error", error);
          this.errors = ["commonError"];
        })
        .finally(() => {
          this.$store.commit("STOP_LOADING");
        });
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss">
.errors {
  color: #dc3545;
}

div svg.my-icon-eye {
  position: absolute;
  right: 11px;
  top: 11px;
}

.form-row .form-group .multiselect__select {
  top: 3px;
}

.form-row .form-group .multiselect__tags {
  border: 1px solid #ced4da;
  color: #495057;
  font-weight: 400;
}
</style>
