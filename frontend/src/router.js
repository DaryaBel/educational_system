import Vue from "vue";
import VueRouter from "vue-router";

import CourseList from "@/components/course/CourseList.vue";
import Course from "@/components/course/Course.vue";
import LogIn from "@/components/LogIn.vue";
import Profile from "@/components/Profile.vue";
import SignUp from "@/components/SignUp.vue";
import SignUpEmployee from "@/components/SignUpEmployee.vue";
import DeleteAccount from "@/components/DeleteAccount.vue";
import OlympiadList from "@/components/olympiad/OlympiadList.vue";
import Olympiad from "@/components/olympiad/Olympiad.vue";
import OlympiadRules from "@/components/olympiad/OlympiadRules.vue";
import OlympiadProcess from "@/components/olympiad/OlympiadProcess.vue";
import OlympiadResult from "@/components/olympiad/OlympiadResult.vue";
import StudentOlympiads from "@/components/olympiad/StudentOlympiads.vue";
import StudentCourses from "@/components/course/StudentCourses.vue";
import OrganizationCourses from "@/components/course/organizers/OrganizationCourses.vue";
import OrganizationCourse from "@/components/course/organizers/OrganizationCourse.vue";
import NewCourse from "@/components/course/organizers/NewCourse.vue";
import CourseMembers from "@/components/course/organizers/CourseMembers.vue";
import OrganizationOlympiads from "@/components/olympiad/organizers/OrganizationOlympiads.vue";
import OrganizationOlympiad from "@/components/olympiad/organizers/OrganizationOlympiad.vue";
import NewOlympiad from "@/components/olympiad/organizers/NewOlympiad.vue";
import OlympiadMembers from "@/components/olympiad/organizers/OlympiadMembers.vue";
import StudentAnswers from "@/components/olympiad/organizers/StudentAnswers.vue";

const routes = [
  {
    path: "/login",
    name: "LogIn",
    component: LogIn,
  },
  {
    path: "/organization/courses/new",
    name: "NewCourse",
    component: NewCourse,
  },
  {
    path: "/olympiads",
    name: "OlympiadList",
    component: OlympiadList,
  },
  {
    path: "/organization/course/:id/members",
    name: "CourseMembers",
    component: CourseMembers,
  },
  {
    path: "/organization/olympiad/:id/members",
    name: "OlympiadMembers",
    component: OlympiadMembers,
  },
  {
    path: "/organization/olympiad/:id/members/:user/answers",
    name: "StudentAnswers",
    component: StudentAnswers,
  },
  {
    path: "/organization/olympiads/new",
    name: "NewOlympiad",
    component: NewOlympiad,
  },
  {
    path: "/organization/courses",
    name: "OrganizationCourses",
    component: OrganizationCourses,
  },
  {
    path: "/organization/course/:id",
    name: "OrganizationCourse",
    component: OrganizationCourse,
  },
  {
    path: "/organization/olympiads",
    name: "OrganizationOlympiads",
    component: OrganizationOlympiads,
  },
  {
    path: "/organization/olympiads/:id",
    name: "OrganizationOlympiad",
    component: OrganizationOlympiad,
  },
  {
    path: "/course/:id",
    name: "Course",
    component: Course,
  },
  {
    path: "/courses",
    name: "CourseList",
    component: CourseList,
  },

  {
    path: "/my/olympiads",
    name: "StudentOlympiads",
    component: StudentOlympiads,
  },
  {
    path: "/my/courses",
    name: "StudentCourses",
    component: StudentCourses,
  },

  {
    path: "/olympiad/:id",
    name: "Olympiad",
    component: Olympiad,
  },
  {
    path: "/olympiad/:id/rules",
    name: "OlympiadRules",
    component: OlympiadRules,
  },
  {
    path: "/olympiad/:id/start",
    name: "OlympiadProcess",
    component: OlympiadProcess,
  },
  {
    path: "/olympiad/:id/results",
    name: "OlympiadResult",
    component: OlympiadResult,
  },
  {
    path: "/delete-account",
    name: "DeleteAccount",
    component: DeleteAccount,
  },
  {
    path: "/profile",
    name: "Profile",
    component: Profile,
  },
  {
    path: "/signup",
    name: "SignUp",
    component: SignUp,
  },
  {
    path: "/signup/employee",
    name: "SignUpEmployee",
    component: SignUpEmployee,
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
