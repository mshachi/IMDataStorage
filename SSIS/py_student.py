import csv
from PyQt5 import QtWidgets, uic
import os.path
from py_course import CourseCSV

# fieldnames/column names for csv file
student_fieldnames = ['Student_ID', 'Name', 'Age', 'Gender', 'Course', 'Year_Level']
course_fieldnames = ['Course_Code', 'Course_Name']
student_filename = "student_csv.csv"
course_filename = "course_csv.csv"
student = {}
course = {}


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow_ui.ui', self)
        self.show()
        self.load_student_csvfile(student_filename)
        self.load_course_csvfile(course_filename)
        self.course_csv = CourseCSV(course_filename)

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

        self.searchStudent = self.findChild(QtWidgets.QLineEdit, 'searchStudentField')
        self.searchStudent.textChanged.connect(self.filter_student_tree)

        self.searchCourse = self.findChild(QtWidgets.QLineEdit, 'searchCourseField')
        self.searchCourse.textChanged.connect(self.filter_course_tree)

        self.addCourse = self.findChild(QtWidgets.QPushButton, 'addCourse')
        self.addCourse.clicked.connect(self.open_add_course_dialog)

        self.deleteCourse = self.findChild(QtWidgets.QPushButton, 'deleteCourse')
        self.deleteCourse.clicked.connect(self.open_delete_course_dialog)

    def open_add_student_dialog(self):
        self.add_student_dialog = AddStudentDialog(self)
        self.add_student_dialog.accepted.connect(self.refresh_student_tree)
        self.add_student_dialog.exec_()

    def open_add_course_dialog(self):
        self.add_course_dialog = AddCourseDialog(self)
        self.add_course_dialog.accepted.connect(self.refresh_course_tree)  # Corrected signal connection
        self.add_course_dialog.exec_()

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
                    # Delete the course from the course CSV file
                    self.course_csv.delete_course(course_code)

                    # Update the course dictionary to reflect the deletion
                    del course[course_code]  # Remove the course from the in-memory dictionary

                    # Update the student CSV file and student tree
                    self.update_student_csvfile_with_deleted_course(student_filename, course_code)
                    self.refresh_student_tree()

                    # Refresh the course tree
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
            if student_id in student:
                # Read course codes from course_csv.csv
                course_codes = self.read_course_codes()

                # Create a QComboBox and populate it with course codes
                course_combobox = QtWidgets.QComboBox()
                course_combobox.addItems(course_codes)

                # Create a dialog for editing student information
                edit_dialog = QtWidgets.QDialog(self)
                edit_dialog.setWindowTitle('Edit Student')
                layout = QtWidgets.QFormLayout()
                layout.addRow('Course:', course_combobox)
                year_level_spinbox = QtWidgets.QSpinBox()
                year_level_spinbox.setMinimum(1)
                year_level_spinbox.setMaximum(4)
                layout.addRow('Year Level:', year_level_spinbox)
                buttons = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
                layout.addWidget(buttons)
                edit_dialog.setLayout(layout)

                def accept():
                    new_course = course_combobox.currentText()
                    new_year_level = year_level_spinbox.value()
                    student[student_id]['Course'] = new_course
                    student[student_id]['Year_Level'] = str(new_year_level)
                    # Update CSV file
                    self.update_student_csvfile(student_filename)
                    # Refresh student tree
                    self.refresh_student_tree()
                    edit_dialog.accept()

                buttons.accepted.connect(accept)
                buttons.rejected.connect(edit_dialog.reject)
                edit_dialog.exec_()
            else:
                QtWidgets.QMessageBox.warning(self, 'Student Not Found', f"Student {student_id} does not exist.")
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
                    course_codes.append(row[1])  # Assuming course code is in the first column
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
                writer = csv.writer(csvfile)
                writer.writerow(course_fieldnames)

    def update_student_csvfile(self, filename):
        global student
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=student_fieldnames)
            writer.writeheader()
            for student_data in student.values():
                writer.writerow(student_data)

    def filter_course_tree(self, text):
        filtered_courses = {}
        for course_code, course_name in course.items():
            if text.lower() in course_code.lower() or text.lower() in course_name.lower():
                filtered_courses[course_code] = course_name

        # Update the course tree view with the filtered data
        self.update_course_tree(filtered_courses)

    def filter_student_tree(self, text):
        # Filter student data based on the entered text
        filtered_students = {student_id: student_data for student_id, student_data in student.items()
                             if text.lower() in student_id.lower() or
                             text.lower() in student_data['Name'].lower()}

        # Update the student tree view with the filtered data
        self.update_student_tree(filtered_students)

    def update_student_tree(self, students):
        # Clear the student tree view
        self.studentTree.clear()

        # Add filtered students to the tree view
        for student_data in students.values():
            self.add_student_to_tree(student_data)

    def update_course_tree(self, courses):
        # Clear the course tree view
        self.courseTree.clear()

        # Add filtered courses to the tree view
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

        if studentID in student:
            QtWidgets.QMessageBox.warning(self, "Duplicate Student ID", f"Student with ID {studentID} already exists.")
            return

        student_data = {'Student_ID': studentID, 'Name': name, 'Age': age,
                        'Gender': gender, 'Course': course, 'Year_Level': yearLevel}

        student[studentID] = student_data
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
                course_codes = [row[1] for row in reader]
                self.courseComboBox.addItems(course_codes)

    def get_gender(self):
        if self.maleRadBut.isChecked():
            return "Male"
        elif self.femaleRadBut.isChecked():
            return "Female"
        else:
            print("Error: No gender selected.")
            return ""


class AddCourseDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(AddCourseDialog, self).__init__(parent)
        uic.loadUi('addcourse_ui.ui', self)
        self.parent = parent
        self.course_csv = CourseCSV(course_filename)  # Create an instance of CourseCSV
        self.confirmButton = self.findChild(QtWidgets.QPushButton, 'addCourseConfirm')
        self.cancelButton = self.findChild(QtWidgets.QPushButton, 'cancelCourse')
        self.confirmButton.clicked.connect(self.confirm_course)
        self.cancelButton.clicked.connect(self.reject)

    def confirm_course(self):
        course_code = self.courseCodeField.text()
        course_name = self.courseNameField.text()
        if not self.course_csv.is_duplicate_course(course_code):  # Check if course code is not a duplicate
            self.course_csv.add_course(course_code, course_name)  # Add the course
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Course Duplicate', f"Course {course_code} already exists.")


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
