import gql from "graphql-tag";

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

export const UPDATE_COURSE = gql`
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

export const DELETE_COURSE = gql`
  mutation ($courseId: ID!) {
    deleteCourse(courseId: $courseId) {
      ok
    }
  }
`;
