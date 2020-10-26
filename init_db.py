#Execute this python file to initialize db and also add courses to course table accordingly
from main import db
from main import Callback, Student_book, Course, Time_slot, Student_book_all

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
slot1 = Time_slot(slotDate = "25,Oct", slotTime = "12:30pm", totalSlots = 11, availableSlots = 11)
db.session.add(slot1)
slot2 = Time_slot(slotDate = "25,Oct", slotTime = "02:30pm", totalSlots = 10, availableSlots = 10)
db.session.add(slot2)


slot3 = Time_slot(slotDate = "26,Oct", slotTime = "04:30pm", totalSlots = 15, availableSlots = 15)
db.session.add(slot3)
slot4 = Time_slot(slotDate = "26,Oct", slotTime = "06:00pm", totalSlots = 25, availableSlots = 25)
db.session.add(slot4)
slot5 = Time_slot(slotDate = "26,Oct", slotTime = "08:00pm", totalSlots = 35, availableSlots = 35)
db.session.add(slot5)

slot6 = Time_slot(slotDate = "27,Oct", slotTime = "01:30pm", totalSlots = 60, availableSlots = 60)
db.session.add(slot6)
slot7 = Time_slot(slotDate = "27,Oct", slotTime = "03:30pm", totalSlots = 20, availableSlots = 20)
db.session.add(slot7)
slot8 = Time_slot(slotDate = "27,Oct", slotTime = "04:30pm", totalSlots = 18, availableSlots = 18)
db.session.add(slot8)
slot9 = Time_slot(slotDate = "27,Oct", slotTime = "05:30pm", totalSlots = 15, availableSlots = 15)
db.session.add(slot9)

slot10 = Time_slot(slotDate = "28,Oct", slotTime = "09:30am", totalSlots = 18, availableSlots = 18)
db.session.add(slot10)
slot11 = Time_slot(slotDate = "28,Oct", slotTime = "11:15am", totalSlots = 18, availableSlots = 18)
db.session.add(slot11)
slot12 = Time_slot(slotDate = "28,Oct", slotTime = "04:30pm", totalSlots = 28, availableSlots = 28)
db.session.add(slot12)
slot13 = Time_slot(slotDate = "28,Oct", slotTime = "06:30pm", totalSlots = 23, availableSlots = 23)
db.session.add(slot13)


slot14 = Time_slot(slotDate = "29,Oct", slotTime = "12:30pm", totalSlots = 15, availableSlots = 15)
db.session.add(slot14)
slot15 = Time_slot(slotDate = "29,Oct", slotTime = "01:30pm", totalSlots = 15, availableSlots = 15)
db.session.add(slot15)
slot16 = Time_slot(slotDate = "29,Oct", slotTime = "02:30pm", totalSlots = 25, availableSlots = 25)
db.session.add(slot16)
slot17 = Time_slot(slotDate = "29,Oct", slotTime = "04:45pm", totalSlots = 12, availableSlots = 12)
db.session.add(slot17)
slot18 = Time_slot(slotDate = "29,Oct", slotTime = "07:30pm", totalSlots = 10, availableSlots = 10)
db.session.add(slot18)

db.session.commit()

