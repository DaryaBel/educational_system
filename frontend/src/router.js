import Vue from "vue";
import VueRouter from "vue-router";
import { createProvider } from "@/apollo";

import SignUp from "@/components/SignUp.vue";
import SignUpEmployee from "@/components/SignUpEmployee.vue";
import LogIn from "@/components/LogIn.vue";
import Profile from "@/components/Profile.vue";
import DeleteAccount from "@/components/DeleteAccount.vue";

import CourseList from "@/components/course/CourseList.vue";
import Course from "@/components/course/Course.vue";
import StudentCourses from "@/components/course/StudentCourses.vue";
import OrganizationCourses from "@/components/course/organizers/OrganizationCourses.vue";
import OrganizationCourse from "@/components/course/organizers/OrganizationCourse.vue";
import NewCourse from "@/components/course/organizers/NewCourse.vue";
import CourseMembers from "@/components/course/organizers/CourseMembers.vue";

import OlympiadList from "@/components/olympiad/OlympiadList.vue";
import Olympiad from "@/components/olympiad/Olympiad.vue";
import OlympiadRules from "@/components/olympiad/OlympiadRules.vue";
import OlympiadProcess from "@/components/olympiad/OlympiadProcess.vue";
import OlympiadResult from "@/components/olympiad/OlympiadResult.vue";
import StudentOlympiads from "@/components/olympiad/StudentOlympiads.vue";
import OrganizationOlympiads from "@/components/olympiad/organizers/OrganizationOlympiads.vue";
import OrganizationOlympiad from "@/components/olympiad/organizers/OrganizationOlympiad.vue";
import NewOlympiad from "@/components/olympiad/organizers/NewOlympiad.vue";
import OlympiadMembers from "@/components/olympiad/organizers/OlympiadMembers.vue";
import StudentAnswers from "@/components/olympiad/organizers/StudentAnswers.vue";

import store from "@/store.js";
import verifyToken from "@/graphql/mutations/verifyToken.gql";

function verifyAuth(to, from) {
  store.commit("START_LOADING");
  let provider = createProvider();
  return new Promise(function (resolve, reject) {
    provider.defaultClient
      // из локаласторджа кладем и передаем токен
      .mutate({ mutation: verifyToken })
      .then((result) => {
        let userId = result.data.verifyToken.payload.user_id;
        store.commit("SET_USER_ID", userId);
        store.commit("SET_IS_AUTHENTICATED", true);
      })
      .catch((error) => {
        store.commit("SET_IS_AUTHENTICATED", false);
      })
      .finally(() => {
        store.commit("SET_GOT_VERIFIED_AUTH", true);
        store.commit("STOP_LOADING");
        resolve();
      });
  });
}

const ifAuthenticated = async (to, from, next) => {
  try {
    if (!store.state.gotVerifiedAuth) {
      await verifyAuth(to, from);
    }
    if (store.state.isAuthenticated) {
      next();
      return;
    }
    next("/login");
  } catch (error) {
    console.log("ERROR TEST: ", error);
  }
};

const ifNotAuthenticated = async (to, from, next) => {
  try {
    if (!store.state.gotVerifiedAuth) {
      await verifyAuth(to, from);
    }
    if (!store.state.isAuthenticated) {
      next();
      return;
    }
    next("/olympiads");
  } catch (error) {
    console.log("ERROR TEST: ", error);
  }
};

const isOrganizer = async (to, from, next) => {
  try {
    if (!store.state.gotVerifiedAuth) {
      await verifyAuth(to, from);
    }
    if (store.state.isOrganizer) {
      next();
      return;
    }
    next("/olympiads");
  } catch (error) {
    console.log("ERROR TEST: ", error);
  }
};

const isStudent = async (to, from, next) => {
  try {
    if (!store.state.gotVerifiedAuth) {
      await verifyAuth(to, from);
    }
    if (store.state.isStudent) {
      next();
      return;
    }
    next("/organization/olympiads");
  } catch (error) {
    console.log("ERROR TEST: ", error);
  }
};

const routes = [
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
    beforeEnter: ifNotAuthenticated,
    meta: { title: "Зарегистрироваться - Пора!" },
  },
  {
    path: "/signup/employee",
    name: "SignUpEmployee",
    component: SignUpEmployee,
    beforeEnter: ifNotAuthenticated,
    meta: { title: "Зарегистрироваться как организатор - Пора!" },
  },
  {
    path: "/login",
    name: "LogIn",
    component: LogIn,
    beforeEnter: ifNotAuthenticated,
    meta: { title: "Войти - Пора!" },
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
    beforeEnter: ifAuthenticated,
    meta: { title: "Личный кабинет - Пора!" },
  },
  {
    path: "/profile/delete-account",
    name: "DeleteAccount",
    component: DeleteAccount,
    beforeEnter: ifAuthenticated,
    meta: { title: "Удалить аккаунт - Пора!" },
  },

  // КУРСЫ

  {
    path: "/courses",
    name: "CourseList",
    component: CourseList,
    meta: { title: "Курсы - Пора!" },
  },
  {
    path: "/courses/:id",
    name: "Course",
    component: Course,
    beforeEnter: ifAuthenticated,
    meta: { title: "Курс - Пора!" },
  },
  {
    path: "/my/courses",
    name: "StudentCourses",
    component: StudentCourses,
    beforeEnter: [ifAuthenticated, isStudent],
    meta: { title: "Мои курсы - Пора!" },
  },
  {
    path: "/organization/courses",
    name: "OrganizationCourses",
    component: OrganizationCourses,
    beforeEnter: ifAuthenticated,
    isOrganizer,
    meta: { title: "Курсы организации - Пора!" },
  },
  {
    path: "/organization/courses/:id",
    name: "OrganizationCourse",
    component: OrganizationCourse,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Курс организации - Пора!" },
  },
  {
    path: "/organization/courses/:id/members",
    name: "CourseMembers",
    component: CourseMembers,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Записавшиеся на курс - Пора!" },
  },
  {
    path: "/organization/courses/new",
    name: "NewCourse",
    component: NewCourse,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Новый курс - Пора!" },
  },

  // ОЛИМПИАДЫ
  {
    path: "/olympiads",
    name: "OlympiadList",
    component: OlympiadList,
    meta: { title: "Олимпиады - Пора!" },
  },
  {
    path: "/olympiads/:id",
    name: "Olympiad",
    component: Olympiad,
    beforeEnter: ifAuthenticated,
    meta: { title: "Олимпиада - Пора!" },
  },
  {
    path: "/olympiads/:id/rules",
    name: "OlympiadRules",
    component: OlympiadRules,
    beforeEnter: [ifAuthenticated, isStudent],
    meta: { title: "Правила олимпиады - Пора!" },
  },
  {
    path: "/olympiads/:id/start",
    name: "OlympiadProcess",
    component: OlympiadProcess,
    beforeEnter: [ifAuthenticated, isStudent],
    meta: { title: "Олимпиада - Пора!" },
  },
  {
    path: "/olympiads/:id/result",
    name: "OlympiadResult",
    component: OlympiadResult,
    beforeEnter: [ifAuthenticated, isStudent],
    meta: { title: "Результаты олимпиады - Пора!" },
  },
  {
    path: "/my/olympiads",
    name: "StudentOlympiads",
    component: StudentOlympiads,
    beforeEnter: [ifAuthenticated, isStudent],
    meta: { title: "Мои олимпиады - Пора!" },
  },
  {
    path: "/organization/olympiads",
    name: "OrganizationOlympiads",
    component: OrganizationOlympiads,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Олимпиады организации - Пора!" },
  },
  {
    path: "/organization/olympiads/:id",
    name: "OrganizationOlympiad",
    component: OrganizationOlympiad,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Олимпиада - Пора!" },
  },

  {
    path: "/organization/olympiads/:id/members",
    name: "OlympiadMembers",
    component: OlympiadMembers,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Участники олимпиады - Пора!" },
  },
  {
    path: "/organization/olympiads/:id/members/:user/answers",
    name: "StudentAnswers",
    component: StudentAnswers,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Решения школьника - Пора!" },
  },
  {
    path: "/organization/olympiads/new",
    name: "NewOlympiad",
    component: NewOlympiad,
    beforeEnter: [ifAuthenticated, isOrganizer],
    meta: { title: "Новая олимпиада - Пора!" },
  },
];

Vue.use(VueRouter);
const router = new VueRouter({
  scrollBehavior(to, from, savedPosition) {
    return { x: 0, y: 0 };
  },
  mode: "history",
  routes,
});

export default router;
