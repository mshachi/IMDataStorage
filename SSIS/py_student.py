import csv
from PyQt5 import QtWidgets, uic
import sys
import os.path
from PyQt5.QtWidgets import QDialog, QMessageBox
import py_course as cr

# fieldnames/column names for csv file
student_fieldnames = ['Student_ID', 'Name', 'Age', 'Gender', 'Course', 'Year_Level']
course_fieldnames = ['Course_Code', 'Course_Name']
filename = "student_csv.csv"
student = {}


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('mainwindow_ui.ui', self)
        self.show()
        self.load_csvfile(filename)

        self.addStudent = self.findChild(QtWidgets.QPushButton, 'addStudent')
        self.addStudent.clicked.connect(self.open_add_student_dialog)

        self.deleteStudent = self.findChild(QtWidgets.QPushButton, 'deleteStudent')
        self.deleteStudent.clicked.connect(self.open_delete_student_dialog)

        self.editStudent = self.findChild(QtWidgets.QPushButton, 'editStudent')
        self.editStudent.clicked.connect(self.open_edit_student_dialog)

        self.refreshButton = self.findChild(QtWidgets.QPushButton, 'reloadButton')
        self.refreshButton.clicked.connect(self.refresh_student_tree)
        self.studentTree = self.findChild(QtWidgets.QTreeWidget, 'studentTree')

    def open_add_student_dialog(self):
        self.add_student_dialog = AddStudentDialog(self)
        self.add_student_dialog.accepted.connect(self.refresh_student_tree)
        self.add_student_dialog.exec_()

    def open_delete_student_dialog(self):
        self.delete_student_dialog = DeleteStudentDialog(self)
        self.delete_student_dialog.accepted.connect(self.refresh_student_tree)
        self.delete_student_dialog.exec_()

    def open_edit_student_dialog(self):
        self.edit_student_dialog = EditDialog(self)
        self.edit_student_dialog.accepted.connect(self.refresh_student_tree)
        self.edit_student_dialog.exec_()

    def load_csvfile(self, filename):
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

    def update_csvfile(self, filename):
        global student
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=student_fieldnames)
            writer.writeheader()
            for student_data in student.values():
                writer.writerow(student_data)

    def add_student_to_tree(self, student_data):
        item = QtWidgets.QTreeWidgetItem(self.studentTree)
        item.setText(0, student_data['Student_ID'])
        item.setText(1, student_data['Name'])
        item.setText(2, student_data['Age'])
        item.setText(3, student_data['Gender'])
        item.setText(4, student_data['Course'])
        item.setText(5, student_data['Year_Level'])

    def refresh_student_tree(self):
        self.studentTree.clear()
        self.load_csvfile(filename)


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
        self.parent.update_csvfile(filename)
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


class DeleteStudentDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(DeleteStudentDialog, self).__init__(parent)
        uic.loadUi('deletestudent_ui.ui', self)
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
                self.parent.update_csvfile(filename)
                self.accept()

        else:
            QtWidgets.QMessageBox.warning(self, 'Student Not Found', f"Student {studentID} does not exist.")


class EditDialog(QtWidgets.QDialog):
    def __init__(self, parent):
        super(EditDialog, self).__init__(parent)
        uic.loadUi('editstudent_ui.ui', self)
        self.parent = parent
        self.load_course_codes()
        self.find = self.findChild(QtWidgets.QPushButton, 'findStudent')
        self.editConfirm = self.findChild(QtWidgets.QPushButton, 'editStudent_confirm')
        self.editCancel = self.findChild(QtWidgets.QPushButton, 'editStudent_cancel')
        self.findStudent.clicked.connect(self.find_student)
        self.editConfirm.clicked.connect(self.edit_student)
        self.editCancel.clicked.connect(self.reject)


    def find_student(self):
        studentID = self.studentIDField.text()
    def edit_student(self):
        global student


        if studentID in student:
            course = self.courseComboBox.currentText()
            yearLevel = str(self.yearSpinBox.value())

            # Update student information
            student[studentID]['Course'] = course
            student[studentID]['Year_Level'] = yearLevel

            # Update CSV file
            self.parent.update_csvfile(filename)

            # Close dialog
            self.accept()
        else:
            QtWidgets.QMessageBox.warning(self, 'Student Not Found', f"Student {studentID} does not exist.")

    def load_course_codes(self):
        course_filename = "course_csv.csv"
        if os.path.exists(course_filename):
            with open(course_filename, mode='r') as file:
                reader = csv.reader(file)
                next(reader)
                course_codes = [row[0] for row in reader]
                self.courseComboBox.addItems(course_codes)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    window = Ui()
    app.exec_()
