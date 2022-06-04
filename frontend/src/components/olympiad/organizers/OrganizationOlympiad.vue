<template>
  <div>
    <p v-if="isLoading || olympiad == undefined">Загрузка...</p>
    <div v-else>
      <div v-if="!edit">
        <h1>{{ olympiad.name }}</h1>
        <p>
          <span
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
          <h4 v-if="olympiad.olympiadTask.length == 0">
            К данной олимпиаде пока не добавлено заданий
          </h4>
          <div v-else>
            <div v-for="task in sortedTasks" :key="task.id">
              <h4>Задание {{ task.order }}.</h4>
              <p>{{ task.task }}</p>
              <p>Максиальный балл: {{ task.maxScore }}</p>
            </div>
          </div>
        </div>
        <p v-if="olympiad.published">Опубликовано</p>
        <p v-if="!olympiad.published">Не опубликовано</p>
        <button
          @click="
            modal = true;
            modalId = olympiad.id;
            modalName = olympiad.name;
          "
        >
          Удалить
        </button>
        <button v-if="!olympiad.published" @click="onEdit">
          Отредактировать
        </button>
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
        <button @click="onLink">Посмотреть участников</button>
      </div>
      <div v-else>
        <h1>Редактирование олимпиады</h1>
        <div class="form-group">
          <label for="name">Название *</label><br />
          <input
            id="name"
            name="name"
            type="text"
            v-model.trim="form.name"
            :class="{ 'is-invalid': submittedForm && $v.form.name.$error }"
          />
          <div
            v-if="submittedForm && $v.form.name.$error"
            class="invalid-feedback"
          >
            <span v-if="!$v.form.name.required">Данное поле обязательно</span>
          </div>
        </div>
        <div class="form-group">
          <label for="description">Описание </label><br />
          <textarea
            name="description"
            id="description"
            cols="30"
            rows="10"
            v-model.trim="form.description"
            :class="{
              'is-invalid': submittedForm && $v.form.description.$error,
            }"
          ></textarea>
        </div>
        <div class="form-group">
          <label for="subjects">Предметы *</label><br />
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
          <div
            v-if="submittedForm && $v.form.subjects.$error"
            class="invalid-feedback"
          >
            <span v-if="!$v.form.subjects.required"
              >Данное поле обязательно</span
            >
          </div>
        </div>
        <div class="form-group">
          <label for="dateEnd">Дата окончания приема ответов</label><br />
          <input
            id="dateEnd"
            name="dateEnd"
            type="date"
            v-model="form.dateEnd"
            :class="{ 'is-invalid': submittedForm && $v.form.dateEnd.$error }"
          />
        </div>
        <div class="form-group">
          <label for="dateResult">Дата оглашения результатов</label><br />
          <input
            id="dateResult"
            name="dateResult"
            type="date"
            v-model="form.dateResult"
            :class="{
              'is-invalid': submittedForm && $v.form.dateResult.$error,
            }"
          />
        </div>
        <div class="form-group">
          <label for="percentToWin">Необходимое количество % для победы *</label
          ><br />
          <input
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
          <div
            v-if="submittedForm && $v.form.percentToWin.$error"
            class="invalid-feedback"
          >
            <span v-if="!$v.form.percentToWin.required"
              >Данное поле обязательно</span
            >
            <span v-if="!$v.form.percentToWin.betweenValue"
              >Число должно находиться в отрезке от 1 до 100</span
            >
          </div>
        </div>
        <div>
          <h4>Задания</h4>
          <div
            v-for="(task, i) in sortedEditTasks"
            :key="i"
            :set="(v = $v.tasks.$each[i])"
          >
            <div class="form-group">
              <label for="task">Текст задания *</label><br />
              <textarea
                name="task"
                id="task"
                cols="30"
                rows="10"
                v-model.trim="task.task"
                :class="{
                  'is-invalid': submittedForm && v.task.$error,
                }"
              ></textarea>

              <div
                v-if="submittedForm && v.task.$error"
                class="invalid-feedback"
              >
                <span v-if="!v.task.required">Данное поле обязательно</span>
              </div>
            </div>
            <div class="form-group">
              <label for="maxScore">Максимальный балл *</label><br />
              <input
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
              <div
                v-if="submittedForm && v.maxScore.$error"
                class="invalid-feedback"
              >
                <span v-if="!v.maxScore.required">Данное поле обязательно</span>
                <span v-if="!v.maxScore.betweenValue"
                  >Число должно находиться в отрезке от 1 до 100</span
                >
              </div>
            </div>
            <button
              v-if="tasks.length != 1"
              :disabled="task.order == 1"
              @click="toUp(task.order)"
            >
              Вверх
            </button>
            <button
              v-if="tasks.length != 1"
              :disabled="task.order == tasks.length"
              @click="toDown(task.order)"
            >
              Вниз
            </button>
            <button
              v-if="tasks.length != 1"
              @click="deleteFromLocalTasks(task.order)"
            >
              Удалить
            </button>
          </div>
          <button
            @click="
              tasks.push({
                task: undefined,
                maxScore: undefined,
                order: tasks.length + 1,
              })
            "
          >
            Добавить
          </button>
        </div>
        <p>* - обязательное поле</p>
        <button @click="onEdit">Сохранить</button>
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
      userId: 2,
      organizationId: 4,
      submittedForm: false,
      isLoading: false,
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
    },
    sortByOrder(d1, d2) {
      return d1.order > d2.order ? 1 : -1;
    },
    toPublish(olympiadId, published) {
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
        this.isLoading = true;
        this.submittedForm = true;
        this.$v.form.$touch();
        this.$v.tasks.$touch();
        if (this.$v.form.$invalid) {
          this.isLoading = false;
          return;
        }
        if (this.$v.tasks.$invalid) {
          this.isLoading = false;
          return;
        }
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
            this.isLoading = false;
          })
          .catch((error) => {
            console.error(error);
          });
      } else {
        this.isLoading = true;
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
        this.isLoading = false;
      }
    },
  },
};
</script>
<style src="vue-multiselect/dist/vue-multiselect.min.css"></style>
<style lang="scss"></style>
