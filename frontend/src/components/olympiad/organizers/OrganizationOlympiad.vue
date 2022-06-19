<template>
  <div>
    <loader v-if="isLoading || olympiad == undefined"></loader>
    <div v-else>
      <div v-if="!edit">
        <div class="position-relative">
          <h1 class="mb-3">{{ olympiad.name }}</h1>
          <p
            class="position-absolute"
            style="font-size: 20px; top: -20px; right: 0"
            v-if="olympiad.published"
          >
            <span class="badge badge-primary mr-2"> Опубликовано </span>
          </p>
          <p
            class="position-absolute"
            style="font-size: 20px; top: -20px; right: 0"
            v-if="!olympiad.published"
          >
            <span class="badge badge-danger mr-2"> Не опубликовано </span>
          </p>
        </div>
        <p>
          <span
            class="badge my-badge badge-secondary mr-2"
            v-for="subject in olympiad.olympiadSubject"
            :key="subject.subject.id"
          >
            {{ subject.subject.name }}
          </span>
        </p>
        <p>{{ olympiad.description }}</p>
        <p v-if="formatDate(olympiad.dateEnd) != null">
          Олимпиада проводится до
          {{ formatDate(olympiad.dateEnd) }} (включительно).
        </p>
        <p v-if="formatDate(olympiad.dateResult) != null">
          Результаты олимпиады будут объявлены
          {{ formatDate(olympiad.dateResult) }}.
        </p>

        <p>
          Необходимое количество процентов для победы:
          {{ olympiad.percentToWin }}%.
        </p>
        <div>
          <p class="fs-2" v-if="olympiad.olympiadTask.length == 0">
            К данной олимпиаде пока не добавлено заданий
          </p>
          <div v-else>
            <div v-for="task in sortedTasks" :key="task.id">
              <p class="fs-2">{{ task.order }} задание</p>
              <p>{{ task.task }}</p>
              <p>Максиальный балл: {{ task.maxScore }}</p>
            </div>
          </div>
        </div>
        <p>
          <a
            @click="onLink"
            style="cursor: pointer"
            class="text-decoration-none"
            >Посмотреть участников</a
          >
        </p>

        <button
          class="text-gradient btn-sm mr-2"
          @click="
            modal = true;
            modalId = olympiad.id;
            modalName = olympiad.name;
          "
        >
          Удалить
          <span class="text">Удалить</span>
        </button>

        <button
          class="gradient btn-sm mr-2"
          v-if="!olympiad.published"
          @click="onEdit"
        >
          Отредактировать
        </button>

        <button
          class="text-gradient btn-sm mr-2"
          v-if="!olympiad.published"
          @click="toPublish(olympiad.id, true)"
        >
          Опубликовать
          <span class="text">Опубликовать</span>
        </button>
        <button
          class="text-gradient btn-sm mr-2"
          v-if="olympiad.published"
          @click="toPublish(olympiad.id, false)"
        >
          Снять с публикации
          <span class="text">Снять с публикации</span>
        </button>
      </div>
      <div v-else>
        <h1>Редактирование олимпиады</h1>
        <div class="form-group">
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
                  :class="{
                    'is-invalid': submittedForm && $v.form.name.$error,
                  }"
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
                <label class="form-name" for="description">Описание </label
                ><br />
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
                <label class="form-name" for="dateEnd"
                  >Дата окончания приема ответов</label
                ><br />
                <input
                  id="dateEnd"
                  name="dateEnd"
                  class="form-control"
                  type="date"
                  v-model="form.dateEnd"
                  :class="{
                    'is-invalid': submittedForm && $v.form.dateEnd.$error,
                  }"
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
            <div class="form-row">
              <div class="form-group col-md-6">
                <label class="form-name" for="percentToWin"
                  >Необходимое количество % для победы *</label
                ><br />
                <input
                  class="form-control"
                  name="percentToWin"
                  id="percentToWin"
                  type="number"
                  min="1"
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
          </form>
          <div>
            <p class="fs-2 font-weight-normal">Задания</p>
            <div
              v-for="(task, i) in sortedEditTasks"
              :key="i"
              :set="(v = $v.tasks.$each[i])"
            >
              <div class="form-row">
                <div class="form-group col-md-6 position-relative">
                  <label class="form-name" for="task">Текст задания *</label
                  ><br />
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
                  <label class="form-name" for="maxScore"
                    >Максимальный балл *</label
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
        </div>
        <p class="mt-2">* - обязательное поле</p>
        <button class="text-gradient to-block" @click="onEdit">
          Сохранить
          <span class="text">Сохранить</span>
        </button>
      </div>
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
</template>

<script>
import {
  PUBLISH_OLYMPIAD,
  UPDATE_OLYMPIAD,
  DELETE_OLYMPIAD,
  UPDATE_TASK,
  CREATE_TASK,
  DELETE_TASK,
  CREATE_OLYMPIAD_SUBJECT,
  DELETE_OLYMPIAD_SUBJECT,
} from "@/graphql/mutations/mutations";
import { required, integer, between } from "vuelidate/lib/validators";
import Multiselect from "vue-multiselect";
import { OLYMPIAD_FOR_ORGANIZERS, SUBJECTS } from "@/graphql/queries/queries";
import ModalDeleteOlympiad from "@/components/olympiad/organizers/ModalDeleteOlympiad.vue";
import jwt from "jsonwebtoken";
import Loader from "@/components/parts/Loader.vue";

export default {
  name: "OrganizationOlympiad",
  apollo: {
    olympiad: {
      query: OLYMPIAD_FOR_ORGANIZERS,
      variables() {
        return {
          olympiadId: this.$route.params.id,
        };
      },
    },
    subjects: {
      query: SUBJECTS,
    },
  },
  components: {
    Multiselect,
    ModalDeleteOlympiad,
    Loader,
  },
  data() {
    return {
      modal: false,
      modalId: 0,
      modalName: "",
      tasks: [{ task: undefined, maxScore: undefined, order: 1 }],
      form: {
        name: undefined,
        description: undefined,
        percentToWin: undefined,
        dateResult: undefined,
        dateEnd: undefined,
        subjects: [],
      },
      edit: false,

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
    isLoading() {
      return this.$store.state.isLoading;
    },
    subjectsOption() {
      if (this.subjects == undefined) return [];
      else return this.subjects;
    },
    sortedTasks() {
      return this.olympiad.olympiadTask.sort(this.sortByOrder);
    },
    sortedEditTasks() {
      return this.tasks.sort(this.sortByOrder);
    },
  },
  methods: {
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
    deleteOlympiad() {
      this.$store.commit("START_LOADING");

      this.$apollo
        .mutate({
          mutation: DELETE_OLYMPIAD,
          variables: {
            olympiadId: this.$route.params.id,
          },
        })
        .then(() => {
          this.$router.push({
            name: "OrganizationOlympiads",
          });
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
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
          this.$apollo.queries.olympiad.refresh();
          this.$apollo.queries.olympiad.refetch();
        })
        .catch((error) => {
          console.error(error);
        });
      this.$store.commit("STOP_LOADING");
    },
    onLink() {
      this.$router.push({
        name: "OlympiadMembers",
        params: { id: this.olympiad.id },
      });
    },
    formatDate(date) {
      if (!date) return null;
      const [year, month, day] = date.split("-");
      return `${day}.${month}.${year}`;
    },
    onEdit() {
      if (this.edit) {
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

        let subjectsArr = [];
        if (
          this.olympiad.olympiadSubject != null &&
          this.olympiad.olympiadSubject != undefined &&
          this.olympiad.olympiadSubject.length != 0
        ) {
          this.olympiad.olympiadSubject.forEach((element) => {
            subjectsArr.push(element.subject);
          });
        }
        let newSubjects = this.form.subjects.filter((sub) =>
          subjectsArr.every((item) => item.id !== sub.id)
        );
        let deletedSubjects = subjectsArr.filter((sub) =>
          this.form.subjects.every((item) => item.id !== sub.id)
        );
        let tasksArr = [];
        if (this.olympiad.olympiadTask.length != 0) {
          this.olympiad.olympiadTask.forEach((element) => {
            tasksArr.push(element);
          });
        }

        let newTasks = this.tasks.filter((t) =>
          tasksArr.every((item) => item.id !== t.id)
        );
        let deletedTasks = tasksArr.filter((t) =>
          this.tasks.every((item) => {
            return item.id !== t.id;
          })
        );
        let updatedTasks = this.tasks.filter((t) =>
          newTasks.every((item) => item.id !== t.id)
        );
        this.$apollo
          .mutate({
            mutation: UPDATE_OLYMPIAD,
            variables: {
              olympiadId: this.olympiad.id,
              name: this.form.name,
              description: this.form.description,
              dateResult: this.form.dateResult,
              dateEnd: this.form.dateEnd,
              percentToWin: this.form.percentToWin,
            },
          })
          .then(() => {
            newSubjects.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: CREATE_OLYMPIAD_SUBJECT,
                  variables: {
                    subjectId: element.id,
                    olympiadId: this.olympiad.id,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });
            deletedSubjects.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: DELETE_OLYMPIAD_SUBJECT,
                  variables: {
                    subjectId: element.id,
                    olympiadId: this.olympiad.id,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });
            newTasks.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: CREATE_TASK,
                  variables: {
                    task: element.task,
                    maxScore: element.maxScore,
                    order: element.order,
                    olympiadId: this.$route.params.id,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });
            deletedTasks.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: DELETE_TASK,
                  variables: {
                    taskId: element.id,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });
            updatedTasks.forEach((element) => {
              this.$apollo
                .mutate({
                  mutation: UPDATE_TASK,
                  variables: {
                    taskId: element.id,
                    task: element.task,
                    maxScore: element.maxScore,
                    order: element.order,
                  },
                })
                .then(() => {})
                .catch((error) => {
                  console.error(error);
                });
            });

            this.$apollo.queries.olympiad.refresh();
            this.$apollo.queries.olympiad.refetch();
            this.edit = false;
            this.submittedForm = false;
          })
          .catch((error) => {
            console.error(error);
          });
        this.$store.commit("STOP_LOADING");
      } else {
        this.$store.commit("START_LOADING");

        this.edit = true;
        this.form.name = this.olympiad.name;
        this.form.description = this.olympiad.description;
        this.form.dateResult = this.olympiad.dateResult;
        this.form.dateEnd = this.olympiad.dateEnd;
        this.form.percentToWin = this.olympiad.percentToWin;
        if (
          this.olympiad.olympiadSubject != null &&
          this.olympiad.olympiadSubject != undefined &&
          this.olympiad.olympiadSubject.length != 0
        ) {
          let subjectsArr = [];
          this.olympiad.olympiadSubject.forEach((element) => {
            subjectsArr.push(element.subject);
          });
          this.form.subjects = subjectsArr;
        }

        if (this.olympiad.olympiadTask.length != 0) {
          let taskArr = [];
          this.olympiad.olympiadTask.forEach((element) => {
            taskArr.push(element);
          });
          this.tasks = taskArr;
        }
        this.$store.commit("STOP_LOADING");
      }
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
