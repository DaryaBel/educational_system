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
        logo
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

export const STUDENT = gql`
  query ($userId: ID!) {
    student(userId: $userId) {
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
`;

export const EMPLOYEE = gql`
  query ($userId: ID!) {
    employee(userId: $userId) {
      id
      organization {
        id
        logo
        fullname
      }
      position
      user {
        id
        email
        firstName
        lastName
      }
    }
  }
`;

export const OLYMPIAD_RESULTS = gql`
  query ($olympiadId: ID!) {
    results(olympiadId: $olympiadId) {
      id
      status
      olympiad {
        id
        resultPublished
      }
      won
      score
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

export const NUMBER_NOT_CHECKED_RESULTS = gql`
  query ($olympiadId: ID!) {
    countNotCheckedResults(olympiadId: $olympiadId)
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
        logo
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
        logo
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
      logo
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
        logo
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
      resultPublished
      organization {
        logo
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
        logo
        id
        kind
        fullname
        shortname
        logo
      }
      dateResult
      dateEnd
      resultPublished
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

export const STUDENT_ANSWERS_WITH_TASK = gql`
  query ($olympiadId: ID!, $userId: ID!) {
    answers(olympiadId: $olympiadId, userId: $userId) {
      id
      answer
      score
      task {
        id
        maxScore
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

export const OLYMPIAD_TASK_CHECK = gql`
  query ($olympiadId: ID!) {
    olympiad(olympiadId: $olympiadId) {
      id
      percentToWin
      resultPublished
      olympiadTask {
        id
        task
        maxScore
        order
      }
    }
  }
`;

export const OLYMPIAD_FOR_ORGANIZERS = gql`
  query ($olympiadId: ID!) {
    olympiad(olympiadId: $olympiadId) {
      id
      name
      description
      resultPublished
      published
      percentToWin
      dateResult
      dateEnd
      olympiadSubject {
        subject {
          id
          name
        }
      }
      olympiadTask {
        id
        task
        maxScore
        order
      }
    }
  }
`;

export const OLYMPIAD_STATUS = gql`
  query ($olympiadId: ID!, $userId: ID!) {
    result(olympiadId: $olympiadId, userId: $userId) {
      id
      status
    }
  }
`;

export const RESULT_WITH_ANSWERS = gql`
  query ($userId: ID!, $olympiadId: ID!) {
    result(userId: $userId, olympiadId: $olympiadId) {
      id
      student {
        id
        user {
          id
          lastName
          firstName
        }
        patronymic
      }
      score
      status
      won
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

export const ORGANIZATION_OLYMPIADS = gql`
  query ($organizationId: ID!) {
    organizationOlympiads(organizationId: $organizationId) {
      id
      name
      published
      description
      percentToWin
      dateResult
      dateEnd
      olympiadTask {
        id
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
