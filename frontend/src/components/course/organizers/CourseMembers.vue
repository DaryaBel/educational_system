<template>
  <div>
    <h1>Записавшиеся на курс</h1>
    <div>
      <input
        placeholder="Поиск по ФИО и email"
        name="search"
        id="search"
        :disabled="courseStudents == undefined"
        type="text"
        v-model.trim="findString"
      />
    </div>

    <div>
      <p v-if="courseStudents == undefined">Загрузка...</p>
      <div v-else>
        <p v-if="filterItems.length == 0">Не найдено</p>
        <table v-else>
          <tr>
            <th>ФИО</th>
            <th>Дата рождения</th>
            <th>Email</th>
          </tr>
          <tr v-for="student in filterItems" :key="student.id">
            <td>
              <span
                >{{ student.student.user.lastName }}
                {{ student.student.user.firstName }}
                {{ student.student.patronymic }}</span
              >
            </td>
            <td>
              <span> {{ formatDate(student.student.birthdate) }} <br /> </span>
            </td>
            <td>{{ student.student.user.email }}</td>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import { ALL_MEMBER_COURSE } from "@/graphql/queries/queries";
export default {
  name: "CourseMembers",
  apollo: {
    courseStudents: {
      query: ALL_MEMBER_COURSE,
      variables() {
        return {
          courseId: this.$route.params.id,
        };
      },
    },
  },

  data() {
    return {
      findString: "",
    };
  },
  computed: {
    filterItems() {
      let students;
      if (
        this.courseStudents != null &&
        this.courseStudents != undefined &&
        this.courseStudents.length != 0
      ) {
        students = this.courseStudents;
        if (this.findString != "") {
          students = students.filter((el) => {
            return (
              (el.student.user.firstName
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.student.user.firstName != "") ||
              (el.student.user.lastName
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.student.user.lastName != "") ||
              (el.student.user.email
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.student.user.email != "") ||
              (el.student.patronymic
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.student.patronymic != "")
            );
          });
        }
      } else students = [];
      return students;
    },
  },

  methods: {
    formatDate(date) {
      if (!date) return "-";
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
  },
};
</script>

<style lang="scss"></style>
