<template>
  <div>
    <loader v-if="isLoading || organizationOlympiads == undefined"> </loader>
    <div v-else>
      <h1>Олимпиады организации</h1>
      <button @click="onLink()" class="mb-3 text-gradient to-block">
        Добавить новую олимпиаду
        <span class="text">Добавить новую олимпиаду</span>
      </button>
      <div class="row mb-3">
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <input
            placeholder="Поиск по названию и описанию"
            name="search"
            class="form-control"
            id="search"
            :disabled="organizationOlympiads == undefined"
            type="text"
            v-model.trim="findString"
          />
        </div>
        <div class="col-lg-4 mb-2 d-flex align-items-center">
          <span class="mr-2">Опубликована?</span>

          <select
            class="form-control"
            name="published"
            id="published"
            v-model="published"
          >
            <option value="all">Все</option>
            <option value="yes">Да</option>
            <option value="no">Нет</option>
          </select>
        </div>
      </div>
      <div>
        <p v-if="filterItems.length == 0">Не найдено</p>
        <table v-else class="table">
          <tr>
            <th scope="col">Название</th>
            <th scope="col">Предметы</th>
            <th scope="col">Количество заданий</th>
            <th scope="col">Опубликовано</th>
            <th scope="col"></th>
          </tr>
          <tr v-for="olympiad in filterItems" :key="olympiad.id">
            <td>
              <router-link
                tag="a"
                class="text-decoration-none"
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
                class="mb-2 btn-sm text-gradient"
                @click="
                  openModal();
                  modal = true;
                  modalId = olympiad.id;
                  modalName = olympiad.name;
                "
              >
                Удалить
                <span class="text">Удалить</span></button
              ><br />
              <button
                class="gradient btn-sm"
                v-if="!olympiad.published"
                @click="toPublish(olympiad.id, true)"
              >
                Опубликовать
              </button>
              <button
                class="gradient btn-sm"
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
            closeModal();
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
import Loader from "@/components/parts/Loader.vue";

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
    Loader,
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
    openModal() {
      document.documentElement.style.overflow = "hidden";
    },
    closeModal() {
      document.documentElement.style.overflow = "auto";
    },
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
