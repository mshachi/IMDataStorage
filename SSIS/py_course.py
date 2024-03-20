import csv
import os.path


course_fieldnames = {'Course_Code', 'Course_Name'}


class CourseCSV:

    def __init__(self, filename):
        self.courses = {}
        self.filename = filename

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

    def edit_course(self, old_course_code, new_course_code, new_course_name):
        courses = []
        with open(self.filename, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Course_Code'] == old_course_code:
                    row['Course_Code'] = new_course_code
                    row['Course_Name'] = new_course_name
                courses.append(row)

        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=course_fieldnames)
            writer.writeheader()
            writer.writerows(courses)

    def delete_course(self, course_code):
        courses = []
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if not row['Course_Code'] == course_code:
                    courses.append(row)
        with open(self.filename, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=course_fieldnames)
            writer.writeheader()
            writer.writerows(courses)

    def valid_course(self, course_code):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Course_Code'] == course_code:
                    return True
        return False

    def is_duplicate_course(self, course_code):
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['Course_Code'] == course_code:
                    return True
        return False

    def get_deleted_course(self):
        # Get list of deleted course codes
        deleted_courses = set()
        with open(self.filename, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                deleted_courses.add(row['Course_Code'])

        return deleted_courses
