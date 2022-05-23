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
      <button v-if="studentOlympiadResult == undefined">Принять участие</button>
      <div v-else>
        <button
          v-if="studentOlympiadResult.status == 'TAKEPART'"
          @click="toRules"
        >
          Начать выполнение
        </button>
        <button v-if="studentOlympiadResult.status == 'TAKEPART'">
          Отменить участие
        </button>
        <button v-if="studentOlympiadResult.status == 'BEGIN'">
          Продолжить выполнение
        </button>
        <p v-if="studentOlympiadResult.status == 'SENT'">
          Вы успешно отправили свои ответы на олимпиаду. После того, как
          организаторы проверят все решения, будут вывешны результаты.
        </p>
        <button v-if="studentOlympiadResult.status == 'CHECKED'">
          Посмотреть результаты
        </button>
      </div>
    </div>
  </div>
</template>

<script>
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
  methods: {
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
    toRules() {
      this.$router.push({ name: "OlympiadRules" });
    },
  },
};
</script>

<style lang="scss"></style>
