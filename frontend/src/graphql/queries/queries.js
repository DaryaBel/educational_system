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

export const COURSE = gql`
  query ($courseId: ID!) {
    course(courseId: $courseId) {
      id
      name
      published
      description
      duration
      form
      dateStart
      dateEnd
      maxNumberMember
      city {
        id
        name
      }
      courseSubject {
        subject {
          id
          name
        }
      }
      organization {
        id
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

export const PUBLISHED_COURSES = gql`
  {
    publishedCourses {
      id
      name
      description
      organization {
        id
        fullname
        shortname
        logo
      }
      form
      city {
        id
        name
      }
      courseSubject {
        subject {
          id
          name
        }
      }
    }
  }
`;

export const SUBJECTS = gql`
  {
    subjects {
      id
      name
    }
  }
`;

export const SHORT_LIST_ORGANIZATIONS = gql`
  {
    organizations {
      id
      fullname
      shortname
    }
  }
`;

export const CITIES = gql`
  {
    cities {
      id
      name
    }
  }
`;

export const STUDENT_COURSES = gql`
  query ($userId: ID!) {
    studentCourses(userId: $userId) {
      id
      name
      description
      organization {
        id
        fullname
        shortname
        logo
      }
      form
      courseSubject {
        subject {
          id
          name
        }
      }
    }
  }
`;

export const ORGANIZATION_COURSES = gql`
  query ($organizationId: ID!) {
    organizationCourses(organizationId: $organizationId) {
      id
      name
      published
      description
      form
      city {
        id
      }
      courseSubject {
        subject {
          id
          name
        }
      }
    }
  }
`;
