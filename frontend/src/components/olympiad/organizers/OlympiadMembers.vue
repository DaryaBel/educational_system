<template>
  <div>
    <loader v-if="isLoading || results == undefined"></loader>
    <div v-else>
      <h1>Участники олимпиады</h1>
      <div class="row mb-3">
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <input
            class="form-control"
            placeholder="Поиск по ФИО и email"
            name="search"
            id="search"
            :disabled="results == undefined"
            type="text"
            v-model.trim="findString"
          />
        </div>
        <div class="col-lg-3 mb-2 d-flex align-items-center">
          <multiselect
            :disabled="results == undefined"
            v-model="findStatus"
            track-by="status"
            label="name"
            placeholder="Cтатус"
            :options="statusOption"
            :showLabels="false"
            :searchable="false"
            :allow-empty="true"
            :showPointer="false"
            :multiple="true"
            :close-on-select="false"
            :clear-on-select="false"
          >
            <span slot="noResult">Не найдено</span>
          </multiselect>
        </div>
        <div class="col-lg-3 mb-2 d-flex align-items-center">
          <div class="form-check">
            <input
              class="form-check-input"
              type="checkbox"
              id="winner"
              :disabled="results == undefined"
              v-model="won"
              name="winner"
            />
            <label class="form-check-label" for="winner">
              Только победители</label
            >
          </div>
        </div>
      </div>
      <div>
        <p v-if="filterItems.length == 0">Не найдено</p>
        <div v-else>
          <p>
            Результаты
            <span v-if="!results[0].olympiad.resultPublished">еще не </span
            ><span v-if="results[0].olympiad.resultPublished">уже </span
            >опубликованы для школьников.
          </p>
          <button
            class="text-gradient to-block mb-4"
            v-if="
              !results[0].olympiad.resultPublished &&
              countNotCheckedResults != null &&
              countNotCheckedResults < 1
            "
            @click="modal = true"
          >
            Опубликовать результаты

            <span class="text"> Опубликовать результаты </span>
          </button>

          <table class="table">
            <tr>
              <th scope="col">ФИО</th>
              <th scope="col">Дата рождения</th>
              <th scope="col">Email</th>
              <th scope="col">Статус</th>
            </tr>
            <tr v-for="student in filterItems" :key="student.id">
              <td>
                <router-link
                  tag="a"
                  class="text-decoration-none"
                  :to="{
                    name: 'StudentAnswers',
                    params: {
                      id: $route.params.id,
                      user: student.student.user.id,
                    },
                  }"
                  >{{ student.student.user.lastName }}
                  {{ student.student.user.firstName }}
                  {{ student.student.patronymic }}</router-link
                >
              </td>
              <td>
                <span>
                  {{ formatDate(student.student.birthdate) }} <br />
                </span>
              </td>
              <td>{{ student.student.user.email }}</td>
              <td>
                {{ getStatus(student.status, student.won) }}
              </td>
            </tr>
          </table>
          <modal-publish-result
            v-if="modal"
            @publish="toPublishResult"
            @close="modal = false"
          ></modal-publish-result>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {
  OLYMPIAD_RESULTS,
  NUMBER_NOT_CHECKED_RESULTS,
} from "@/graphql/queries/queries";
import { PUBLISH_OLYMPIAD_RESULTS } from "@/graphql/mutations/mutations";
import ModalPublishResult from "@/components/olympiad/organizers/ModalPublishResult.vue";
import Multiselect from "vue-multiselect";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "OlympiadMembers",
  apollo: {
    results: {
      query: OLYMPIAD_RESULTS,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
    countNotCheckedResults: {
      query: NUMBER_NOT_CHECKED_RESULTS,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
  },
  components: {
    Multiselect,
    ModalPublishResult,
    Loader,
  },
  data() {
    return {
      modal: false,
      findStatus: [],
      won: false,
      statusOption: [
        { status: "TAKEPART", name: "Участвует" },
        { status: "BEGIN", name: "В процессе выполнения" },
        { status: "SENT", name: "Ожидает проверки" },
        { status: "CHECKED", name: "Проверено" },
      ],
      findString: "",
    };
  },
  computed: {
    isLoading() {
      return this.$store.state.isLoading;
    },
    filterItems() {
      let students;
      if (
        this.results != null &&
        this.results != undefined &&
        this.results.length != 0
      ) {
        students = this.results;
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
        if (this.findStatus.length != 0) {
          students = students.filter((el) => {
            let flag = false;
            this.findStatus.forEach((status) => {
              if (el.status == status.status) flag = true;
            });
            return flag;
          });
        }
        if (this.won) {
          students = students.filter((el) => el.won);
        }
      } else students = [];
      return students;
    },
  },

  methods: {
    toPublishResult() {
      this.$store.commit("START_LOADING");
      this.$apollo
        .mutate({
          mutation: PUBLISH_OLYMPIAD_RESULTS,
          variables: {
            olympiadId: this.$route.params.id,
            resultPublished: true,
          },
        })
        .then(() => {
          this.$apollo.queries.results.refresh();
          this.$apollo.queries.results.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    getStatus(status, won) {
      let str = "";
      switch (status) {
        case "TAKEPART":
          str = "Участвует";
          break;

        case "BEGIN":
          str = "В процессе выполнения";
          break;

        case "SENT":
          str = "Ожидает проверки";
          break;

        case "CHECKED":
          str = "Проверено";
          if (won) str += ". Победа";
          break;

        default:
          return "?";
          break;
      }
      return str;
    },
    formatDate(date) {
      if (!date) return "-";
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
  },
};
</script>

<style lang="scss"></style>
