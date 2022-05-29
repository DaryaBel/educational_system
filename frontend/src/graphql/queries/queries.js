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

export const ALL_MEMBER_COURSE = gql`
  query ($courseId: ID!) {
    courseStudents(courseId: $courseId) {
      id
      student {
        id
        birthdate
        user {
          id
          email
          firstName
          lastName
        }
        patronymic
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

export const PUBLISHED_OLYMPIADS = gql`
  {
    publishedOlympiads {
      id
      name
      description
      organization {
        id
        fullname
        shortname
        logo
      }
      olympiadSubject {
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

export const STUDENT_OLYMPIADS = gql`
  query ($userId: ID!) {
    studentOlympiads(userId: $userId) {
      id
      name
      description
      organization {
        id
        fullname
        shortname
        logo
      }
      olympiadResult {
        id
        status
        student {
          id
          user {
            id
          }
        }
      }
      olympiadSubject {
        subject {
          id
          name
        }
      }
    }
  }
`;

export const OLYMPIAD = gql`
  query ($olympiadId: ID!) {
    olympiad(olympiadId: $olympiadId) {
      id
      name
      description
      organization {
        id
        kind
        fullname
        shortname
        logo
      }
      dateResult
      dateEnd
      olympiadSubject {
        subject {
          id
          name
        }
      }
    }
  }
`;

export const OLYMPIAD_RULES = gql`
  query ($olympiadId: ID!) {
    olympiad(olympiadId: $olympiadId) {
      id
      name
      olympiadTask {
        id
      }
    }
  }
`;

export const STUDENT_ANSWERS = gql`
  query ($olympiadId: ID!, $userId: ID!) {
    answers(olympiadId: $olympiadId, userId: $userId) {
      id
      answer
      task {
        id
      }
    }
  }
`;

export const OLYMPIAD_PROCESS = gql`
  query ($olympiadId: ID!) {
    olympiad(olympiadId: $olympiadId) {
      id
      name
      olympiadTask {
        id
        task
        order
      }
    }
  }
`;

export const OLYMPIAD_STATUS = gql`
  query ($olympiadId: ID!, $userId: ID!) {
    studentOlympiadResult(olympiadId: $olympiadId, userId: $userId) {
      id
      status
      published
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
