#Execute this python file to initialize db and also add courses to course table accordingly
from main import db
from main import Callback, Student_book, Course, Time_slot

#First go and delete site.db from the root folder to clear db (all tables)
#Initialize db 
db.create_all()

#Write details for courses
course1 = Course(courseId = "1", courseName = "Scratch Programmming")
db.session.add(course1)
course2 = Course(courseId = "2", courseName = "App Inventor")
db.session.add(course2)
course3 = Course(courseId = "3", courseName = "Web Development")
db.session.add(course3)
course4 = Course(courseId = "4", courseName = "Python Programming")
db.session.add(course4)

db.session.commit()


#Write details for slots
slot1 = Time_slot(slotId = "1", slotDate = "21stSept", slotTime = "12:30pm")
db.session.add(slot1)
slot2 = Time_slot(slotId = "2", slotDate = "21stSept", slotTime = "02:30pm")
db.session.add(slot2)
slot3 = Time_slot(slotId = "3", slotDate = "21stSept", slotTime = "04:30pm")
db.session.add(slot3)
slot4 = Time_slot(slotId = "4", slotDate = "21stSept", slotTime = "06:00pm")
db.session.add(slot4)
slot5 = Time_slot(slotId = "5", slotDate = "22stSept", slotTime = "01:30pm")
db.session.add(slot5)
slot6 = Time_slot(slotId = "6", slotDate = "22stSept", slotTime = "03:30pm")
db.session.add(slot6)
slot7 = Time_slot(slotId = "7", slotDate = "22stSept", slotTime = "04:30pm")
db.session.add(slot7)
slot8 = Time_slot(slotId = "8", slotDate = "22stSept", slotTime = "07:30pm")
db.session.add(slot8)

db.session.commit()

