<template>
  <div>
    <h1>{{ olympiad.name }}</h1>

    <p>
      Данная олимпиада состоит из {{ olympiad.olympiadTask.length }}
      {{ formOfWord(olympiad.olympiadTask.length, 1) }} с развернутым ответом.
      Ответ можно написать в текстовом поле или приложить в данное поле ссылку
      (например, на гугл-диск). Проверьте, что ваш документ доступен для чтения
      по ссылке.
    </p>
    <p v-if="olympiad.time_to_pass != null && olympiad.time_to_pass != 0">
      На решение заданий даётся {{ formatTime(olympiad.time_to_pass) }}. Если
      работа не будет отправлена по истечению данного времени, она отправится
      автоматически.
    </p>
    <button @click="toStart()">Начать</button>
  </div>
</template>

<script>
export default {
  name: "OlympiadRules",
  data() {
    return {
      hours: "",
      minutes: "",
      seconds: "",
      olympiad: {
        name: 'Олимпиада "Инновационный полет"',
        description:
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam at ultrices enim. Maecenas id sodales libero, vitae tristique orci. Cras quis venenatis sem, laoreet pellentesque dui. Mauris faucibus neque turpis. Vivamus id sapien fermentum metus pulvinar pellentesque eget ac diam. Phasellus tristique massa non bibendum suscipit. Aliquam vel libero ut nunc ultrices maximus ac in turpis. Phasellus commodo, orci sit amet suscipit consectetur, risus est tempus felis, sed rhoncus eros lacus vitae purus. Nullam pellentesque consectetur libero, vel bibendum mauris blandit eu. Quisque hendrerit libero nec sem sollicitudin fermentum. Nullam id dui mattis, imperdiet velit vitae, placerat magna. Aliquam lobortis tempus orci, in placerat dui eleifend id. Sed sed lacus eget nulla aliquam aliquet. Nunc egestas lacus in pellentesque iaculis. Phasellus blandit efficitur lectus, sit amet finibus leo tincidunt eget. Aenean in viverra dui.",
        percent_to_win: 85,
        time_to_pass: "8147.0",
        date_end: "2022-06-05",
        date_result: "2022-07-05",
        published: true,
        subjects: [
          { id: 1, name: "Обществознание" },
          { id: 2, name: "Экономика" },
        ],
        olympiadTask: [
          { id: 1, task: "Опишите мировую экономику" },
          { id: 2, task: "Посчитайте 2+2" },
        ],
        organization: {
          fullname: "ОАО Тинькофф Банк",
          shortname: "Тинькофф",
          kind: "COMPANY",
          description:
            " российский коммерческий банк, сфокусированный полностью на дистанционном обслуживании, не имеющий розничных отделений",
          logo: "",
        },
      },
    };
  },
  methods: {
    toStart() {
      // создать результат в табличке
      let start = new Date();
      console.log(start.toLocaleTimeString());
      let delta = Math.trunc(this.olympiad.time_to_pass);
      let finish = new Date(start.setMilliseconds(delta * 1000));
      console.log(finish.toLocaleTimeString());
      this.$router.push({ name: "OlympiadProcess" });
    },
    formatTime(time) {
      if (!time) return null;
      time = Math.trunc(time);
      this.seconds = time % 60;
      time = (time - this.seconds) / 60;
      this.minutes = time % 60;
      this.hours = (time - this.minutes) / 60;
      let result;
      result = "";
      if (this.hours != 0) {
        result = result + ` ${this.hours} ${this.formOfWord(this.hours, 2)}`;
      }
      if (this.minutes != 0) {
        result =
          result + ` ${this.minutes} ${this.formOfWord(this.minutes, 3)}`;
      }
      if (this.seconds != 0) {
        result =
          result + ` ${this.seconds} ${this.formOfWord(this.seconds, 4)}`;
      }
      return result;
    },
    formOfWord(length, word) {
      // задания
      if (word == 1) {
        if (length == 1) return "задания";
        else return "заданий";
      }
      // часы
      if (word == 2) {
        if (
          length % 10 >= 2 &&
          length % 10 <= 4 &&
          length % 100 != 12 &&
          length % 100 != 13 &&
          length % 100 != 14
        )
          return "часа";
        else {
          if (
            (length % 10 >= 5 && length % 10 <= 9) ||
            (length % 100 >= 10 && length % 100 <= 20) ||
            length % 10 == 0
          )
            return "часов";
          else return "час";
        }
      }
      // минуты
      if (word == 3) {
        if (
          length % 10 >= 2 &&
          length % 10 <= 4 &&
          length % 100 != 12 &&
          length % 100 != 13 &&
          length % 100 != 14
        )
          return "минуты";
        else {
          if (
            (length % 10 >= 5 && length % 10 <= 9) ||
            (length % 100 >= 10 && length % 100 <= 20) ||
            length % 10 == 0
          )
            return "минут";
          else return "минута";
        }
      }
      // секунды
      if (word == 4) {
        if (
          length % 10 >= 2 &&
          length % 10 <= 4 &&
          length % 100 != 12 &&
          length % 100 != 13 &&
          length % 100 != 14
        )
          return "секунды";
        else {
          if (
            (length % 10 >= 5 && length % 10 <= 9) ||
            (length % 100 >= 10 && length % 100 <= 20) ||
            length % 10 == 0
          )
            return "секунд";
          else return "секунда";
        }
      }
    },
  },
};
</script>

<style lang="scss"></style>
