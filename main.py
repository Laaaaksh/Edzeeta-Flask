from flask import Flask, render_template, url_for, flash, redirect, request, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from chatbot import chatbot
import random
import uuid
from flask_mail import Mail, Message
import collections
import flask_excel as excel

#from twilio.rest import Client

admin_id = "/"+ str(uuid.uuid1()) 


app = Flask(__name__) #App instance
app.static_folder = 'static'
app.config['SECRET_KEY'] = 'e36106119a10a327dd4fd993dfad8262'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'   #DB path
db = SQLAlchemy(app)  #Create a database instance

'''
Follow these instructions to enable some settings for sending automated mails
https://stackoverflow.com/questions/16512592/login-credentials-not-working-with-gmail-smtp
'''
#Required for sending automated mails
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": 'Edzeetawebsite@gmail.com',
    "MAIL_PASSWORD": 'reset@123'
    }

app.config.update(mail_settings)
mail = Mail(app)



#Email content
scratch = "We follow a personalized approach to learning and plan the course pace by assessing the level of a kid during the demo session.\n\nScratch is a block-based programming language developed by MIT. It helps to develop computational thinking in kids. We teach with the help of an interactive curriculum which is completely flexible and adjustable depending upon the student’s pace. We emphasize on experientialexperimental learning and encourage kids to develop their own projects. Check out _____!"
app_d = "We follow a personalized approach to learning and plan the course pace by assessing the level of a kid during the demo session.\n\nThrough the App Inventor course, we teach kids block based app development, which helps them increase their creativity, computational thinking and obviously build real world apps completely on their own. We publish the best apps built by our students on the google playstore! Check out _____!"
python_ = "We follow a personalized approach to learning and plan the course pace by assessing the level of a kid during the demo session.\n\nThis course introduces your child to one of the widely used scripting languages in the world of development, research and corporate business. The kid understands how he/she can use his/her new skills for the betterment of the world and their personal development. Check out _____!"
web = "We follow a personalized approach to learning and plan the course pace by assessing the level of a kid during the demo session.\n\nYour child will be introduced to building beautiful, interactive websites out of nothing. They learn most of the front end related development for a website with the three skills HTML, CSS, and Javascript. We also teach how to host your websites. Your child’s website can be live in the real web world! Check out _____!" 

end_content = "\nPrerequisites-\n- Laptop or PC with good internet connectivity\n- Working Webcam\n- Headphone with Mic\n- Notebook and Pencil/Pen\n\nEdZeeta's courses range from block-based languages for beginners to advanced programming languages. All courses are project-based and this will be their first step towards creating games, animations, and interesting applications using the concepts they learn. View more details: ____\n\nOur team will soon get in touch with you regarding further details. Incase of anny queries write back to us.\n\nRegards\nTeam EdZeeta"    


#DB class for booking a class
class Student_book(db.Model):
    __tablename__ = 'book'
    childId = db.Column(db.Integer, primary_key=True)
    childName = db.Column(db.String(50), nullable = False)
    parentName = db.Column(db.String(50), nullable = True)
    phoneNo = db.Column(db.String(10), nullable = False)
    emailId = db.Column(db.String(50), nullable = False)
    age = db.Column(db.String(2), nullable = False)	
    courseName = db.Column(db.String(50), nullable = False)
    courseId = db.Column(db.String(10), db.ForeignKey('course.courseId'))
    slotDate = db.Column(db.String(10), nullable = False)
    slotTime = db.Column(db.String(10), nullable = False)
    laptop = db.Column(db.String(1), nullable = False)
    def __repr__(self):
    	return "{},{},{},{},{},{},{},{},{},{},{}".format(self.childId, self.childName, self.parentName, self.phoneNo, self.emailId, self.age, self.courseName, self.courseId, self.slotDate, self.slotTime, self.laptop)


#DB class for all bookings till date
class Student_book_all(db.Model):
    __tablename__ = 'book_all'
    childId = db.Column(db.Integer, primary_key=True)
    childName = db.Column(db.String(50), nullable = False)
    parentName = db.Column(db.String(50), nullable = True)
    phoneNo = db.Column(db.String(10), nullable = False)
    emailId = db.Column(db.String(50), nullable = False)
    age = db.Column(db.String(2), nullable = False)	
    courseName = db.Column(db.String(50), nullable = False)
    courseId = db.Column(db.String(10), db.ForeignKey('course.courseId'))
    slotDate = db.Column(db.String(10), nullable = False)
    slotTime = db.Column(db.String(10), nullable = False)
    laptop = db.Column(db.String(1), nullable = False)
    def __repr__(self):
    	return "{},{},{},{},{},{},{},{},{},{},{}".format(self.childId, self.childName, self.parentName, self.phoneNo, self.emailId, self.age, self.courseName, self.courseId, self.slotDate, self.slotTime, self.laptop)





#DB class for storing time slots
class Time_slot(db.Model):
    __tablename__ = 'time_slot'
    slotId = db.Column(db.Integer, primary_key=True)
    slotDate = db.Column(db.String(100))
    slotTime = db.Column(db.String(100))
    totalSlots = db.Column(db.Integer)
    availableSlots = db.Column(db.Integer)
    def __repr__(self):
    	return "{},{},{},{},{}".format(self.slotId,self.slotDate, self.slotTime, self.totalSlots, self.availableSlots)
    def __init__(self, slotDate, slotTime, totalSlots, availableSlots):
        self.slotDate = slotDate
        self.slotTime = slotTime
        self.totalSlots = totalSlots
        self.availableSlots = availableSlots




#DB class for callback feature
class Callback(db.Model):
    __tablename__ = 'callback'
    callbackId = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable = False)
    phoneNo = db.Column(db.String(10), nullable = False)
    time = db.Column(db.String(20), nullable = False)
    def __repr__(self):
    	return "{},{},{},{}".format(self.callbackId, self.phoneNo, self.date, self.time)



#DB for all courses
class Course(db.Model):
    __tablename__ = 'course'
    courseId = db.Column(db.Integer, primary_key=True)
    courseName = db.Column(db.String(50), nullable = False)
    courseEnrolled = db.relationship('Student_book', backref = 'constituency', lazy = True)
    def __repr__(self):
    	return "{},{}".format(self.courseId, self.courseName)
    def __init__(self, courseName):
        self.courseName = courseName


def unique(list1): 
  
    # intilize a null list 
    unique_list = [] 
    # traverse for all elements 
    for x in list1: 
        # check if exists in unique_list or not 
        if x not in unique_list: 
            unique_list.append(x) 
    return unique_list






#All the routes of the website
@app.route('/')
def home():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template('home.html', msg2 = msg2)

@app.route('/callback',methods=['POST'])
def callback_post():
    #name = request.form.get('name') #Remove from db
    formName = request.form.get('formName')
    phoneNo = request.form.get('phoneNo')
    date = request.form.get('date')
    time = request.form.get('time')
    print(phoneNo, date, time)
    callback_ = Callback(phoneNo = phoneNo, time = time, date = date)
    db.session.add(callback_)
    db.session.commit()

    
    if formName == 'home':
        session['msg2'] = "Success"
        return redirect(url_for('home'))

    if formName == 'register':
        session['msg2'] = "Success"
        return redirect(url_for('register')) 
    
    if formName == 'courses':
        session['msg2'] = "Success"
        return redirect(url_for('courses'))
    if formName == 'course1':
        session['msg2'] = "Success"
        return redirect(url_for('course1'))
    if formName == 'course2':
        session['msg2'] = "Success"
        return redirect(url_for('course2'))
    if formName == 'course3':
        session['msg2'] = "Success"
        return redirect(url_for('course3'))
    if formName == 'course4':
        session['msg2'] = "Success"
        return redirect(url_for('course4'))
    if formName == 'about':
        session['msg2'] = "Success"
        return redirect(url_for('about'))
    if formName == 'blogs':
        session['msg2'] = "Success"
        return redirect(url_for('blogs'))
    if formName == 'blog1':
        session['msg2'] = "Success"
        return redirect(url_for('blog1'))
    if formName == 'error':
        session['msg2'] = "Success"
        return redirect(url_for('error'))   

@app.route('/about')
def about():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template('about.html', msg2 = msg2)

@app.route('/courses')
def courses():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template('parent_course.html', msg2 = msg2)

@app.route('/register' , methods=["GET"])
def register():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)

    msg = session.get('msg')
    print(msg)
    if not msg:
        msg = "0"
    else:
        session.pop('msg', None)
    
    msg3 = session.get('msg3')
    print(msg3)
    if not msg3:
        msg3 = "0"
    else:
        session.pop('msg3', None)

    sql_q=text('select slotTime,slotDate from Time_slot')
    result = db.engine.execute(sql_q)
    result = list(result)
    date = []
    for row in result:
        date.append(row[1])

    date = unique(date)
    2#Collections.sort(date.subList(1, date.size()))

    time = []
    for i in range(len(date)):
        time.append([])
    
    for row in result:
        date1 = row[1]
        ind = date.index(date1)
        time[ind].append(row[0])

    #Collections.sort(.subList(1, .size()))

    print(date)
    print(time)
    
    '''

    '''
    return render_template('register.html', result = result, date = date, time = time, msg = msg, msg3= msg3, msg2 = msg2)

@app.route('/register',methods=['POST'])
def register_post():
    parentName = request.form.get('parentName')
    emailId = request.form.get('emailId')
    phoneNo = request.form.get('phoneNo')
    childName = request.form.get('childName')
    age = request.form.get('age')
    courseName = request.form.get('courseName')
    slotDate = request.form.get('slotDate') 
    slotTime = request.form.get('slotTime') 
    laptop = request.form.get('laptop')     
    sql_q=text('select slotTime,slotDate from Time_slot')
    result = db.engine.execute(sql_q)
    result = list(result)
    date = []
    for row in result:
        date.append(row[1])

    date = list(set(date))
    #Collections.sort(date.subList(1, date.size()))

    time = []
    for i in range(len(date)):
        time.append([])
    
    for row in result:
        date1 = row[1]
        ind = date.index(date1)
        time[ind].append(row[0])
    print(parentName, emailId, phoneNo, childName, age, courseName, slotDate, slotTime, laptop)
    sql_q=text('select courseId from Course where Course.courseName = :courseName')
    result = db.engine.execute(sql_q, courseName = courseName)
    result = list(result)
    courseId = result[0][0]
    if laptop is None:
        laptop = 0
    sql_q2 = text('select * from book where book.emailId = :emailId or book.phoneNo =:phoneNo')
    result2 = db.engine.execute(sql_q2, emailId = emailId, phoneNo = phoneNo)
    result2 = list(result2)
    sql_q3 = text('select slotId,availableSlots from Time_slot where Time_slot.slotTime = :slotTime')
    result3 = db.engine.execute(sql_q3, slotTime = slotTime)
    result3 = list(result3)
    if not result3:
        msg_to_send2 = "Slot already full! Choose another slot"
        return render_template('register.html', msg = "0",msg3 = msg_to_send2 , result = result, date = date, time = time)
    msg_to_send2 = "0"
    print(result3, slotTime)
    availableSlots = result3[0][1]
    slotId = result3[0][0]
    if result2:
        msg_to_send = "You have already registered for a Trial class!"
        session['msg'] = msg_to_send
        session['msg3'] = msg_to_send2
        return redirect(url_for('register'))
    else:
        msg_to_send = "Hey " + str(childName)+ "!  Your Free Trial Class is Booked."
        student_book_ = Student_book(childName = childName, parentName = parentName, phoneNo = phoneNo, emailId = emailId, age = age, courseName = courseName, courseId = courseId, slotTime = slotTime, slotDate = slotDate, laptop = laptop)
        student_book_a = Student_book_all(childName = childName, parentName = parentName, phoneNo = phoneNo, emailId = emailId, age = age, courseName = courseName, courseId = courseId, slotTime = slotTime, slotDate = slotDate, laptop = laptop)
        db.session.add(student_book_a)        
        db.session.add(student_book_)
        db.session.commit()



    if availableSlots >= 1:
        availableSlots -= 1
        my_data1 = Time_slot.query.filter_by(slotTime = slotTime).first()
        my_data1.availableSlots = availableSlots
        db.session.commit()
  
    if availableSlots == 0:
        my_data = Time_slot.query.filter_by(slotTime = slotTime).first()
        db.session.delete(my_data)
        db.session.commit()


    
    if courseName == "Scratch Programming":
        mailCont = scratch
    if courseName == "App Inventor":
        mailCont = app_d
    if courseName == "Web Development":
        mailCont = web
    if courseName == "Python Programming":
        mailCont = python_
            
    
    #Email functionality
    if not result2:
        with app.app_context():
           msg = Message(subject="Booking confirmation",
                          sender=app.config.get("MAIL_USERNAME"),
                          recipients=[emailId, "edzeetawebsite@gmail.com"], # replace with your email for testing
                            body= "Hey "+ childName +"! Welcome to EdZeeta's " + courseName + " course!\n\nThanks for choosing EdZeeta Learning. During the demo session your kid will be exposed to "+courseName + ". "+ mailCont +"\n"+ end_content)
           mail.send(msg)
   
    session['msg'] = msg_to_send
    session['msg3'] = msg_to_send2
    return redirect(url_for('register'))


@app.route('/blogs')
def blogs():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template('blog.html', msg2 = msg2)

@app.route('/blog1')
def blog1():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template('parent_blog.html', msg2 = msg2)

@app.route('/course1')
def course1():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template("course1.html", msg2 = msg2)
@app.route('/course2')
def course2():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template("course2.html", msg2 = msg2)

@app.route('/error')
def error():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template("error.html", msg2 = msg2)

@app.route('/course4')
def course4():
    msg2 = session.get('msg2')
    if not msg2:
        msg2 = "0"
    else:
        session.pop('msg2', None)
    return render_template("course4.html", msg2 = msg2)

@app.route('/adminLogin', methods = ["GET", "POST"])
def adminLogin():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        password = request.form['password']
        correct_pass = ["admin@edzeeta99"]
        if password == "admin@edzeeta99" or not password:
            return redirect(url_for('admin'))
        else:
            return render_template("login.html")

@app.route(admin_id)
def admin():
    sql1 = text('select * from course') 
    sql2 = text('select * from book')
    sql3 = text('select * from callback')
    sql5 = text('select * from time_slot')
    sql6 = text('select * from book_all')
    res1 = db.engine.execute(sql1)
    res2 = db.engine.execute(sql2)
    res3 = db.engine.execute(sql3)
    res5 = db.engine.execute(sql5)
    res6 = db.engine.execute(sql6)
    res1 = list(res1)
    res2 = list(res2)
    res3 = list(res3)
    res4 = '0'
    res5 = list(res5)
    res6 = list(res6)
    return render_template('admin.html', res1 = res1, res2 = res2, res3 = res3, res4 = res4, res5 = res5, res6 = res6)





@app.route(admin_id, methods=['POST'])
def admin_post():
    sql1 = text('select * from course') 
    sql2 = text('select * from book')
    sql3 = text('select * from callback')
    sql5 = text('select * from time_slot')
    sql4 = text('select * from book where book.courseName = :courseName')
    sql6 = text('select * from book_all')
    res1 = db.engine.execute(sql1)
    res2 = db.engine.execute(sql2)
    res3 = db.engine.execute(sql3)
    res5 = db.engine.execute(sql5)
    res4 = db.engine.execute(sql4, courseName = request.form.get('courseName'))
    res6 = db.engine.execute(sql6)
    res1 = list(res1)
    res2 = list(res2)
    res3 = list(res3)
    res4 = list(res4)
    res5 = list(res5)
    res6 = list(res6)
    return render_template('admin.html', res1 = res1, res2 = res2, res3 = res3, res4 = res4, res5 = res5, res6 = res6)


@app.route('/insert_slot', methods = ['POST'])
def insert_slot():
 
    if request.method == 'POST':
 
        slotDate = request.form['slotDate']
        slotTime = request.form['slotTime']
        totalSlots = request.form['totalSlots']
        availableSlots = totalSlots
         
        my_data = Time_slot(slotDate, slotTime, totalSlots, availableSlots)
        db.session.add(my_data)
        db.session.commit()
 
        return redirect(url_for('admin'))




@app.route('/update_slot', methods = ['GET', 'POST'])
def update_slot():
    
    if request.method == 'POST':
        my_data = Time_slot.query.get(request.form.get('slotId'))
 
        my_data.slotDate = request.form['slotDate']
        my_data.slotTime = request.form['slotTime']
        #print(type(my_data.availableSlots ), type(request.form['totalSlots']), type(my_data.totalSlots))
        my_data.availableSlots = my_data.availableSlots + int(request.form['totalSlots']) - my_data.totalSlots
        my_data.totalSlots = int(request.form['totalSlots'])

        db.session.commit()
  
 
        return redirect(url_for('admin'))



@app.route('/delete_slot/<slotId>/', methods = ['GET', 'POST'])
def delete_slot(slotId):
    my_data = Time_slot.query.get(slotId)
    db.session.delete(my_data)
    db.session.commit()
    flash("Time Slot Deleted Successfully")
 
    return redirect(url_for('admin'))
 
 



@app.route('/insert_course', methods = ['POST'])
def insert_course():
 
    if request.method == 'POST': 
        courseName = request.form['courseName']

        my_data = Course(courseName)
        print(my_data)
        db.session.add(my_data)
        db.session.commit()
        print("Course added successfully")
        return redirect(url_for('admin'))




@app.route('/update_course', methods = ['GET', 'POST'])
def update_course():
    
    if request.method == 'POST':
        my_data = Course.query.get(request.form.get('courseId'))
 
        my_data.courseName = request.form['courseName']
     
        db.session.commit()
        print("Course updated successfully")
        return redirect(url_for('admin'))




 
@app.route('/delete_course/<courseId>/', methods = ['GET', 'POST'])
def delete_course(courseId):
    my_data = Course.query.get(courseId)
    db.session.delete(my_data)
    db.session.commit()
    flash("Course Deleted Successfully")
 
    return redirect(url_for('admin'))
 
 
@app.route('/delete_student/<childId>/', methods = ['GET', 'POST'])
def delete_student(childId):
    my_data = Student_book.query.get(childId)
    db.session.delete(my_data)
    db.session.commit()
    flash("Student Deleted Successfully")
 
    return redirect(url_for('admin'))
 
@app.route('/delete_callback/<callbackId>/', methods = ['GET', 'POST'])
def delete_callback(callbackId):
    my_data = Callback.query.get(callbackId)
    db.session.delete(my_data)
    db.session.commit()
    flash("Callback Request Deleted Successfully")
 
    return redirect(url_for('admin'))
 


@app.route('/delete_callback_all', methods = ['GET', 'POST'])
def delete_callback_all():
    db.session.query(Callback).delete()
    db.session.commit()
    print("All callback deleted!")

    return redirect(url_for('admin'))



@app.route('/delete_slot_all', methods = ['GET', 'POST'])
def delete_slot_all():
    db.session.query(Time_slot).delete()
    db.session.commit()
    print("All Time Slots deleted!")

    return redirect(url_for('admin'))



@app.route('/delete_student_all', methods = ['GET', 'POST'])
def delete_student_all():
    db.session.query(Student_book).delete()
    db.session.commit()
    print("All Student Registrations deleted!")
    return redirect(url_for('admin'))


@app.route('/delete_course_all', methods = ['GET', 'POST'])
def delete_course_all():
    db.session.query(Course).delete()
    db.session.commit()
    print("All course deleted!")
    return redirect(url_for('admin'))


@app.route('/delete_all_records_all', methods = ['GET', 'POST'])
def delete_all_record_all():
    db.session.query(Student_book_all).delete()
    db.session.commit()
    print("All records deleted!")
    return redirect(url_for('admin'))



@app.route("/download", methods=['GET'])
def download_file():
    sql = text('select * from book_all')
    res = db.engine.execute(sql)
    res = list(res)
    result = []
    result.append(['childId', 'childName', 'parentName', 'phoneNo', 'emailId', 'age', 'courseName', 'courseId', 'slotDate', 'slotTime', 'laptop'])
    for row in res:
        temp = []
        for r in row:
            temp.append(r)
        result.append(temp)
    print(result)
    return excel.make_response_from_array(result, "csv", file_name="export_data")



#Chatbot

@app.route("/getR")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText)) 

@app.route("/chatbot")
def chat_bot():
    return render_template("index.html")


if __name__ == '__main__':
    excel.init_excel(app)
    app.run(debug=True)
    