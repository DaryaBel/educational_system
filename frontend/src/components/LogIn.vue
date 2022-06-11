<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>

    <div v-else>
      <h1>Авторизация</h1>
      <form>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="email" class="form-name">E-mail *</label><br />
            <input
              id="email"
              name="email"
              :disabled="isLoading"
              type="text"
              v-model.trim="form.email"
              class="form-control"
              :class="{ 'is-invalid': submitted && $v.form.email.$error }"
            />
            <p
              v-if="submitted && !$v.form.email.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label for="password" class="form-name">Пароль *</label><br />
            <div style="position: relative">
              <input
                class="form-control"
                id="password"
                name="password"
                :disabled="isLoading"
                :type="passShow ? 'text' : 'password'"
                v-model="form.password"
                :class="{ 'is-invalid': submitted && $v.form.password.$error }"
              />
              <svg
                v-if="!passShow"
                @click="passShow = !passShow"
                xmlns="http://www.w3.org/2000/svg"
                width="16"
                height="16"
                style="cursor: pointer"
                fill="currentColor"
                :class="{ 'd-none': submitted && !$v.form.password.required }"
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
                :class="{ 'd-none': submitted && !$v.form.password.required }"
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

            <p
              v-if="submitted && !$v.form.password.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
      </form>

      <p v-if="errors" class="errors fs-2">Неправильный логин или пароль!</p>

      <p>* - обязательное поле</p>
      <div>
        <button class="text-gradient" @click="onLogin">
          Войти
          <span class="text">Войти</span>
        </button>
      </div>
      <br />
      <p>
        Нет аккаунта?
        <router-link
          tag="a"
          :to="{ name: 'SignUp' }"
          class="text-decoration-none"
          >Зарегистрируйся!</router-link
        >
      </p>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import { required } from "vuelidate/lib/validators";
import login from "@/graphql/mutations/login.gql";
export default {
  name: "LogIn",
  data() {
    return {
      passShow: false,
      form: {
        email: "",
        password: "",
      },
      submitted: false,
      errors: false,
    };
  },
  validations: {
    form: {
      email: {
        required,
      },
      password: {
        required,
      },
    },
  },
  computed: {
    isLoading() {
      return this.$store.state.isLoading;
    },
  },
  methods: {
    onLogin() {
      this.submitted = true;
      this.$v.$touch();
      if (this.$v.form.$invalid) {
        return;
      }
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
          this.$store.commit("MODERATE_ORGANIZER", objJWT.moderated);
          this.$store.commit("SET_STUDENT", objJWT.is_student);
          if (objJWT.is_organizer)
            this.$router.push({ name: "OrganizationOlympiads" });
          if (objJWT.is_student) this.$router.push({ name: "OlympiadList" });
        })
        .catch((error) => {
          console.log("error", error);
          this.errors = true;
        })
        .finally(() => {
          this.$store.commit("STOP_LOADING");
        });
    },
  },
};
</script>

<style lang="scss">
.errors {
  color: #dc3545;
}

div svg.my-icon-eye {
  position: absolute;
  right: 11px;
  top: 11px;
}
</style>
