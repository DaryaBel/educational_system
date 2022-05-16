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
    <multiselect
      :disabled="isLoading"
      track-by="id"
      label="name"
      v-model="findSubjects"
      placeholder="Выберите школьные предметы"
      :options="subjectList"
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

    <p v-if="filterItems.length == 0">Не найдено</p>
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";

export default {
  name: "StudentOlympiad",
  components: { Multiselect },
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
        { name: "Один", id: "1" },
        { name: "Два", id: "2" },
        { name: "Три", id: "5" },
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
    onLink(id) {
      //   this.$router.push({ name: "Olympiad", params: { id: id } });
    },
  },
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
