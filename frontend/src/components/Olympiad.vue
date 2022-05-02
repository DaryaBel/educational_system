<template>
  <div>
    <h1>{{ olympiad.name }}</h1>
    <p>
      <span v-for="subject in olympiad.subjects" :key="subject.id">
        {{ subject.name }}
      </span>
    </p>
    <img src="https://picsum.photos/200" alt="" />
    <p>{{ olympiad.description }}</p>
    <p>
      Организатор: {{ organizationType() }}
      {{ olympiad.organization.shortname }}
    </p>
    <p v-if="formatDate(olympiad.date_end) != null">
      Олимпиада проводится до {{ formatDate(olympiad.date_end) }} (включительно)
    </p>
    <p v-if="formatDate(olympiad.date_result) != null">
      Результаты олимпиады будут объявлены
      {{ formatDate(olympiad.date_result) }}
    </p>
    <button v-if="status != 'Отправлено'" @click="toRules">
      Принять участие
    </button>
  </div>
</template>

<script>
export default {
  name: "Olympiad",
  data() {
    return {
      status: "",
      olympiad: {
        name: 'Олимпиада "Инновационный полет"',
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ultrices enim. Maecenas id sodales libero, vitae tristique orci. Cras quis venenatis sem, laoreet pellentesque dui. Mauris faucibus neque turpis. Vivamus id sapien fermentum metus pulvinar pellentesque eget ac diam. Phasellus tristique massa non bibendum suscipit. Aliquam vel libero ut nunc ultrices maximus ac in turpis. Phasellus commodo, orci sit amet suscipit consectetur, risus est tempus felis, sed rhoncus eros lacus vitae purus. Nullam pellentesque consectetur libero, vel bibendum mauris blandit eu. Quisque hendrerit libero nec sem sollicitudin fermentum. Nullam id dui mattis, imperdiet velit vitae, placerat magna. Aliquam lobortis tempus orci, in placerat dui eleifend id. Sed sed lacus eget nulla aliquam aliquet. Nunc egestas lacus in pellentesque iaculis. Phasellus blandit efficitur lectus, sit amet finibus leo tincidunt eget. Aenean in viverra dui.",
        percent_to_win: 85,
        time_to_pass: undefined,
        date_end: "2022-06-05",
        date_result: "2022-07-05",
        published: true,
        subjects: [
          { id: 1, name: "Обществознание" },
          { id: 2, name: "Экономика" },
        ],
        organization: {
          fullname: "ОАО Тинькофф Банк",
          shortname: "Тинькофф",
          kind: "COMPANY",
          description:
            " российский коммерческий банк, сфокусированный полностью на дистанционном обслуживании, не имеющий розничных отделений",
          logo: "",
        },
      },
    };
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
      // поставить статус как записан
      this.$router.push({ name: "OlympiadRules" });
    },
  },
};
</script>

<style lang="scss"></style>
