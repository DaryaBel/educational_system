<template>
  <div>
    <h1>Авторизация</h1>
    <div class="form-group">
      <label class="form-name">E-mail *</label><br />
      <input
        id="email"
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
      <label class="form-name">Пароль *</label><br />
      <input
        id="password"
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
</template>

<script>
import { required } from "vuelidate/lib/validators";
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
      this.submitted = true;
      this.$v.$touch();
      if (this.$v.$invalid) return;
      // to form submit after this
      console.log(this.form);
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
