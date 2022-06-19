<template>
  <div>
    <loader v-if="isLoading || publishedOlympiads == undefined"></loader>
    <div v-else>
      <h1>Олимпиады</h1>
      <div class="row mb-3">
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <input
            class="form-control"
            placeholder="Поиск по названию и описанию"
            name="search"
            id="search"
            :disabled="publishedOlympiads == undefined"
            type="text"
            v-model.trim="findString"
          />
        </div>
        <div class="col-lg-3 mb-2">
          <multiselect
            :disabled="publishedOlympiads == undefined || subjects == undefined"
            v-model="findSubject"
            track-by="id"
            label="name"
            placeholder="Школьные предметы"
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
        </div>
        <div class="col-lg-3 mb-2">
          <multiselect
            :disabled="
              publishedOlympiads == undefined || organizations == undefined
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
import Loader from "@/components/parts/Loader.vue";
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
    OlympiadElement,
    Loader,
    Multiselect,
  },
  data() {
    return {
      findString: "",
      findSubject: [],
      findOrganization: [],
    };
  },
  computed: {
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    isLoading() {
      return this.$store.state.isLoading;
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
