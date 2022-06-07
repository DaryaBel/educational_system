<template>
  <div>
    <div v-if="isLoading || organizationOlympiads == undefined">
      Загрузка...
    </div>
    <div v-else>
      <h1>Олимпиады организации</h1>
      <button @click="onLink()">Добавить новую олимпиаду</button>
      <div>
        <input
          placeholder="Поиск по названию и описанию"
          name="search"
          id="search"
          :disabled="organizationOlympiads == undefined"
          type="text"
          v-model.trim="findString"
        />
      </div>
      <span>Опубликована?</span>
      <select name="published" id="published" v-model="published">
        <option value="all">Все</option>
        <option value="yes">Да</option>
        <option value="no">Нет</option>
      </select>
      <div>
        <p v-if="filterItems.length == 0">Не найдено</p>
        <table v-else>
          <tr>
            <th>Название</th>
            <th>Предметы</th>
            <th>Количество заданий</th>
            <th>Опубликовано</th>
            <th></th>
          </tr>
          <tr v-for="olympiad in filterItems" :key="olympiad.id">
            <td>
              <router-link
                tag="a"
                :to="{
                  name: 'OrganizationOlympiad',
                  params: { id: olympiad.id },
                }"
                >{{ olympiad.name }}</router-link
              >
            </td>
            <td>
              <span
                v-for="subject in olympiad.olympiadSubject"
                :key="subject.subject.id"
              >
                {{ subject.subject.name }} <br />
              </span>
            </td>
            <td>{{ olympiad.olympiadTask.length }}</td>
            <td>{{ olympiad.published ? "Да" : "Нет" }}</td>
            <td>
              <button
                @click="
                  modal = true;
                  modalId = olympiad.id;
                  modalName = olympiad.name;
                "
              >
                Удалить</button
              ><br />
              <button
                v-if="!olympiad.published"
                @click="toPublish(olympiad.id, true)"
              >
                Опубликовать
              </button>
              <button
                v-if="olympiad.published"
                @click="toPublish(olympiad.id, false)"
              >
                Снять с публикации
              </button>
            </td>
          </tr>
        </table>
        <modal-delete-olympiad
          v-if="modal"
          @delete="deleteOlympiad"
          @close="
            modal = false;
            modalId = 0;
            modalName = '';
          "
          :olympiadId="modalId"
          :olympiadName="modalName"
        ></modal-delete-olympiad>
      </div>
    </div>
  </div>
</template>

<script>
import jwt from "jsonwebtoken";

import {
  PUBLISH_OLYMPIAD,
  DELETE_OLYMPIAD,
} from "@/graphql/mutations/mutations";
import { ORGANIZATION_OLYMPIADS } from "@/graphql/queries/queries";
import ModalDeleteOlympiad from "@/components/olympiad/organizers/ModalDeleteOlympiad.vue";
export default {
  name: "OrganizationOlympiads",
  apollo: {
    organizationOlympiads: {
      query: ORGANIZATION_OLYMPIADS,
      variables() {
        return {
          organizationId: this.organizationId,
        };
      },
    },
  },
  components: {
    ModalDeleteOlympiad,
  },
  data() {
    return {
      modal: false,
      modalId: 0,
      modalName: "",
      findString: "",
      published: "all",
    };
  },
  computed: {
    organizationId() {
      return jwt.decode(localStorage.getItem("token")).organization_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    filterItems() {
      let olympiads;
      if (
        this.organizationOlympiads != null &&
        this.organizationOlympiads != undefined &&
        this.organizationOlympiads.length != 0
      ) {
        olympiads = this.organizationOlympiads;
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
        if (this.published != "all") {
          olympiads = olympiads.filter((el) => {
            let publishedBoolean = this.published == "yes" ? true : false;
            return el.published == publishedBoolean;
          });
        }
      } else olympiads = [];
      return olympiads;
    },
  },

  methods: {
    toPublish(olympiadId, published) {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: PUBLISH_OLYMPIAD,
          variables: {
            olympiadId: olympiadId,
            published: published,
          },
        })
        .then(() => {
          this.$apollo.queries.organizationOlympiads.refresh();
          this.$apollo.queries.organizationOlympiads.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    onLink() {
      this.$router.push({ name: "NewOlympiad" });
    },
    deleteOlympiad(olympiadId) {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: DELETE_OLYMPIAD,
          variables: {
            olympiadId: olympiadId,
          },
        })
        .then(() => {
          this.$apollo.queries.organizationOlympiads.refresh();
          this.$apollo.queries.organizationOlympiads.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
  },
};
</script>

<style lang="scss"></style>
