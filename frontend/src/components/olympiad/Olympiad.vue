<template>
  <div>
    <loader v-if="isLoading || olympiad == undefined"> </loader>
    <div v-else>
      <h1>{{ olympiad.name }}</h1>
      <img
        class="rounded img-fluid mb-4"
        :src="'http://localhost:8000/media/' + olympiad.organization.logo"
        alt=""
        style="max-width: 400px; border: 1px solid #dee2e6"
      />

      <p>
        <span
          class="badge my-badge badge-secondary mr-2"
          v-for="subject in olympiad.olympiadSubject"
          :key="subject.subject.id"
        >
          {{ subject.subject.name }}
        </span>
      </p>
      <p>{{ olympiad.description }}</p>
      <p>
        Организатор: {{ organizationType() }}
        {{ olympiad.organization.shortname }}
      </p>
      <p v-if="formatDate(olympiad.dateEnd) != null">
        Олимпиада проводится до
        {{ formatDate(olympiad.dateEnd) }} (включительно).
      </p>
      <p v-if="formatDate(olympiad.dateResult) != null">
        Результаты олимпиады будут объявлены
        {{ formatDate(olympiad.dateResult) }}.
      </p>

      <div v-if="isStudent">
        <button
          v-if="result == undefined"
          @click="toTakePart"
          class="text-gradient to-block"
        >
          Принять участие
          <span class="text">Принять участие</span>
        </button>

        <div v-else>
          <button
            v-if="result.status == 'TAKEPART'"
            @click="toBegin"
            class="gradient to-block mb-2 mr-2"
          >
            Начать выполнение
          </button>

          <button
            @click="toCancelParticipation"
            v-if="result.status == 'TAKEPART'"
            class="text-gradient to-block"
          >
            Отменить участие
            <span class="text">Отменить участие</span>
          </button>

          <button
            @click="toContinue"
            v-if="result.status == 'BEGIN'"
            class="gradient to-block"
          >
            Продолжить выполнение
          </button>

          <p
            v-if="
              result.status == 'SENT' ||
              (result.status == 'CHECKED' && !olympiad.resultPublished)
            "
          >
            Вы успешно отправили свои ответы на олимпиаду. После того, как
            организаторы проверят все решения, будут вывешны результаты.
          </p>
          <button
            @click="toGetResult"
            v-if="result.status == 'CHECKED' && olympiad.resultPublished"
            class="gradient to-block"
          >
            Посмотреть результаты
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";
import { CREATE_RESULT, DELETE_RESULT } from "@/graphql/mutations/mutations";
import { OLYMPIAD, OLYMPIAD_STATUS } from "@/graphql/queries/queries.js";
import Loader from "@/components/parts/Loader.vue";

export default {
  components: { Loader },
  name: "Olympiad",
  data() {
    return {};
  },
  apollo: {
    olympiad: {
      query: OLYMPIAD,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
    result: {
      query: OLYMPIAD_STATUS,
      variables() {
        return {
          userId: this.userId,
          olympiadId: this.$route.params.id,
        };
      },
    },
  },
  computed: {
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    isStudent() {
      return this.$store.state.isStudent;
    },
    resultId() {
      if (this.result == undefined) return 0;
      else return this.result.id;
    },
  },
  methods: {
    toBegin() {
      this.$router.push({
        name: "OlympiadRules",
        params: { id: this.$route.params.id },
      });
    },
    toContinue() {
      this.$router.push({
        name: "OlympiadProcess",
        params: { id: this.$route.params.id },
      });
    },
    toCancelParticipation() {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: DELETE_RESULT,
          variables: {
            resultId: this.resultId,
          },
        })
        .then(() => {
          this.$apollo.queries.result.refresh();
          this.$apollo.queries.result.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    toGetResult() {
      this.$router.push({
        name: "OlympiadResult",
        params: { id: this.$route.params.id },
      });
    },
    toTakePart() {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: CREATE_RESULT,
          variables: {
            olympiadId: this.$route.params.id,
            userId: this.userId,
          },
        })
        .then(() => {
          this.$apollo.queries.result.refresh();
          this.$apollo.queries.result.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    organizationType() {
      if (this.olympiad.organization.kind == "UNIVERSITY")
        return "образовательная организация";
      if (this.olympiad.organization.kind == "COMPANY") return "компания";
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
  },
};
</script>

<style lang="scss">
span.my-badge {
  padding: 4px 8px;
  background: linear-gradient(132.33deg, #d24074 -0.67%, #6518b4 102.54%);
}
</style>
