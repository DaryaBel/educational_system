<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-else>
      <h1>Авторизация</h1>
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
        <p v-if="submitted && !$v.form.email.required" class="invalid-feedback">
          Данное поле обязательно
        </p>
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
        <p
          v-if="submitted && !$v.form.password.required"
          class="invalid-feedback"
        >
          Данное поле обязательно
        </p>
      </div>
      <div class="errors">
        <div class="error-message" v-if="errors">
          Неправильный логин или пароль
        </div>
      </div>
      <p>* - обязательное поле</p>
      <button @click="onLogin">Войти</button>
      <p>
        Нет аккаунта?
        <router-link tag="a" :to="{ name: 'SignUp' }"
          >Зарегистрируйся!</router-link
        >
      </p>
      <a href="/admin">Административная панель</a>
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
.is-invalid {
  border-color: red;
}
.invalid-feedback {
  color: red;
}
</style>
