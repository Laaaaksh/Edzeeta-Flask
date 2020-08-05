#Execute this python file to initialize db and also add courses to course table accordingly
from main import db
from main import Callback, Student_book, Course

#First go and delete site.db from the root folder to clear db (all tables)
#Initialize db 
db.create_all()

#Write details for courses
course1 = Course(courseId = "course01", courseName = "courseName01")
db.session.add(course1)
course2 = Course(courseId = "course02", courseName = "courseName02")
db.session.add(course2)
course3 = Course(courseId = "course03", courseName = "courseName03")
db.session.add(course3)
course4 = Course(courseId = "course04", courseName = "courseName04")
db.session.add(course4)

db.session.commit()