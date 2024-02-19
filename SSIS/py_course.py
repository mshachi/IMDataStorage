import csv
import os.path


course_fieldnames = {'Course_Code', 'Course_Name'}


class CourseCSV:

    def __init__(self, filename):
        self.courses = {}
        self.filename = filename
        self.valid = False

    def add_course(self, course_code, course_name):
        self.courses = {'Course_Code': course_code, 'Course_Name': course_name}
        if os.path.exists(self.filename):
            with open(self.filename, mode='a', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=course_fieldnames)
                writer.writerow(self.courses)
        else:
            with open(self.filename, 'w', newline='') as csvfile:
                writer = csv.writer(csvfile, fieldnames=course_fieldnames)
                writer.writerow(self.courses)

    def delete_course(self, course_code):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row[0] == course_code:
                    del row
                    break

    def valid_course(self, course_code):
        with open(self.filename, mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == course_code:
                    self.valid = True
