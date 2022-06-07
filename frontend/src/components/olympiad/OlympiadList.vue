<template>
  <div>
    <log-out-button></log-out-button>
    <h1>Олимпиады</h1>
    <div>
      <input
        placeholder="Поиск по названию и описанию"
        name="search"
        id="search"
        :disabled="publishedOlympiads == undefined"
        type="text"
        v-model.trim="findString"
      />
      <multiselect
        :disabled="publishedOlympiads == undefined || subjects == undefined"
        v-model="findSubject"
        track-by="id"
        label="name"
        placeholder="Выберите школьные предметы"
        :options="subjectsOption"
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

      <multiselect
        :disabled="
          publishedOlympiads == undefined || organizations == undefined
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
      <p v-if="publishedOlympiads == undefined">Загрузка...</p>
      <div v-else>
        <div v-for="olympiad in filterItems" :key="olympiad.id">
          <olympiad-element :olympiad="olympiad" :status="'-'">
          </olympiad-element>
        </div>
        <p v-if="filterItems.length == 0">Не найдено</p>
      </div>
    </div>
  </div>
</template>

<script>
import {
  PUBLISHED_OLYMPIADS,
  SHORT_LIST_ORGANIZATIONS,
  SUBJECTS,
} from "@/graphql/queries/queries";
import OlympiadElement from "@/components/olympiad/OlympiadElement.vue";
import LogOutButton from "@/components/LogOutButton.vue";
import Multiselect from "vue-multiselect";

export default {
  name: "OlympiadList",
  apollo: {
    publishedOlympiads: {
      query: PUBLISHED_OLYMPIADS,
    },
    subjects: {
      query: SUBJECTS,
    },
    organizations: {
      query: SHORT_LIST_ORGANIZATIONS,
    },
  },
  components: {
    LogOutButton,
    OlympiadElement,
    Multiselect,
  },
  data() {
    return {
      findString: "",
      findSubject: [],
      findOrganization: [],

      userId: 2,
    };
  },
  computed: {
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
        this.publishedOlympiads != null &&
        this.publishedOlympiads != undefined &&
        this.publishedOlympiads.length != 0
      ) {
        olympiads = this.publishedOlympiads;
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

  methods: {},
};
</script>

<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
