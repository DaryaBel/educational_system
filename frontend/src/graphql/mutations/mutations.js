import gql from "graphql-tag";

export const CREATE_RESULT = gql`
  mutation ($olympiadId: ID!, $userId: ID!) {
    createResult(olympiadId: $olympiadId, userId: $userId) {
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
  mutation (
    $resultId: ID!
    $startTryTime: Int
    $finishTryTime: Int
    $status: String
  ) {
    updateResult(
      resultId: $resultId
      startTryTime: $startTryTime
      finishTryTime: $finishTryTime
      status: $status
    ) {
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

export const PUBLISH_COURSE = gql`
  mutation ($courseId: ID!, $published: Boolean) {
    updateCourse(courseId: $courseId, published: $published) {
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
