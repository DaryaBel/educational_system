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
