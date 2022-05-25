<template>
  <div>
    <div v-if="olympiad == undefined">
      <p>Загрузка...</p>
    </div>
    <div v-else>
      <h1>{{ olympiad.name }}</h1>
      <p>
        <span
          v-for="subject in olympiad.olympiadSubject"
          :key="subject.subject.id"
        >
          {{ subject.subject.name }}
        </span>
      </p>
      <img src="https://picsum.photos/200" alt="" />
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
      <button v-if="studentOlympiadResult == undefined" @click="toTakePart">
        Принять участие
      </button>
      <div v-else>
        <button
          v-if="studentOlympiadResult.status == 'TAKEPART'"
          @click="toBegin"
        >
          Начать выполнение
        </button>
        <button
          @click="toCancelParticipation"
          v-if="studentOlympiadResult.status == 'TAKEPART'"
        >
          Отменить участие
        </button>
        <button
          @click="toContinue"
          v-if="studentOlympiadResult.status == 'BEGIN'"
        >
          Продолжить выполнение
        </button>
        <p
          v-if="
            studentOlympiadResult.status == 'SENT' ||
            (studentOlympiadResult.status == 'CHECKED' &&
              !studentOlympiadResult.published)
          "
        >
          Вы успешно отправили свои ответы на олимпиаду. После того, как
          организаторы проверят все решения, будут вывешны результаты.
        </p>
        <button
          @click="toGetResult"
          v-if="
            studentOlympiadResult.status == 'CHECKED' &&
            studentOlympiadResult.published
          "
        >
          Посмотреть результаты
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import { CREATE_RESULT, DELETE_RESULT } from "@/graphql/mutations/mutations";
import { OLYMPIAD, OLYMPIAD_STATUS } from "@/graphql/queries/queries.js";
export default {
  name: "Olympiad",
  data() {
    return {
      userId: 2,
    };
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
    studentOlympiadResult: {
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
    resultId() {
      if (this.studentOlympiadResult == undefined) return 0;
      else return this.studentOlympiadResult.id;
    },
  },
  methods: {
    toBegin() {
      this.$router.push({
        name: "OlympiadRules",
        params: { id: this.$route.params.id },
      });

      // this.$apollo
      //   .mutate({
      //     mutation: UPDATE_RESULT,
      //     variables: {
      //       resultId: this.resultId,
      //       status: "BEGIN",
      //     },
      //   })
      //   .then(() => {
      //     this.$apollo.queries.studentOlympiadResult.refresh();
      //     this.$apollo.queries.studentOlympiadResult.refetch();
      //   })
      //   .catch((error) => {
      //     console.error(error);
      //   });
    },
    toContinue() {
      this.$router.push({
        name: "OlympiadProcess",
        params: { id: this.$route.params.id },
      });
    },
    toCancelParticipation() {
      this.$apollo
        .mutate({
          mutation: DELETE_RESULT,
          variables: {
            resultId: this.resultId,
          },
        })
        .then(() => {
          this.$apollo.queries.studentOlympiadResult.refresh();
          this.$apollo.queries.studentOlympiadResult.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    toGetResult() {
      this.$router.push({
        name: "OlympiadResult",
        params: { id: this.$route.params.id },
      });
    },
    toTakePart() {
      this.$apollo
        .mutate({
          mutation: CREATE_RESULT,
          variables: {
            olympiadId: this.$route.params.id,
            userId: this.userId,
          },
        })
        .then(() => {
          this.$apollo.queries.studentOlympiadResult.refresh();
          this.$apollo.queries.studentOlympiadResult.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
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

<style lang="scss"></style>
