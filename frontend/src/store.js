import Vue from "vue";
import Vuex from "vuex";

Vue.use(Vuex);

const store = new Vuex.Store({
  strict: true,
  state: {
    isStudent: false,
    isOrganizer: false,
    userId: false,
    isAuthenticated: false,
    isLoading: false,
    gotVerifiedAuth: false,
  },
  mutations: {
    START_LOADING(state) {
      state.isLoading = true;
    },
    STOP_LOADING(state) {
      state.isLoading = false;
    },
    SET_IS_AUTHENTICATED(state, boolean) {
      state.isAuthenticated = boolean;
    },
    SET_GOT_VERIFIED_AUTH(state, boolean) {
      state.gotVerifiedAuth = boolean;
    },
    SET_USER_ID(state, userId) {
      state.userId = userId;
    },
    SET_STUDENT(state, boolean) {
      state.isStudent = boolean;
    },
    SET_ORGANIZER(state, boolean) {
      state.isOrganizer = boolean;
    },
  },
  actions: {},
});

export default store;
