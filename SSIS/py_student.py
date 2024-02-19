import csv
import os.path
import py_course as cr
import tkinter as tk

# fieldnames/column names for csv file
fieldnames = ['Student_ID', 'Name', 'Age', 'Gender', 'Course', 'Year_Level']


# Student Information Management System class
class StudentSystem:
    def __init__(self):
        self.student = {}

    # function to create a new student record and add it to a dictionary
    def create_student(self, student_id, name, age, gender, course, year):
        self.student[student_id] = {'Student_ID': student_id, 'Name': name, 'Age': age,
                                    'Gender': gender, 'Course': course, 'Year_Level': year}

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
    sys = StudentSystem()
    filename = "student_csv.csv"
    course_filename = "course_csv.csv"
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
            else:
                sys.create_student(student_id, name, age, gender, course, year_level)
            print("Student added successfully.")

        elif choice == "2":
            student_id = input("Enter Student ID: ")
            sys.read_student(student_id)

        elif choice == "3":
            student_id = input("Enter Student ID: ")
            year = input("Enter Year Level: ")
            course = input("Enter new course: ")
            sys.update_student(student_id, year, course)
            print("Student information updated successfully.")

        elif choice == "4":
            student_id = input("Enter Student ID: ")
            sys.delete_student(student_id)
            print("Student information deleted successfully.")

        elif choice == "5":
            print("List of students: ")
            sys.list_students()

        elif choice == "6":
            exit()

        else:
            print("Please enter a valid choice.")

        sys.update_csvfile(filename)


if __name__ == "__main__":
    main()
