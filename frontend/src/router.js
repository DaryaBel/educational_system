import Vue from "vue";
import VueRouter from "vue-router";

import CourseList from "@/components/course/CourseList.vue";
import Course from "@/components/course/Course.vue";
import ExampleComponent from "@/components/ExampleComponent.vue";
import LogIn from "@/components/LogIn.vue";
import Profile from "@/components/Profile.vue";
import SignUp from "@/components/SignUp.vue";
import SignUpEmployee from "@/components/SignUpEmployee.vue";
import DeleteAccount from "@/components/DeleteAccount.vue";
import Olympiad from "@/components/olympiad/Olympiad.vue";
import OlympiadRules from "@/components/olympiad/OlympiadRules.vue";
import OlympiadProcess from "@/components/olympiad/OlympiadProcess.vue";
import StudentOlympiads from "@/components/olympiad/StudentOlympiads.vue";
import StudentCourses from "@/components/course/StudentCourses.vue";
import OrganizationCourses from "@/components/course/organizers/OrganizationCourses.vue";
import OrganizationCourse from "@/components/course/organizers/OrganizationCourse.vue";
import NewCourse from "@/components/course/organizers/NewCourse.vue";

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
    path: "/olympiad",
    name: "Olympiad",
    component: Olympiad,
  },
  {
    path: "/olympiad/rules",
    name: "OlympiadRules",
    component: OlympiadRules,
  },
  {
    path: "/olympiad/start",
    name: "OlympiadProcess",
    component: OlympiadProcess,
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
  { path: "/", component: ExampleComponent },
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
