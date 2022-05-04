import gql from "graphql-tag";

export const PROFILE = gql`
  query profile {
    profile {
      id
      email
      firstName
      lastName
    }
  }
`;

export const COURSE_FOR_STUDENT = gql`
  query ($courseId: ID!) {
    course(courseId: $courseId) {
      id
      name
      description
      duration
      form
      dateStart
      dateEnd
      maxNumberMember
      courseSubject {
        subject {
          id
          name
        }
      }
      organization {
        shortname
        kind
      }
    }
  }
`;

export const NUMBER_MEMBER_COURSE = gql`
  query ($courseId: ID!) {
    countCourseMember(courseId: $courseId)
  }
`;

export const IS_STUDENT_COURSE_MEMBER = gql`
  query ($courseId: ID!, $userId: ID!) {
    isStudentCourseMember(courseId: $courseId, userId: $userId)
  }
`;
