<template>
  <div>
    <div v-if="isLoading || studentOlympiads == undefined">Загрузка...</div>
    <div v-else>
      <h1>Мои олимпиады</h1>
      <div>
        <input
          placeholder="Поиск по названию олимпиады и ее описанию"
          name="search"
          id="search"
          :disabled="studentOlympiads == undefined"
          type="text"
          v-model.trim="findString"
        />

        <select
          placeholder="Статус"
          :disabled="studentOlympiads == undefined"
          name="status"
          id="status"
          v-model.trim="findStatus"
        >
          <option value="TAKEPART">Участвую</option>
          <option value="BEGIN">В процессе выполнения</option>
          <option value="SENT">Отправлено на проверку</option>
          <option value="CHECKED">Проверено</option>
        </select>
        <multiselect
          :disabled="studentOlympiads == undefined"
          track-by="id"
          label="name"
          v-model="findSubject"
          placeholder="Выберите школьные предметы"
          :options="subjectsOption"
          :showLabels="false"
          :searchable="true"
          :multiple="true"
          :close-on-select="false"
          :clear-on-select="false"
          :allow-empty="true"
          :showPointer="false"
        >
          <span slot="noResult">Не найдено</span>
        </multiselect>
        <multiselect
          :disabled="
            studentOlympiads == undefined || organizations == undefined
          "
          v-model="findOrganization"
          track-by="id"
          label="fullname"
          placeholder="Выберите организатора"
          :options="organizationsOption"
          :showLabels="false"
          :searchable="true"
          :allow-empty="true"
          :showPointer="false"
          :multiple="true"
          :close-on-select="false"
          :clear-on-select="false"
        >
          <span slot="noResult">Не найдено</span>
        </multiselect>
      </div>

      <div>
        <div v-for="olympiad in filterItems" :key="olympiad.id">
          <olympiad-element
            :olympiad="olympiad"
            :status="getStatusResult(olympiad.id)"
          >
          </olympiad-element>
        </div>
        <p v-if="filterItems.length == 0">Не найдено</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  STUDENT_OLYMPIADS,
  SHORT_LIST_ORGANIZATIONS,
  SUBJECTS,
} from "@/graphql/queries/queries";
import Multiselect from "vue-multiselect";
import OlympiadElement from "@/components/olympiad/OlympiadElement.vue";
import jwt from "jsonwebtoken";

export default {
  name: "StudentOlympiads",
  apollo: {
    studentOlympiads: {
      query: STUDENT_OLYMPIADS,
      variables() {
        return {
          userId: this.userId,
        };
      },
    },
    subjects: {
      query: SUBJECTS,
    },
    organizations: {
      query: SHORT_LIST_ORGANIZATIONS,
    },
  },
  components: { OlympiadElement, Multiselect },
  data() {
    return {
      findString: "",
      findStatus: "",
      findSubject: [],
      findOrganization: [],
    };
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    organizationsOption() {
      if (this.organizations == undefined) return [];
      else return this.organizations;
    },

    filterItems() {
      let olympiads;
      if (
        this.studentOlympiads != null &&
        this.studentOlympiads != undefined &&
        this.studentOlympiads.length != 0
      ) {
        olympiads = this.studentOlympiads;
        if (this.findString != "") {
          olympiads = olympiads.filter((el) => {
            return (
              (el.name
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.name != "") ||
              (el.description
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.description != "")
            );
          });
        }
        if (this.findStatus != "") {
          olympiads = olympiads.filter((el) => {
            let flag = false;
            let userResult = el.olympiadResult.find(
              (res) => res.student.user.id == this.userId
            );
            if (userResult.status == this.findStatus) flag = true;
            return flag;
          });
        }
        if (this.findOrganization.length != 0) {
          olympiads = olympiads.filter((el) => {
            let flag = false;
            this.findOrganization.forEach((organization) => {
              if (el.organization.id == organization.id) flag = true;
            });
            return flag;
          });
        }
        if (this.findSubject.length != 0) {
          olympiads = olympiads.filter((el) => {
            let flag = false;
            let i = 0;
            let j = 0;
            while (!flag && j < el.olympiadSubject.length) {
              if (el.olympiadSubject[j].subject.id == this.findSubject[i].id)
                flag = true;
              if (i + 1 == this.findSubject.length) {
                i = 0;
                j++;
              } else i++;
            }
            return flag;
          });
        }
      } else olympiads = [];
      return olympiads;
    },
  },
  methods: {
    getStatusResult(id) {
      let olympiad = this.studentOlympiads.find((el) => el.id == id);
      let userResult = olympiad.olympiadResult.find(
        (res) => res.student.user.id == this.userId
      );
      return this.statusType(userResult.status, olympiad.resultPublished);
    },
    statusType(status, published) {
      switch (status) {
        case "TAKEPART":
          return "Участвую";
          break;

        case "BEGIN":
          return "В процессе выполнения";
          break;

        case "SENT":
          return "Отправлено на проверку";
          break;

        case "CHECKED":
          if (!published) return "Отправлено на проверку";
          else return "Проверено";
          break;

        default:
          return "-";
          break;
      }
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
