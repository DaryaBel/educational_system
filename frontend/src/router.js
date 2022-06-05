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
      .mutate({
        mutation: verifyToken,
        variables: {
          token: localStorage.getItem("token"),
        },
      })
      .then((result) => {
        let userId = result.data.verifyToken.payload.user_id;
        let isStudent = result.data.verifyToken.payload.is_student;
        let isOrganizer = result.data.verifyToken.payload.is_organizer;
        store.commit("SET_USER_ID", userId);
        store.commit("SET_ORGANIZER", isOrganizer);
        store.commit("SET_STUDENT", isStudent);
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

const ifAuthenticatedStudent = async (to, from, next) => {
  try {
    if (!store.state.gotVerifiedAuth) {
      await verifyAuth(to, from);
    }
    if (store.state.isAuthenticated && store.state.isStudent) {
      next();
      return;
    } else if (store.state.isAuthenticated) {
      next("/olympiads");
      return;
    }
    next("/login");
  } catch (error) {
    console.log("ERROR TEST: ", error);
  }
};

const ifAuthenticatedOrganizer = async (to, from, next) => {
  try {
    if (!store.state.gotVerifiedAuth) {
      await verifyAuth(to, from);
    }
    if (store.state.isAuthenticated && store.state.isOrganizer) {
      next();
      return;
    } else if (store.state.isAuthenticated) {
      next("/olympiads");
      return;
    }
    next("/login");
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
    // beforeEnter: ifNotAuthenticated,
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
    beforeEnter: ifAuthenticatedStudent,
    meta: { title: "Мои курсы - Пора!" },
  },
  {
    path: "/organization/courses",
    name: "OrganizationCourses",
    component: OrganizationCourses,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Курсы организации - Пора!" },
  },
  {
    path: "/organization/courses/:id",
    name: "OrganizationCourse",
    component: OrganizationCourse,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Курс организации - Пора!" },
  },
  {
    path: "/organization/courses/:id/members",
    name: "CourseMembers",
    component: CourseMembers,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Записавшиеся на курс - Пора!" },
  },
  {
    path: "/organization/courses/new",
    name: "NewCourse",
    component: NewCourse,
    beforeEnter: ifAuthenticatedOrganizer,
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
    beforeEnter: ifAuthenticatedStudent,
    meta: { title: "Правила олимпиады - Пора!" },
  },
  {
    path: "/olympiads/:id/start",
    name: "OlympiadProcess",
    component: OlympiadProcess,
    beforeEnter: ifAuthenticatedStudent,
    meta: { title: "Олимпиада - Пора!" },
  },
  {
    path: "/olympiads/:id/result",
    name: "OlympiadResult",
    component: OlympiadResult,
    beforeEnter: ifAuthenticatedStudent,
    meta: { title: "Результаты олимпиады - Пора!" },
  },
  {
    path: "/my/olympiads",
    name: "StudentOlympiads",
    component: StudentOlympiads,
    beforeEnter: ifAuthenticatedStudent,
    meta: { title: "Мои олимпиады - Пора!" },
  },
  {
    path: "/organization/olympiads",
    name: "OrganizationOlympiads",
    component: OrganizationOlympiads,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Олимпиады организации - Пора!" },
  },
  {
    path: "/organization/olympiads/:id",
    name: "OrganizationOlympiad",
    component: OrganizationOlympiad,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Олимпиада - Пора!" },
  },

  {
    path: "/organization/olympiads/:id/members",
    name: "OlympiadMembers",
    component: OlympiadMembers,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Участники олимпиады - Пора!" },
  },
  {
    path: "/organization/olympiads/:id/members/:user/answers",
    name: "StudentAnswers",
    component: StudentAnswers,
    beforeEnter: ifAuthenticatedOrganizer,
    meta: { title: "Решения школьника - Пора!" },
  },
  {
    path: "/organization/olympiads/new",
    name: "NewOlympiad",
    component: NewOlympiad,
    beforeEnter: ifAuthenticatedOrganizer,
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
