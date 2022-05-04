<template>
  <div>
    <h1>Мои олимпиады</h1>
    <input
      placeholder="Поиск по названию олимпиаде и ее организатору"
      name="search"
      id="search"
      :disabled="isLoading"
      type="text"
      v-model.trim="findString"
    />

    <select
      placeholder="Статус олимпиады"
      :disabled="isLoading"
      name="status"
      id="status"
      v-model.trim="findStatus"
    >
      <option value="TAKEPART">Записался(лась)</option>
      <option value="BEGIN">В процессе выполнения</option>
      <option value="SENT">Отправлено на проверку</option>
      <option value="CHECKED">Проверено</option>
    </select>

    <multi-select
      class="search-select"
      :isDisabled="isLoading"
      :options="subjectList"
      :selected-options="findSubjects"
      placeholder="Выберите школьные предметы"
      @select="onSelect"
    >
    </multi-select>
    <p v-if="filterItems.length == 0">Не найдено</p>
  </div>
</template>

<script>
import _ from "lodash";
import { MultiSelect } from "vue-search-select";
export default {
  name: "StudentOlympiad",
  components: {
    MultiSelect,
  },
  data() {
    return {
      pagination: 1,
      lastSelectSubject: {},
      isLoading: false,
      findString: "",
      findStatus: "",
      findSubjects: [],
      studentOlympiads: [],
      subjectList: [
        { text: "Один", value: "1" },
        { text: "Два", value: "2" },
        { text: "Три", value: "5" },
      ],
    };
  },
  computed: {
    filterItems() {
      let olympiads;
      if (
        this.studentOlympiads != null &&
        this.studentOlympiads != undefined &&
        this.studentOlympiads.length != 0
      ) {
        olympiads = this.studentOlympiads;
        if (this.findString != "") {
          olympiads = this.olympiads.filter((el) => {
            return (
              (el.name
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.name != "") ||
              (el.organization.fullname
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.organization.fullname != "") ||
              (el.organization.shortname
                .toLowerCase()
                .split(" ")
                .join("")
                .indexOf(this.findString.toLowerCase().split(" ").join("")) !=
                -1 &&
                el.organization.shortname != "")
            );
          });
        }
        if (this.findStatus != "") {
          olympiads = this.olympiads.filter((el) => {
            return el.result.status == this.findStatus;
          });
        }
        if (this.findSubjects.length != 0) {
          olympiads = this.olympiads.filter((el) => {
            let flag = false;
            i = 0;
            j = 0;
            while (!flag && j < el.subjects.length) {
              if (el.subjects[j].id == this.findSubjects[i].value) flag = true;
              if (i == this.findSubjects.length) {
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
    onSelect(items, lastSelectItem) {
      this.findSubjects = items;
      this.lastSelectSubject = lastSelectItem;
    },
    onLink(id) {
      //   this.$router.push({ name: "Olympiad", params: { id: id } });
    },
  },
};
</script>

<style lang="scss">
.form-group div.search-select {
  width: 11rem !important;
}
</style>
