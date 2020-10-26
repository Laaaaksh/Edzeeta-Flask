#Execute this python file to initialize db and also add courses to course table accordingly
from main import db
from main import Callback, Student_book, Course, Time_slot

#First go and delete site.db from the root folder to clear db (all tables)
#Initialize db 
db.create_all()

#Write details for courses
course1 = Course(courseName = "Scratch Programming")
db.session.add(course1)
course2 = Course(courseName = "App Inventor")
db.session.add(course2)
course3 = Course(courseName = "Web Development")
db.session.add(course3)
course4 = Course(courseName = "Python Programming")
db.session.add(course4)

db.session.commit()


#Write details for slots
slot1 = Time_slot(slotDate = "25,Oct", slotTime = "12:30pm", totalSlots = 11, availableSlots = 5)
db.session.add(slot1)
slot2 = Time_slot(slotDate = "25,Oct", slotTime = "02:30pm", totalSlots = 10, availableSlots = 10)
db.session.add(slot2)
slot3 = Time_slot(slotDate = "26,Oct", slotTime = "04:30pm", totalSlots = 5, availableSlots = 5)
db.session.add(slot3)
slot4 = Time_slot(slotDate = "26,Oct", slotTime = "06:00pm", totalSlots = 5, availableSlots = 5)
db.session.add(slot4)
slot5 = Time_slot(slotDate = "27,Oct", slotTime = "01:30pm", totalSlots = 6, availableSlots = 6)
db.session.add(slot5)
slot6 = Time_slot(slotDate = "27,Oct", slotTime = "03:30pm", totalSlots = 7, availableSlots = 7)
db.session.add(slot6)
slot7 = Time_slot(slotDate = "28,Oct", slotTime = "04:30pm", totalSlots = 8, availableSlots = 8)
db.session.add(slot7)
slot8 = Time_slot(slotDate = "29,Oct", slotTime = "07:30pm", totalSlots = 5, availableSlots = 5)
db.session.add(slot8)

db.session.commit()

