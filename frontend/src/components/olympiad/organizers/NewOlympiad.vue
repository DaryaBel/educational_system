<template>
  <div>
    <loader v-if="isLoading"></loader>
    <div v-else>
      <h1>Создать олимпиаду</h1>
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
          :class="{ 'is-invalid': submittedForm && $v.form.description.$error }"
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
          <span v-if="!$v.form.subjects.required">Данное поле обязательно</span>
        </div>
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
          :class="{ 'is-invalid': submittedForm && $v.form.dateResult.$error }"
        />
      </div>
      <div>
        <h4>Задания</h4>
        <div
          v-for="(task, i) in sortedTasks"
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

            <div v-if="submittedForm && v.task.$error" class="invalid-feedback">
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

      <button @click="onAdd">Сохранить</button>
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
.border-line {
  border: 1px solid palevioletred;
}
</style>
