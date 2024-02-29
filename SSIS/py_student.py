import csv
import os.path
import py_course as cr
import tkinter as tk

# fieldnames/column names for csv file
fieldnames = ['Student_ID', 'Name', 'Age', 'Gender', 'Course', 'Year_Level']
@@ -16,6 +15,7 @@ def __init__(self):
    def create_student(self, student_id, name, age, gender, course, year):
        self.student[student_id] = {'Student_ID': student_id, 'Name': name, 'Age': age,
                                    'Gender': gender, 'Course': course, 'Year_Level': year}
        print("Student added successfully.")

    # function to read student info (from the dictionary loaded from the csv file)
    def read_student(self, student_id):
@@ -80,36 +80,33 @@ def main():
    sys.load_csvfile(filename)
    course_check = cr.CourseCSV(course_filename)

    window = tk.Tk()
    label = tk.Label(text="Python rocks!")
    label.pack()

    window.mainloop()

    while True:
        print("--Student Information System--")
        print("1. Add Student")
        print("2. View Student")
        print("3. Update Student")
        print("4. Delete Student")
        print("5. List All Students")
        print("6. Exit")
        print("6. Add Course")
        print("7. Delete Course")
        print("8. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            student_id = input("Enter Student ID: ")
            name = input("Enter Name: ")
            age = input("Enter Age: ")
            gender = input("Enter Gender: ")
            year_level = input("Enter Year Level: ")
            course = input("Enter Course: ")
            course_check.valid_course(course)
            if not course_check.valid:
                sys.create_student(student_id, name, age, gender, "N/A", year_level)
            if student_id in sys.student:
                print(f"Student {student_id} already exists.")
            else:
                sys.create_student(student_id, name, age, gender, course, year_level)
            print("Student added successfully.")
                name = input("Enter Name: ")
                age = input("Enter Age: ")
                gender = input("Enter Gender: ")
                year_level = input("Enter Year Level: ")
                course = input("Enter Course: ")
                if not course_check.valid_course(course):
                    sys.create_student(student_id, name, age, gender, "N/A", year_level)
                else:
                    sys.create_student(student_id, name, age, gender, course, year_level)

        elif choice == "2":
            student_id = input("Enter Student ID: ")
@@ -132,6 +129,27 @@ def main():
            sys.list_students()

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
        sys.update_csvfile(filename)
if __name__ == "__main__":
    main()
