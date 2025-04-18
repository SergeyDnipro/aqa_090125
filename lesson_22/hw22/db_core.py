import random

from sqlalchemy.exc import IntegrityError

import dataset
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, Table
from sqlalchemy.orm import sessionmaker, relationship, declarative_base, joinedload


Base = declarative_base()

class StudentsDatabase:

    def __init__(self, *, db_url:str="sqlite:///students_courses.db", default_data:bool=False):
        self.engine = create_engine(db_url, echo=False)
        self.DB_session = sessionmaker(bind=self.engine)
        Base.metadata.create_all(self.engine)

        # Initiate filing database with random values
        if not default_data:
            self.fill_default_values_into_db()

    class BaseModel(Base):
        __abstract__ = True

        id = Column(Integer, primary_key=True)


    class Student(BaseModel):
        __tablename__ = 'students'

        name = Column(String, unique=True)
        age = Column(Integer)
        courses = relationship(
            lambda: StudentsDatabase.Course,
            secondary=lambda: StudentsDatabase.students_courses,
            back_populates='students'
        )

        def __repr__(self):
            return f"Student name: {self.name}, Courses: {self.courses}"

    class Course(BaseModel):
        __tablename__ = 'courses'

        title = Column(String, unique=True)
        difficulty = Column(Integer, default=-1)
        students = relationship(
            lambda: StudentsDatabase.Student,
            secondary=lambda: StudentsDatabase.students_courses,
            back_populates='courses'
        )

        def __repr__(self):
            return f"{self.title}"


    students_courses = Table(
        'students_courses',
        Base.metadata,
        Column('student_id', ForeignKey('students.id'), primary_key=True),
        Column('course_id', ForeignKey('courses.id'), primary_key=True),
    )

    def fill_default_values_into_db(self):
        """ Initiate empty database with default values."""
        with self.DB_session() as session:
            if not session.query(self.Student).first():
                courses_instances_list = []
                students_instances_list = []

                for course_name, course_difficulty in dataset.courses_list:
                    courses_instances_list.append(
                        self.Course(
                            title=course_name,
                            difficulty=course_difficulty
                        )
                    )
                session.add_all(courses_instances_list)

                for student_name, student_age in dataset.students_list:
                    # noinspection PyArgumentList
                    students_instances_list.append(
                        self.Student(
                            name=student_name,
                            age=student_age,
                            courses=random.sample(courses_instances_list, k=random.randint(1, len(courses_instances_list)))
                        )
                    )
                session.add_all(students_instances_list)
                session.commit()


    def get_all_students(self):
        """ Get all students info including courses from database"""
        with self.DB_session() as session:
            result = session.query(self.Student).options(joinedload(self.Student.courses)).all()
        return result

    def add_student(self, *, name:str, age:int):
        """ Add student to database"""
        try:
            with self.DB_session() as session:
                session.add(self.Student(name=name, age=age))
                session.commit()
                return f"Student {name} added to database"
        except IntegrityError as e:
            return f"Student {name} already exists, error: {e}"


    def add_course(self, *, title:str, difficulty:int):
        """ Add course to database"""
        try:
            with self.DB_session() as session:
                session.add(self.Course(title=title, difficulty=difficulty))
                session.commit()
                return f"Course {title} added to database"
        except IntegrityError as e:
            return f"Course {title} already exists, error: {e}"

    def add_student_to_course(self, *, student_name, course_title):
        """ Assign student to course"""
        with self.DB_session() as session:
            course = session.query(self.Course).filter_by(title=course_title).first()
            student = session.query(self.Student).filter_by(name=student_name).first()
            if student and course not in student.courses:
                student.courses.append(course)
                session.commit()
                return f"Student: {student_name} added to course: {course_title}"
            return 'Student/Course not found or Student already assigned course'

    def remove_student_from_course(self, *, student_name:str, course_title:str):
        """ Remove student from course"""
        with self.DB_session() as session:
            course = session.query(self.Course).filter_by(title=course_title).first()
            student = session.query(self.Student).filter_by(name=student_name).first()
            if student and course in student.courses:
                student.courses.remove(course)
                session.commit()
                return f"Student: {student_name} removed from course: {course_title}"
            return 'Student or Course not found'

    def remove_student_from_db(self, *, student_name:str):
        """ Remove student from database"""
        with self.DB_session() as session:
            student = session.query(self.Student).filter_by(name=student_name).first()
            if student:
                session.delete(student)
                session.commit()
                return f"Student: {student_name} removed from database"
            return 'Student not found'

    def get_courses_for_student(self, *, student_name:str):
        """ Get all assigned courses for student"""
        with self.DB_session() as session:
            student = session.query(self.Student).filter_by(name=student_name).first()
            if student:
                return f"Student: {student.name},\nCourses: {student.courses}"
            return 'No courses found for this student'

    def get_students_on_course(self, *, course_title:str):
        """ Get all students on course"""
        student_list = []
        with self.DB_session() as session:
            course = session.query(self.Course).filter_by(title=course_title).first()
            if course:
                for student in course.students:
                    student_list.append(student.name)
                return f"Course: {course.title},\nStudents: {student_list}"
            return 'No students found for this course'
