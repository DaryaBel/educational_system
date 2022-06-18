<template>
  <header>
    <div
      class="d-flex flex-column flex-md-row align-items-center justify-content-between pb-3 mb-5 mt-1"
      style="margin-bottom: 5rem !important"
    >
      <router-link tag="a" :to="{ name: 'OlympiadList' }">
        <img src="@/assets/logo.png" alt="Пора!" />
      </router-link>

      <nav class="d-inline-flex mt-2 mt-md-0 ms-md-auto align-items-center">
        <router-link
          tag="a"
          :to="{ name: 'CourseList' }"
          class="me-3 py-2 text-dark text-decoration-none mr-5 fs-4"
        >
          Курсы
        </router-link>
        <router-link
          tag="a"
          :to="{ name: 'OlympiadList' }"
          class="me-3 py-2 text-dark text-decoration-none mr-5 fs-4"
        >
          Олимпиады
        </router-link>
        <router-link
          v-if="!isAuthenticated"
          tag="a"
          :to="{ name: 'LogIn' }"
          class="me-3 py-2 text-dark text-decoration-none fs-4"
        >
          Войти
        </router-link>
        <div v-if="isAuthenticated" class="btn-group">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            fill="currentColor"
            viewBox="0 0 16 16"
            class="bi bi-person"
            @click="click()"
            dropdownClose
          >
            <path
              d="M8 8a3 3 0 1 0 0-6 3 3 0 0 0 0 6zm2-3a2 2 0 1 1-4 0 2 2 0 0 1 4 0zm4 8c0 1-1 1-1 1H3s-1 0-1-1 1-4 6-4 6 3 6 4zm-1-.004c-.001-.246-.154-.986-.832-1.664C11.516 10.68 10.289 10 8 10c-2.29 0-3.516.68-4.168 1.332-.678.678-.83 1.418-.832 1.664h10z"
            />
          </svg>
          <ul v-if="dropdown" @click="close()" class="my-dropdown">
            <li>
              <router-link
                tag="a"
                :to="{ name: 'Profile' }"
                class="pb-2 border-bottom px-3 d-block text-dark text-decoration-none fs-4"
              >
                Профиль
              </router-link>
            </li>

            <li v-if="isStudent">
              <router-link
                tag="a"
                :to="{ name: 'StudentCourses' }"
                class="pb-2 border-bottom pt-2 px-3 d-block text-dark text-decoration-none fs-4"
              >
                Мои курсы
              </router-link>
            </li>
            <li v-if="isStudent">
              <router-link
                tag="a"
                :to="{ name: 'StudentOlympiads' }"
                class="pb-2 border-bottom pt-2 px-3 d-block text-dark text-decoration-none fs-4"
              >
                Мои олимпиады
              </router-link>
            </li>
            <li v-if="isOrganizer">
              <router-link
                tag="a"
                :to="{ name: 'OrganizationCourses' }"
                class="pb-2 border-bottom pt-2 px-3 d-block text-dark text-decoration-none fs-4"
              >
                Курсы организации
              </router-link>
            </li>
            <li v-if="isOrganizer">
              <router-link
                tag="a"
                :to="{ name: 'OrganizationOlympiads' }"
                class="pb-2 border-bottom pt-2 px-3 d-block text-dark text-decoration-none fs-4"
              >
                Олимпиады организации
              </router-link>
            </li>
            <li>
              <span
                class="pt-2 px-3 d-block text-dark fs-4 pointer"
                style="cursor: pointer"
                @click="logOut"
                >Выйти</span
              >
            </li>
          </ul>
        </div>
      </nav>
    </div>
  </header>
</template>

<script>
import logout from "@/graphql/mutations/logout.gql";
export default {
  name: "Topbar",
  data() {
    return {
      dropdown: false,
    };
  },
  computed: {
    isAuthenticated() {
      return this.$store.state.isAuthenticated;
    },
    isOrganizer() {
      return this.$store.state.isOrganizer;
    },
    isStudent() {
      return this.$store.state.isStudent;
    },
  },
  methods: {
    logOut() {
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({ mutation: logout })
        .then(() => {
          localStorage.removeItem("token");
          this.$store.commit("SET_IS_AUTHENTICATED", false);
          this.$store.commit("SET_USER_ID", 0);
          this.$store.commit("SET_ORGANIZER", false);
          this.$store.commit("MODERATE_ORGANIZER", false);
          this.$store.commit("SET_STUDENT", false);
          this.$router.push({ name: "LogIn" });
          this.$store.commit("STOP_LOADING");
        })
        .catch(() => {});
    },
    click() {
      this.dropdown = !this.dropdown;
    },
    close() {
      this.dropdown = false;
    },
  },
  mounted() {
    document.addEventListener("click", (e) => {
      if (!e.target.closest("[dropdownClose]") && this.dropdown) {
        this.dropdown = false;
      }
    });
  },
};
</script>

<style lang="scss" scoped>
.text-dark {
  color: #1a1a1a !important;
}

header .d-flex a img {
  height: 64px;
  display: block;
}

nav.d-inline-flex svg {
  width: 22px;
  height: 22px;
  cursor: pointer;
}

.btn-group ul.my-dropdown {
  position: absolute;
  top: 100%;
  right: 0;
  z-index: 1000;
  min-width: 10rem;
  padding: 0.5rem 0;
  margin: 0.125rem 0 0;
  font-size: 1rem;
  color: #1a1a1a;
  text-align: left;
  list-style: none;
  background-color: #fff;
  background-clip: padding-box;
  border: 1px solid rgba(0, 0, 0, 0.15);
  border-radius: 0.25rem;
}
</style>
