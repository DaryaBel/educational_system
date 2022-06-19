<template>
  <div>
    <loader v-if="isLoading"></loader>
    <div v-else>
      <h1>Создать олимпиаду</h1>
      <form>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name" for="name">Название *</label><br />
            <input
              id="name"
              name="name"
              class="form-control"
              type="text"
              v-model.trim="form.name"
              :class="{ 'is-invalid': submittedForm && $v.form.name.$error }"
            />
            <p
              v-if="submittedForm && !$v.form.name.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name" for="description">Описание </label><br />
            <textarea
              name="description"
              id="description"
              cols="30"
              class="form-control"
              rows="10"
              v-model.trim="form.description"
              :class="{
                'is-invalid': submittedForm && $v.form.description.$error,
              }"
            ></textarea>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name" for="subjects">Предметы *</label><br />
            <multiselect
              :disabled="subjects == undefined"
              v-model="form.subjects"
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
            <div class="is-invalid"></div>
            <p
              v-if="submittedForm && !$v.form.subjects.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name" for="percentToWin"
              >Необходимое количество % для победы *</label
            ><br />
            <input
              name="percentToWin"
              id="percentToWin"
              type="number"
              min="1"
              class="form-control"
              max="100"
              step="1"
              v-model.trim="form.percentToWin"
              :class="{
                'is-invalid': submittedForm && $v.form.percentToWin.$error,
              }"
            />
            <p
              v-if="submittedForm && !$v.form.percentToWin.required"
              class="invalid-feedback"
            >
              Данное поле обязательно
            </p>
            <p
              v-if="submittedForm && !$v.form.percentToWin.betweenValue"
              class="invalid-feedback"
            >
              Число должно находиться в отрезке от 1 до 100
            </p>
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name" for="dateEnd"
              >Дата окончания приема ответов</label
            ><br />
            <input
              class="form-control"
              id="dateEnd"
              name="dateEnd"
              type="date"
              v-model="form.dateEnd"
              :class="{ 'is-invalid': submittedForm && $v.form.dateEnd.$error }"
            />
          </div>
        </div>
        <div class="form-row">
          <div class="form-group col-md-6">
            <label class="form-name" for="dateResult"
              >Дата оглашения результатов</label
            ><br />
            <input
              class="form-control"
              id="dateResult"
              name="dateResult"
              type="date"
              v-model="form.dateResult"
              :class="{
                'is-invalid': submittedForm && $v.form.dateResult.$error,
              }"
            />
          </div>
        </div>
      </form>
      <div>
        <p class="fs-2 font-weight-normal">Задания</p>
        <div
          v-for="(task, i) in sortedTasks"
          :key="i"
          :set="(v = $v.tasks.$each[i])"
        >
          <div class="form-row">
            <div class="form-group col-md-6 position-relative">
              <label class="form-name" for="task">Текст задания *</label><br />
              <textarea
                class="form-control"
                name="task"
                id="task"
                cols="30"
                rows="10"
                v-model.trim="task.task"
                :class="{
                  'is-invalid': submittedForm && v.task.$error,
                }"
              ></textarea>
              <p
                v-if="submittedForm && !v.task.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
              <div
                class="position-absolute d-flex flex-column"
                style="top: 30px; right: -45px"
              >
                <button
                  class="mb-2 gradient"
                  v-if="tasks.length != 1"
                  :disabled="task.order == 1"
                  @click="toUp(task.order)"
                  style="padding: 5px 10px"
                  aria-label="arrow-up"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-arrow-up"
                    viewBox="0 0 16 16"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M8 15a.5.5 0 0 0 .5-.5V2.707l3.146 3.147a.5.5 0 0 0 .708-.708l-4-4a.5.5 0 0 0-.708 0l-4 4a.5.5 0 1 0 .708.708L7.5 2.707V14.5a.5.5 0 0 0 .5.5z"
                    />
                  </svg>
                </button>
                <button
                  class="mb-2 gradient"
                  v-if="tasks.length != 1"
                  :disabled="task.order == tasks.length"
                  @click="toDown(task.order)"
                  style="padding: 5px 10px"
                  aria-label="arrow-down"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-arrow-down"
                    viewBox="0 0 16 16"
                  >
                    <path
                      fill-rule="evenodd"
                      d="M8 1a.5.5 0 0 1 .5.5v11.793l3.146-3.147a.5.5 0 0 1 .708.708l-4 4a.5.5 0 0 1-.708 0l-4-4a.5.5 0 0 1 .708-.708L7.5 13.293V1.5A.5.5 0 0 1 8 1z"
                    />
                  </svg>
                </button>
                <button
                  class="gradient"
                  v-if="tasks.length != 1"
                  @click="deleteFromLocalTasks(task.order)"
                  style="padding: 5px 10px"
                  aria-label="trash3"
                >
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    fill="currentColor"
                    class="bi bi-trash3"
                    viewBox="0 0 16 16"
                  >
                    <path
                      d="M6.5 1h3a.5.5 0 0 1 .5.5v1H6v-1a.5.5 0 0 1 .5-.5ZM11 2.5v-1A1.5 1.5 0 0 0 9.5 0h-3A1.5 1.5 0 0 0 5 1.5v1H2.506a.58.58 0 0 0-.01 0H1.5a.5.5 0 0 0 0 1h.538l.853 10.66A2 2 0 0 0 4.885 16h6.23a2 2 0 0 0 1.994-1.84l.853-10.66h.538a.5.5 0 0 0 0-1h-.995a.59.59 0 0 0-.01 0H11Zm1.958 1-.846 10.58a1 1 0 0 1-.997.92h-6.23a1 1 0 0 1-.997-.92L3.042 3.5h9.916Zm-7.487 1a.5.5 0 0 1 .528.47l.5 8.5a.5.5 0 0 1-.998.06L5 5.03a.5.5 0 0 1 .47-.53Zm5.058 0a.5.5 0 0 1 .47.53l-.5 8.5a.5.5 0 1 1-.998-.06l.5-8.5a.5.5 0 0 1 .528-.47ZM8 4.5a.5.5 0 0 1 .5.5v8.5a.5.5 0 0 1-1 0V5a.5.5 0 0 1 .5-.5Z"
                    />
                  </svg>
                </button>
              </div>
            </div>
          </div>
          <div class="form-row">
            <div class="form-group col-md-6">
              <label class="form-name" for="maxScore">Максимальный балл *</label
              ><br />
              <input
                class="form-control"
                name="maxScore"
                id="maxScore"
                type="number"
                min="0"
                max="100"
                step="1"
                v-model.trim="task.maxScore"
                :class="{
                  'is-invalid': submittedForm && v.maxScore.$error,
                }"
              />
              <p
                v-if="submittedForm && !v.maxScore.required"
                class="invalid-feedback"
              >
                Данное поле обязательно
              </p>
              <p
                v-if="submittedForm && !v.maxScore.betweenValue"
                class="invalid-feedback"
              >
                Число должно находиться в отрезке от 1 до 100
              </p>
            </div>
          </div>
        </div>

        <button
          class="gradient"
          @click="
            tasks.push({
              task: undefined,
              maxScore: undefined,
              order: tasks.length + 1,
            })
          "
          style="padding: 5px 10px"
          aria-label="plus"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="16"
            height="16"
            fill="currentColor"
            class="bi bi-plus"
            viewBox="0 0 16 16"
          >
            <path
              d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3v3a.5.5 0 0 1-1 0v-3h-3a.5.5 0 0 1 0-1h3v-3A.5.5 0 0 1 8 4z"
            />
          </svg>
        </button>
      </div>

      <p class="mt-2">* - обязательное поле</p>
      <button class="text-gradient to-block" @click="onAdd">
        Сохранить
        <span class="text">Сохранить</span>
      </button>

      <Transition name="fade">
        <div
          v-if="newObj"
          class="position-fixed my-sticker bottom-0 right-0 p-3"
          style="z-index: 1000; width: 300px; right: 0; bottom: 140px"
        >
          <div class="alert alert-primary" role="alert">
            Вы успешно создали олимпиаду!
            <router-link
              tag="a"
              class="text-decoration-none"
              :to="{ name: 'OrganizationOlympiads' }"
              >Перейти к списку олимпиад организации</router-link
            >.
          </div>
        </div>
      </Transition>
    </div>
  </div>
</template>

<script>
import {
  CREATE_OLYMPIAD,
  CREATE_OLYMPIAD_SUBJECT,
  CREATE_TASK,
} from "@/graphql/mutations/mutations";
import { required, integer, between } from "vuelidate/lib/validators";
import Multiselect from "vue-multiselect";
import { SUBJECTS } from "@/graphql/queries/queries";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "NewOlympiad",

  apollo: {
    subjects: {
      query: SUBJECTS,
    },
  },
  components: {
    Multiselect,
    Loader,
  },

  data() {
    return {
      newObj: false,
      tasks: [{ task: undefined, maxScore: undefined, order: 1 }],
      createdId: undefined,
      form: {
        name: undefined,
        description: undefined,
        percentToWin: undefined,
        dateResult: undefined,
        dateEnd: undefined,
        subjects: [],
      },

      submittedForm: false,
    };
  },
  validations: {
    form: {
      name: { required },
      description: {},
      dateResult: {},
      dateEnd: {},
      subjects: { required },
      percentToWin: { required, integer, betweenValue: between(1, 100) },
    },
    tasks: {
      $each: {
        task: {
          required,
        },
        maxScore: {
          required,
          integer,
          betweenValue: between(1, 100),
        },
      },
    },
  },
  computed: {
    organizationId() {
      return jwt.decode(localStorage.getItem("token")).organization_id;
    },
    userId() {
      return jwt.decode(localStorage.getItem("token")).user_id;
    },
    isLoading() {
      return this.$store.state.isLoading;
    },
    sortedTasks() {
      return this.tasks.sort(this.sortByOrder);
    },
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
  },
  methods: {
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
    },
    deleteFromLocalTasks(order) {
      let i = this.tasks.findIndex((el) => el.order == order);
      this.tasks.splice(i, 1);
      for (var k = i; k < this.tasks.length; k++) {
        this.tasks[k].order = this.tasks[k].order - 1;
      }
    },
    toUp(order) {
      let i1 = this.tasks.findIndex((el) => el.order == order);
      let i2 = this.tasks.findIndex((el) => el.order == order - 1);
      this.tasks[i1].order = order - 1;
      this.tasks[i2].order = order;
    },
    toDown(order) {
      let i1 = this.tasks.findIndex((el) => el.order == order);
      let i2 = this.tasks.findIndex((el) => el.order == order + 1);
      this.tasks[i1].order = order + 1;
      this.tasks[i2].order = order;
    },
    onAdd() {
      this.submittedForm = true;
      this.$v.form.$touch();
      this.$v.tasks.$touch();
      if (this.$v.form.$invalid) {
        return;
      }
      if (this.$v.tasks.$invalid) {
        return;
      }
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: CREATE_OLYMPIAD,
          variables: {
            name: this.form.name,
            organizationId: this.organizationId,
            description: this.form.description,
            dateResult: this.form.dateResult,
            dateEnd: this.form.dateEnd,
            percentToWin: this.form.percentToWin,
          },
        })
        .then((result) => {
          this.createdId = result.data.createOlympiad.olympiad.id;
          this.form.subjects.forEach((element) => {
            this.$apollo
              .mutate({
                mutation: CREATE_OLYMPIAD_SUBJECT,
                variables: {
                  subjectId: element.id,
                  olympiadId: this.createdId,
                },
              })
              .then(() => {})
              .catch((error) => {
                console.error(error);
              });
          });
          this.tasks.forEach((element) => {
            this.$apollo
              .mutate({
                mutation: CREATE_TASK,
                variables: {
                  task: element.task,
                  maxScore: element.maxScore,
                  order: element.order,
                  olympiadId: this.createdId,
                },
              })
              .then(() => {})
              .catch((error) => {
                console.error(error);
              });
          });

          this.form = {
            name: undefined,
            description: undefined,
            percentToWin: undefined,
            dateResult: undefined,
            dateEnd: undefined,
            subjects: [],
          };
          this.tasks = [{ task: undefined, maxScore: undefined, order: 1 }];

          this.submittedForm = false;
          this.$store.commit("STOP_LOADING");
          this.newObj = true;
          setTimeout(() => {
            this.newObj = false;
          }, 5000);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss">
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

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.8s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
