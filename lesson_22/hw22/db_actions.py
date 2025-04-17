from db_core import StudentsDatabase
from pprint import pprint


if __name__ == '__main__':
    # Connect to database class with methods
    database = StudentsDatabase()

    # Retrieve all students with courses from DB
    pprint(database.get_all_students())

    # Add student
    new_student = database.add_student(name='Mad Max', age=35)
    pprint(new_student)

    # Check if new student added to DB
    pprint(database.get_all_students())

    # Add student to the course
    add_to_the_course = database.add_student_to_course(student_name='Mad Max', course_title='Physics')
    pprint(add_to_the_course)

    # Check if student added to the course
    pprint(database.get_all_students())

    # Remove student from the course
    remove_student = database.remove_student_from_course(student_name='Mad Max', course_title='Physics')
    pprint(remove_student)

    # Check if student removed from the course
    pprint(database.get_all_students())

    # Retrieve all assigned courses for student
    get_courses = database.get_courses_for_student(student_name='Gopalkrishna Gokhale')
    print(get_courses)

    # Retrieve all students assigned to the course
    get_students = database.get_students_on_course(course_title='Physics')
    print(get_students)
