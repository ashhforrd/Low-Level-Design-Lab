from enum import Enum, auto
from collections import deque
from typing import Optional
from uuid import uuid4


class EnrollmentStatus(Enum):
    ENROLLED = auto()
    WAITLISTED = auto()
    CANCELLED = auto()


class Enrollment:
    def __init__(self, enrollment_id: str, student_id: str, course_id: str) -> None:
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        self.status = EnrollmentStatus.WAITLISTED

    def promote(self) -> None:
        if self.status != EnrollmentStatus.WAITLISTED:
            raise ValueError("Only a WAITLISTED enrollment can be promoted")

        self.status = EnrollmentStatus.ENROLLED

    def cancel(self) -> None:
        if self.status == EnrollmentStatus.CANCELLED:
            raise ValueError("Enrollment is already cancelled")

        self.status = EnrollmentStatus.CANCELLED


class Course:
    def __init__(self, course_id: str, capacity: int) -> None:
        if capacity <= 0:
            raise ValueError("Capacity must be greater than zero")

        self.course_id = course_id
        self.capacity = capacity
        self.enrolled: list[Enrollment] = []
        self.waiting_list: deque[Enrollment] = deque()

    def add_enrollment(self, enrollment: Enrollment) -> None:
        if len(self.enrolled) < self.capacity:
            enrollment.promote()
            self.enrolled.append(enrollment)
        else:
            self.waiting_list.append(enrollment)

    def promote_next(self) -> Optional[Enrollment]:
        if not self.waiting_list:
            return None

        enrollment = self.waiting_list.popleft()
        enrollment.promote()
        self.enrolled.append(enrollment)

        return enrollment

    def cancel_enrollment(
        self,
        enrollment: Enrollment,
    ) -> Optional[Enrollment]:
        if enrollment.status == EnrollmentStatus.ENROLLED:
            self.enrolled.remove(enrollment)
            enrollment.cancel()

            return self.promote_next()

        if enrollment.status == EnrollmentStatus.WAITLISTED:
            self.waiting_list.remove(enrollment)
            enrollment.cancel()

            return None

        enrollment.cancel()
        return None


class CourseEnrollmentSystem:
    def __init__(self) -> None:
        self.courses: dict[str, Course] = {}
        self.enrollments: dict[str, Enrollment] = {}

    def add_course(self, course_id: str, capacity: int) -> Course:
        if course_id in self.courses:
            raise ValueError("Course already exist")

        course = Course(course_id, capacity)
        self.courses[course_id] = course

        return course

    def enroll_student(
        self,
        course_id: str,
        student_id: str,
    ) -> Enrollment:
        course = self.courses.get(course_id)

        if course is None:
            raise ValueError("Course doesn't exist")

        has_active_enrolled = any(
            enrollment.student_id == student_id
            and enrollment.course_id == course_id
            and enrollment.status in {
                EnrollmentStatus.ENROLLED,
                EnrollmentStatus.WAITLISTED,
            }
            for enrollment in self.enrollments.values()
        )

        if has_active_enrolled:
            raise ValueError("Student already has an active enrollment in this course")

        enrollment_id = str(uuid4())
        enrollment = Enrollment(enrollment_id, student_id, course_id)

        course.add_enrollment(enrollment)
        self.enrollments[enrollment_id] = enrollment

        return enrollment

    def cancel_enrollment(self, enrollment_id: str) -> Optional[Enrollment]:
        enrollment = self.enrollments.get(enrollment_id)

        if enrollment is None:
            raise ValueError("Enrollment does not exist")

        course = self.courses[enrollment.course_id]
        return course.cancel_enrollment(enrollment)

    def get_course_enrollments(
        self,
        course_id: str,
    ) -> list[Enrollment]:
        course = self.courses.get(course_id)

        if course is None:
            raise ValueError("Course does not exist")

        return course.enrolled + list(course.waiting_list)


if __name__ == "__main__":
    system = CourseEnrollmentSystem()
    course = system.add_course("PYTHON-101", capacity=2)

    first = system.enroll_student(course.course_id, "STUDENT-1")
    second = system.enroll_student(course.course_id, "STUDENT-2")
    third = system.enroll_student(course.course_id, "STUDENT-3")

    print(first.status)
    print(second.status)
    print(third.status)

    promoted = system.cancel_enrollment(first.enrollment_id)

    print(first.status)
    print(promoted.student_id if promoted else None)
    print(promoted.status if promoted else None)

    enrollments = system.get_course_enrollments(course.course_id)

    for enrollment in enrollments:
        print(enrollment.student_id, enrollment.status)