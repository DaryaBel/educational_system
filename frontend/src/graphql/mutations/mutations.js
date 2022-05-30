import gql from "graphql-tag";

export const CREATE_RESULT = gql`
  mutation ($olympiadId: ID!, $userId: ID!) {
    createResult(olympiadId: $olympiadId, userId: $userId) {
      ok
    }
  }
`;

export const CREATE_ANSWER = gql`
  mutation ($taskId: ID!, $olympiadId: ID!, $userId: ID!, $answer: String!) {
    createAnswer(
      taskId: $taskId
      olympiadId: $olympiadId
      userId: $userId
      answer: $answer
    ) {
      answer {
        id
      }
    }
  }
`;

export const UPDATE_ANSWER = gql`
  mutation ($answerId: ID!, $answer: String) {
    updateAnswer(answerId: $answerId, answer: $answer) {
      ok
    }
  }
`;

export const DELETE_ANSWER = gql`
  mutation ($answerId: ID!) {
    deleteAnswer(answerId: $answerId) {
      ok
    }
  }
`;

export const DELETE_RESULT = gql`
  mutation ($resultId: ID!) {
    deleteResult(resultId: $resultId) {
      ok
    }
  }
`;

export const UPDATE_RESULT = gql`
  mutation ($resultId: ID!, $status: String) {
    updateResult(resultId: $resultId, status: $status) {
      ok
    }
  }
`;

export const CREATE_STUDENT_COURSE = gql`
  mutation ($courseId: ID!, $userId: ID!) {
    createStudentCourse(courseId: $courseId, userId: $userId) {
      ok
    }
  }
`;

export const DELETE_STUDENT_COURSE = gql`
  mutation ($courseId: ID!, $userId: ID!) {
    deleteStudentCourse(courseId: $courseId, userId: $userId) {
      ok
    }
  }
`;

export const CREATE_COURSE_SUBJECT = gql`
  mutation ($courseId: ID!, $subjectId: ID!) {
    createCourseSubject(courseId: $courseId, subjectId: $subjectId) {
      ok
    }
  }
`;

export const DELETE_COURSE_SUBJECT = gql`
  mutation ($courseId: ID!, $subjectId: ID!) {
    deleteCourseSubject(courseId: $courseId, subjectId: $subjectId) {
      ok
    }
  }
`;

export const CREATE_OLYMPIAD_SUBJECT = gql`
  mutation ($olympiadId: ID!, $subjectId: ID!) {
    createOlympiadSubject(olympiadId: $olympiadId, subjectId: $subjectId) {
      ok
    }
  }
`;

export const DELETE_OLYMPIAD_SUBJECT = gql`
  mutation ($olympiadId: ID!, $subjectId: ID!) {
    deleteOlympiadSubject(olympiadId: $olympiadId, subjectId: $subjectId) {
      ok
    }
  }
`;

export const PUBLISH_COURSE = gql`
  mutation ($courseId: ID!, $published: Boolean) {
    updateCourse(courseId: $courseId, published: $published) {
      ok
    }
  }
`;

export const PUBLISH_OLYMPIAD = gql`
  mutation ($olympiadId: ID!, $published: Boolean) {
    updateOlympiad(olympiadId: $olympiadId, published: $published) {
      ok
    }
  }
`;

export const CREATE_COURSE = gql`
  mutation (
    $name: String!
    $form: String!
    $organizationId: ID!
    $description: String
    $duration: String
    $dateStart: Date
    $dateEnd: Date
    $cityId: ID
    $maxNumberMember: Int
  ) {
    createCourse(
      name: $name
      form: $form
      organizationId: $organizationId
      description: $description
      duration: $duration
      dateStart: $dateStart
      dateEnd: $dateEnd
      cityId: $cityId
      maxNumberMember: $maxNumberMember
    ) {
      course {
        id
      }
    }
  }
`;

export const CREATE_OLYMPIAD = gql`
  mutation (
    $name: String!
    $organizationId: ID!
    $description: String
    $dateResult: Date
    $dateEnd: Date
    $percentToWin: Int!
  ) {
    createOlympiad(
      name: $name
      organizationId: $organizationId
      description: $description
      dateResult: $dateResult
      dateEnd: $dateEnd
      percentToWin: $percentToWin
    ) {
      olympiad {
        id
      }
    }
  }
`;

export const UPDATE_COURSE = gql`
  mutation (
    $courseId: ID!
    $name: String
    $form: String
    $description: String
    $duration: String
    $dateStart: Date
    $dateEnd: Date
    $cityId: ID
    $maxNumberMember: Int
  ) {
    updateCourse(
      courseId: $courseId
      name: $name
      form: $form
      description: $description
      duration: $duration
      dateStart: $dateStart
      dateEnd: $dateEnd
      cityId: $cityId
      maxNumberMember: $maxNumberMember
    ) {
      ok
    }
  }
`;

export const DELETE_COURSE = gql`
  mutation ($courseId: ID!) {
    deleteCourse(courseId: $courseId) {
      ok
    }
  }
`;

export const DELETE_OLYMPIAD = gql`
  mutation ($olympiadId: ID!) {
    deleteOlympiad(olympiadId: $olympiadId) {
      ok
    }
  }
`;
