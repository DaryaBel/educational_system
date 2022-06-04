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
      isLoading: false,
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
  methods: {
    onLogin() {
      this.isLoading = true;
      this.submitted = true;
      this.$v.$touch();
      if (this.$v.form.$invalid) {
        this.isLoading = false;
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
          this.$store.commit("SET_IS_AUTHENTICATED", true);
          this.$store.commit("SET_GOT_VERIFIED_AUTH", true);
          this.$router.push({ name: "OlympiadList" });
        })
        .catch((error) => {
          console.log("error", error);
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
