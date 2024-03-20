"""
File: py_student.py
Author: Febe Gwyn R. Belvis
Description: A Python program for a simple student information manager.
"""

import csv
from PyQt5 import QtWidgets, uic
import os.path
from py_course import CourseCSV

# fieldnames/column names for csv file
student_fieldnames = ['Student_ID', 'Name', 'Age', 'Gender', 'Course', 'Year_Level']
course_fieldnames = ['Course_Code', 'Course_Name']
student_filename = "student_csv.csv"
course_filename = "course_csv.csv"

# categories to search student by
searchStudentBy = ['ID Number', 'Name', 'Year Level', 'Course']

student = {}
course = {}

# main UI class
class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow_ui.ui', self)
        self.show()

        # load student and course info from the CSV files
        self.load_student_csvfile(student_filename)
        self.load_course_csvfile(course_filename)
        self.course_csv = CourseCSV(course_filename)

        # connect UI widgets/elements to their functions
        self.addStudent = self.findChild(QtWidgets.QPushButton, 'addStudent')
        self.addStudent.clicked.connect(self.open_add_student_dialog)

        self.deleteStudent = self.findChild(QtWidgets.QPushButton, 'deleteStudent')
        self.deleteStudent.clicked.connect(self.open_delete_student_dialog)

        self.editStudent = self.findChild(QtWidgets.QPushButton, 'editStudent')
        self.editStudent.clicked.connect(self.open_edit_student_dialog)

        self.refreshButton = self.findChild(QtWidgets.QPushButton, 'reloadButton')
        self.refreshButton.clicked.connect(self.refresh_student_tree)
        self.refreshButton.clicked.connect(self.refresh_course_tree)
        self.studentTree = self.findChild(QtWidgets.QTreeWidget, 'studentTree')
        self.studentTree.itemClicked.connect(self.clear_student_selection)

        self.courseTree = self.findChild(QtWidgets.QTreeWidget, 'courseTree')
        self.courseTree.itemClicked.connect(self.clear_course_selection)

        self.searchCourse = self.findChild(QtWidgets.QLineEdit, 'searchCourseField')
        self.searchCourse.textChanged.connect(self.filter_course_tree)

        self.addCourse = self.findChild(QtWidgets.QPushButton, 'addCourse')
        self.addCourse.clicked.connect(self.open_add_course_dialog)

        self.editCourse = self.findChild(QtWidgets.QPushButton, 'editCourse')
        self.editCourse.clicked.connect(self.open_edit_course_dialog)

        self.deleteCourse = self.findChild(QtWidgets.QPushButton, 'deleteCourse')
        self.deleteCourse.clicked.connect(self.open_delete_course_dialog)

        self.searchComboBox = self.findChild(QtWidgets.QComboBox, 'searchComboBox')
        self.searchComboBox.addItems(searchStudentBy)

        self.searchStudent = self.findChild(QtWidgets.QLineEdit, 'searchStudentField')
        self.get_search_by()
        self.searchComboBox.currentTextChanged.connect(self.get_search_by)
        self.searchStudent.textChanged.connect(self.filter_student_tree)

    # connecting functionality methods
    def get_search_by(self):
        searchBy = self.searchComboBox.currentText()
        if searchBy == "Course":
            self.searchStudent.setPlaceholderText(f"Enter {searchBy} code")
        else:
            self.searchStudent.setPlaceholderText(f"Enter {searchBy}")

    def open_add_student_dialog(self):
        self.add_student_dialog = AddStudentDialog(self)
        self.add_student_dialog.accepted.connect(self.refresh_student_tree)
        self.add_student_dialog.exec_()

    def open_add_course_dialog(self):
        self.add_course_dialog = AddCourseDialog(self)
        self.add_course_dialog.accepted.connect(self.refresh_course_tree) 
        self.add_course_dialog.exec_()

    def open_edit_course_dialog(self):
        course_selected_item = self.courseTree.currentItem()
        if course_selected_item is not None:
            course_code = course_selected_item.text(0)
            course_name = course_selected_item.text(1)
            self.edit_course_dialog = EditCourseDialog(self, course_code, course_name)
            self.edit_course_dialog.accepted.connect(self.refresh_course_tree)
            self.edit_course_dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, 'No Course Selected', "Please select a Course to delete.")

    def open_delete_student_dialog(self):
        student_selected_item = self.studentTree.currentItem()
        if student_selected_item is not None:
            student_id = student_selected_item.text(0)
            confirm = QtWidgets.QMessageBox.question(
                self, 'Confirm Deletion',
                f"Do you want to delete Student {student_id}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm == QtWidgets.QMessageBox.Yes:
                del student[student_id]
                self.update_student_csvfile(student_filename)
                self.refresh_student_tree()

        else:
            QtWidgets.QMessageBox.warning(self, 'No Student Selected', "Please select a student to delete.")

    def open_delete_course_dialog(self):
        course_selected_item = self.courseTree.currentItem()
        if course_selected_item is not None:
            course_code = course_selected_item.text(0)
            confirm = QtWidgets.QMessageBox.question(
                self, 'Confirm Deletion',
                f"Do you want to delete Course {course_code}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
            )

            if confirm == QtWidgets.QMessageBox.Yes:
                if confirm == QtWidgets.QMessageBox.Yes:
                    # update the course dictionary to reflect the deletion
                    del course[course_code]  # remove the course from the in-memory dictionary

                    # update the student CSV file and student tree
                    self.update_student_csvfile_with_deleted_course(student_filename, course_code)
                    self.refresh_student_tree()

                    # update the course CSV file
                    self.update_course_csvfile(course_filename)

                    # refresh the course tree
                    self.refresh_course_tree()
        else:
            QtWidgets.QMessageBox.warning(self, 'No Course Selected', "Please select a Course to delete.")

    def update_student_csvfile_with_deleted_course(self, filename, deleted_course_code):
        global student
        for student_id, student_data in student.items():
            if student_data['Course'] == deleted_course_code:
                student_data['Course'] = 'N/A'

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=student_fieldnames)
            writer.writeheader()
            for student_data in student.values():
                writer.writerow(student_data)

    def open_edit_student_dialog(self):
        selected_item = self.studentTree.currentItem()
        if selected_item is not None:
            student_id = selected_item.text(0)
            self.edit_student_dialog = EditStudentDialog(self, student_id)
            self.edit_student_dialog.accepted.connect(self.refresh_student_tree)
            self.edit_student_dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, 'No Student Selected', "Please select a student to edit.")

    def read_course_codes(self):
        course_codes = []
        global course_filename
        if os.path.exists(course_filename):
            with open(course_filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)  # Skip header
                for row in reader:
                    course_codes.append(row[0]) 
        return course_codes

    def load_student_csvfile(self, filename):
        global student
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    student[row["Student_ID"]] = row
                    self.add_student_to_tree(row)
        else:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(student_fieldnames)

    def load_course_csvfile(self, filename):
        global course_fieldnames
        if os.path.exists(filename):
            with open(filename, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    course_code = row['Course_Code']
                    course_name = row['Course_Name']
                    course[course_code] = course_name
                    self.add_course_to_tree(course_code, course_name)
        else:
            with open(filename, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=course_fieldnames)
                writer.writeheader()

    def update_student_csvfile(self, filename):
        global student
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=student_fieldnames)
            writer.writeheader()
            for student_data in student.values():
                writer.writerow(student_data)

    def update_course_csvfile(self, filename):
        global course
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=course_fieldnames)
            writer.writeheader()
            for course_code, course_name in course.items():
                writer.writerow({'Course_Code': course_code, 'Course_Name': course_name})

    def filter_course_tree(self, text):
        filtered_courses = {}
        for course_code, course_name in course.items():
            if text.lower() in course_code.lower() or text.lower() in course_name.lower():
                filtered_courses[course_code] = course_name

        # update the course tree view with the filtered data
        self.update_course_tree(filtered_courses)

    def filter_student_tree(self, text):

        # Filter student data based on the selected category to search student by
        search_by = self.searchComboBox.currentText()
        filtered_students = {}

        for student_id, student_data in student.items():
            if search_by == 'ID Number' and text.lower() in student_id.lower():
                filtered_students[student_id] = student_data
            elif search_by == 'Name' and text.lower() in student_data['Name'].lower():
                filtered_students[student_id] = student_data
            elif search_by == 'Year Level' and text.lower() in student_data['Year_Level'].lower():
                filtered_students[student_id] = student_data
            elif search_by == 'Course' and text.lower() in student_data['Course'].lower():
                filtered_students[student_id] = student_data

        # Update the student tree view with the filtered data
        self.update_student_tree(filtered_students)

    def update_student_tree(self, students):
        # Clear the student tree view
        self.studentTree.clear()

        # add filtered students to the tree view
        for student_data in students.values():
            self.add_student_to_tree(student_data)

    def update_course_tree(self, courses):
        # clear the course tree view
        self.courseTree.clear()

        # add filtered courses to the tree view
        for course_code, course_name in courses.items():
            self.add_course_to_tree(course_code, course_name)

    def add_course_to_tree(self, course_code, course_name):
        item = QtWidgets.QTreeWidgetItem(self.courseTree)
        item.setText(0, course_code)
        item.setText(1, course_name)

    def add_student_to_tree(self, student_data):
        item = QtWidgets.QTreeWidgetItem(self.studentTree)
        item.setText(0, student_data['Student_ID'])
        item.setText(1, student_data['Name'])
        item.setText(2, student_data['Age'])
        item.setText(3, student_data['Gender'])
        item.setText(4, student_data['Year_Level'])
        item.setText(5, student_data['Course'])

    def refresh_course_tree(self):
        self.courseTree.clear()
        self.load_course_csvfile(course_filename)

    def refresh_student_tree(self):
        self.studentTree.clear()
        self.load_student_csvfile(student_filename)

    def clear_student_selection(self, item):
        if not item:
            self.studentTree.clearSelection()

    def clear_course_selection(self, item):
        if not item:
            self.courseTree.clearSelection()

# AddStudentDialog class for adding a new student
class AddStudentDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AddStudentDialog, self).__init__(parent)
        uic.loadUi('addstudent_ui.ui', self)
        self.parent = parent
        self.load_course_codes()
        self.add = self.findChild(QtWidgets.QPushButton, 'addStudent_confirm')
        self.add.clicked.connect(self.add_student)
        self.cancelAdd.clicked.connect(self.reject)

    def add_student(self):
        global student
        studentID = self.addIDNumField.text()
        name = self.addNameField.text()
        age = str(self.ageSpinBox.value())
        gender = self.get_gender()
        course = self.get_course()
        yearLevel = str(self.yearSpinBox.value())

        if studentID in student: # checking if the input student id number already exists in the list of students (from student csv file)
            QtWidgets.QMessageBox.warning(self, "Duplicate Student ID", f"Student with ID {studentID} already exists.")
            return

        student_data = {'Student_ID': studentID, 'Name': name, 'Age': age,
                        'Gender': gender, 'Course': course, 'Year_Level': yearLevel} 

        student[studentID] = student_data
        self.parent.update_student_csvfile(student_filename)
        self.accept()

    def get_course(self):
        return self.courseComboBox.currentText()

    # loading course codes from course CSV file for the combobox 
    def load_course_codes(self):
        course_filename = "course_csv.csv"
        if os.path.exists(course_filename):
            with open(course_filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                course_codes = [row[0] for row in reader]
                self.courseComboBox.addItems(course_codes)

    # retrieving gender from the checked gender radio button
    def get_gender(self):
        if self.maleRadBut.isChecked():
            return "Male"
        elif self.femaleRadBut.isChecked():
            return "Female"
        else:
            print("Error: No gender selected.")
            return ""


# EditStudentDialog for editing an existing student
class EditStudentDialog(QtWidgets.QDialog):
    global student

    def __init__(self, parent, student_id):
        super(EditStudentDialog, self).__init__(parent)
        uic.loadUi('editstudent_ui.ui', self)
        self.student_id = student_id
        self.parent = parent
        self.load_course_codes()
        self.add = self.findChild(QtWidgets.QPushButton, 'editStudent_confirm')
        self.add.clicked.connect(self.edit_student)
        self.cancelAdd.clicked.connect(self.reject)

        # set default values for field editors
        name = student[student_id]['Name']
        age = int(student[student_id]['Age'])
        gender = student[student_id]['Gender']
        course = student[student_id]['Course']
        yearLevel = int(student[student_id]['Year_Level'])

        self.nameField = self.findChild(QtWidgets.QLineEdit, 'addNameField')
        self.nameField.setText(name)

        self.ageSpinBox = self.findChild(QtWidgets.QSpinBox, 'ageSpinBox')
        self.ageSpinBox.setValue(age)

        self.maleRad = self.findChild(QtWidgets.QRadioButton, 'maleRadBut')
        self.femaleRad = self.findChild(QtWidgets.QRadioButton, 'femaleRadBut')
        if gender == 'Female':
            self.femaleRad.setChecked(True)
        elif gender == 'Male':
            self.maleRad.setChecked(True)

        self.courseBox = self.findChild(QtWidgets.QComboBox, 'courseComboBox')
        self.courseBox.setCurrentText(course)

        self.yearSpinBox = self.findChild(QtWidgets.QSpinBox, 'yearSpinBox')
        self.yearSpinBox.setValue(yearLevel)

    def edit_student(self):
        name = self.addNameField.text()
        age = str(self.ageSpinBox.value())
        gender = self.get_gender()
        course = self.get_course()
        yearLevel = str(self.yearSpinBox.value())

        student_data = {'Student_ID': self.student_id, 'Name': name, 'Age': age,
                        'Gender': gender, 'Course': course, 'Year_Level': yearLevel}

        student[self.student_id] = student_data
        self.parent.update_student_csvfile(student_filename)
        self.accept()

    def get_course(self):
        return self.courseComboBox.currentText()

    def load_course_codes(self):
        course_filename = "course_csv.csv"
        if os.path.exists(course_filename):
            with open(course_filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                course_codes = [row[0] for row in reader]
                self.courseComboBox.addItems(course_codes)

    def get_gender(self):
        if self.maleRadBut.isChecked():
            return "Male"
        elif self.femaleRadBut.isChecked():
            return "Female"
        else:
            print("Error: No gender selected.")
            return ""


# AddCourseDialog class for adding a new course
class AddCourseDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AddCourseDialog, self).__init__(parent)
        uic.loadUi('addcourse_ui.ui', self)
        self.parent = parent
        self.course_csv = CourseCSV(course_filename) 
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'addCourseConfirm')
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'cancelCourse')
        self.confirmButton.clicked.connect(self.confirm_course)
        self.cancelButton.clicked.connect(self.reject)

    def confirm_course(self):
        course_code = self.courseCodeField.text()
        course_name = self.courseNameField.text()
        if not self.course_csv.is_duplicate_course(course_code):  
            self.course_csv.add_course(course_code, course_name)  
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Course Duplicate', f"Course {course_code} already exists.")


# EditCourseDialog class for editing an existing course
class EditCourseDialog(QtWidgets.QDialog):

    def __init__(self, parent, course_code, course_name):
        super(EditCourseDialog, self).__init__(parent)
        uic.loadUi('editcourse_ui.ui', self)
        self.parent = parent
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'editCourseConfirm')
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'cancelEditCourse')
        self.confirmButton.clicked.connect(self.edit_course)
        self.cancelButton.clicked.connect(self.reject)

        self.course_code = course_code
        self.course_name = course_name

        # set default values for the input fields
        self.courseCodeField = self.findChild(QtWidgets.QLineEdit, 'courseCodeField')
        self.courseCodeField.setText(self.course_code)
        self.courseNameField = self.findChild(QtWidgets.QLineEdit, 'courseNameField')
        self.courseNameField.setText(self.course_name)

    def edit_course(self):
        new_course_code = self.courseCodeField.text()
        new_course_name = self.courseNameField.text()
        if new_course_code != self.course_code:  
            if self.parent.course_csv.is_duplicate_course(new_course_code):
                QtWidgets.QMessageBox.warning(self, 'Course Duplicate', f"Course {new_course_code} already exists.")
                return
        self.parent.course_csv.edit_course(self.course_code, new_course_code, new_course_name)
        self.accept()


# DeleteStudentDialog class for deleting a student
class DeleteStudentDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(DeleteStudentDialog, self).__init__(parent)
        self.parent = parent
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'deleteStudentConfirm')
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'cancelDelete')
        self.confirmButton.clicked.connect(self.confirm_delete)
        self.cancelButton.clicked.connect(self.reject)

    def confirm_delete(self):
        global student
        studentID = self.delIDNumField.text()

        if studentID in student:
            confirm = QtWidgets.QMessageBox.question(self, 'Confirm Deletion',
                                                     f"Do you want to delete Student {studentID}?",
                                                     QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

            if confirm == QtWidgets.QMessageBox.Yes:
                del student[studentID]
                self.parent.update_student_csvfile(student_filename)
                self.accept()

        else:
            QtWidgets.QMessageBox.warning(self, 'Student Not Found', f"Student {studentID} does not exist.")


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui()
    app.exec_()
