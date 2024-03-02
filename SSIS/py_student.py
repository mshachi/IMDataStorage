import csv
import os
import py_course as cr

# Student Information Management System class
fieldnames = ['Student_ID', 'Name', 'Age', 'Gender', 'Course', 'Year_Level']


class StudentSystem:
    def __init__(self):
        self.student = {}

    # function to create a new student record and add it to a dictionary
    def create_student(self, student_id, name, age, gender, course, year):
        self.student[student_id] = {'Student_ID': student_id, 'Name': name, 'Age': age,
                                    'Gender': gender, 'Course': course, 'Year_Level': year}
        print("Student added successfully.")
    # function to read student info (from the dictionary loaded from the csv file)
    
    def read_student(self, student_id):
        if student_id in self.student:
            student = self.student[student_id]
            print(f"Student ID: {student['Student_ID']}")
            print(f"Name: {student['Name']}")
            print(f"Age: {student['Age']}")
            print(f"Gender: {student['Gender']}")
            print(f"Course: {student['Course']}")
            print(f"Year Level: {student['Year_Level']}")
        else:
            print(f"Student {student_id} does not exist")

    # function to update student info
    def update_student(self, student_id, year, course):
        if student_id in self.student:
            self.student[student_id]['Year_Level'] = year
            self.student[student_id]['Course'] = course
        else:
            print(f"Student {student_id} does not exist.")

    # function to delete student info
    def delete_student(self, student_id):
        if student_id in self.student:
            del self.student[student_id]
        else:
            print(f"Student {student_id} does not exist.")

    # function to list student info
    def list_students(self):
        for student_id, student in self.student.items():
            print(f"Student ID: {student['Student_ID']}, Name: {student['Name']}, Age: {student['Age']}, "
                  f"Gender: {student['Gender']}, Year Level: {student['Year_Level']}, Course: {student['Course']}")

    # function to update a csv file
    def update_csvfile(self, filename):
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for student in self.student.values():
                writer.writerow(student)

    # function to load csv file
    def load_csvfile(self, filename):
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.student[row["Student_ID"]] = row
        else:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(fieldnames)


# main function
def main():
    sis = StudentSystem()
    filename = "student_csv.csv"
    course_filename = "course_csv.csv"
    sis.load_csvfile(filename)
    course_check = cr.CourseCSV(course_filename)

    while True:
        print("--Student Information System--")
        print("1. Add Student")
        print("2. View Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. List All Students")
        print("6. Add Course")
        print("7. Delete Course")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = input("Enter Student ID: ")
            if student_id in sis.student:
                print(f"Student {student_id} already exists.")
            else:
                name = input("Enter Name: ")
                age = input("Enter Age: ")
                gender = input("Enter Gender: ")
                year_level = input("Enter Year Level: ")
                course = input("Enter Course: ")
                if not course_check.valid_course(course):
                    sis.create_student(student_id, name, age, gender, "N/A", year_level)
                else:
                    sis.create_student(student_id, name, age, gender, course, year_level)

        elif choice == "2":
            student_id = input("Enter Student ID: ")
            sis.read_student(student_id)

        elif choice == "3":
            student_id = input("Enter Student ID: ")
            year = input("Enter Year Level: ")
            course = input("Enter new course: ")
            sis.update_student(student_id, year, course)
            print("Student information updated successfully.")

        elif choice == "4":
            student_id = input("Enter Student ID: ")
            sis.delete_student(student_id)
            print("Student information deleted successfully.")

        elif choice == "5":
            print("List of students: ")
            sis.list_students()

        elif choice == "6":
            course_code = input("Enter Course Code: ")
            course_name = input("Enter Course Name: ")
            if course_check.is_duplicate_course(course_code):
                print(f"Course {course_code} - {course_name} already exists.")
            else:
                course_check.add_course(course_code, course_name)
                print("Course added successfully")

        elif choice == "7":
            course_code = input("Enter Course Code: ")
            if course_check.valid_course(course_code):
                print(f"Are you sure to delete Course {course_code}")
                valid = input("Enter 'Yes' to delete. Enter any key to cancel: ")
                if valid == "Yes":
                    course_check.delete_course(course_code)
                else:
                    print("Course not deleted.")
            else:
                print("Please enter a valid course code.")

        elif choice == "8":
            exit()

        else:
            print("Please enter a valid choice.")

        sis.update_csvfile(filename)


if __name__ == "__main__":
    main()
    
