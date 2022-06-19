<template>
  <div>
    <loader v-if="isLoading || studentOlympiads == undefined"></loader>
    <div v-else>
      <h1>Мои олимпиады</h1>
      <div class="row mb-3">
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <input
            class="form-control"
            placeholder="Поиск по названию олимпиады и ее описанию"
            name="search"
            id="search"
            :disabled="studentOlympiads == undefined"
            type="text"
            v-model.trim="findString"
          />
        </div>
        <div class="col-lg-2 mb-2">
          <select
            placeholder="Статус"
            :disabled="studentOlympiads == undefined"
            name="status"
            id="status"
            class="form-control"
            v-model.trim="findStatus"
          >
            <option value="ALL">Все</option>
            <option value="TAKEPART">Участвую</option>
            <option value="BEGIN">В процессе выполнения</option>
            <option value="SENT">Отправлено на проверку</option>
            <option value="CHECKED">Проверено</option>
          </select>
        </div>
        <div class="col-lg-3 mb-2">
          <multiselect
            :disabled="studentOlympiads == undefined"
            track-by="id"
            label="name"
            v-model="findSubject"
            placeholder="Школьные предметы"
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
        </div>
        <div class="col-lg-3 mb-2">
          <multiselect
            :disabled="
              studentOlympiads == undefined || organizations == undefined
            "
            v-model="findOrganization"
            track-by="id"
            label="fullname"
            placeholder="Организатор"
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
      </div>

      <div class="row">
        <div
          class="col-md-6 mb-5"
          v-for="olympiad in filterItems"
          :key="olympiad.id"
        >
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
import Loader from "@/components/parts/Loader.vue";

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
  components: { OlympiadElement, Multiselect, Loader },
  data() {
    return {
      findString: "",
      findStatus: "ALL",
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
        if (this.findStatus != "" && this.findStatus != "ALL") {
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
<style lang="scss">
div.col-lg-2 div.multiselect__tags,
div.col-lg-4 div.multiselect__tags,
div.col-lg-3 div.multiselect__tags {
  border: 1px solid #ced4da;
  color: #495057;
  font-weight: 400;
}

div.col-lg-2
  div.multiselect
  div.multiselect__tags
  div.multiselect__tags-wrap
  span.multiselect__tag,
div.col-lg-3
  div.multiselect
  div.multiselect__tags
  div.multiselect__tags-wrap
  span.multiselect__tag,
div.col-lg-4
  div.multiselect
  div.multiselect__tags
  div.multiselect__tags-wrap
  span.multiselect__tag {
  background: #924de9 !important;
  & .multiselect__tag-icon:focus,
  .multiselect__tag-icon:hover {
    background: #924de9 !important;
  }
  & span {
    color: white !important;
  }
}
</style>
