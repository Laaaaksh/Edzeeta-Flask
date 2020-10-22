from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
from chatbot import chatbot
import random
import uuid
from flask_mail import Mail, Message
import collections


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

end_content = "\nPrerequisites-\n\n- Laptop or PC with good internet connectivity\n- Working Webcam\n- Headphone with Mic\n- Notebook and Pencil/Pen\nEdZeeta's courses range from block-based languages for beginners to advanced programming languages. All courses are project-based and this will be their first step towards creating games, animations, and interesting applications using the concepts they learn. View more details: ____\nOur team will soon get in touch with you regarding further details. Incase of anny queries write back to us.\n\nRegards\nTeam EdZeeta"    


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


#DB class for storing time slots
class Time_slot(db.Model):
    __tablename__ = 'time_slot'
    slotId = db.Column(db.Integer, primary_key=True)
    slotDate = db.Column(db.String(100))
    slotTime = db.Column(db.String(100))
    def __repr__(self):
    	return "{},{},{}".format(self.slotId,self.slotDate, self.slotTime)
    def __init__(self, slotDate, slotTime):
        self.slotDate = slotDate
        self.slotTime = slotTime




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




#All the routes of the website


@app.route('/')
def home():
	return render_template('home.html')

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
    '''
    with app.app_context():
        msg = Message(subject="Callback Confirmation",
                                sender=app.config.get("MAIL_USERNAME"),
                        recipients=["saxenavedant61@gmail.com"], # replace with your email for testing
                        body="Hey !\n\nWe have noted your request, you will get a call from us at around "+ time+ ". Have a good day!\n\nRegards\nTeam Edzeeta")
        mail.send(msg)
    '''
    
    if formName == 'home':
       return redirect(url_for('home')) 
    if formName == 'register':
       return redirect(url_for('register')) 
    if formName == 'courses':
       return redirect(url_for('courses'))
    if formName == 'course1':
       return redirect(url_for('course1'))
    if formName == 'course2':
       return redirect(url_for('course2'))
    if formName == 'course3':
       return redirect(url_for('course3'))
    if formName == 'course4':
       return redirect(url_for('course4'))
    if formName == 'about':
       return redirect(url_for('about'))
    if formName == 'blogs':
       return redirect(url_for('blogs'))
    if formName == 'blog1':
       return redirect(url_for('blog1'))
       

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/courses')
def courses():
	return render_template('parent_course.html')

@app.route('/register' , methods=["GET"])
def register():
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

    #Collections.sort(.subList(1, .size()))

    print(date)
    print(time)
    '''

    '''
    return render_template('register.html', result = result, date = date, time = time, msg = "0")

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
    if result2:
        msg_to_send = "You have already registered for a Trial class!"
    else:
        msg_to_send = "Hey " + str(childName)+ "!  Your Free Trial Class is Booked."
        student_book_ = Student_book(childName = childName, parentName = parentName, phoneNo = phoneNo, emailId = emailId, age = age, courseName = courseName, courseId = courseId, slotTime = slotTime, slotDate = slotDate, laptop = laptop)
        db.session.add(student_book_)
        db.session.commit()
    
    if courseName == "Scratch Programmming":
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
                          recipients=[emailId], # replace with your email for testing
                            body= "Hey "+ childName +"! Welcome to EdZeeta's " + courseName + " course!\n\nThanks for choosing EdZeeta Learning. During the demo session your kid will be exposed to "+courseName + mailCont +"\n"+ end_content)
           mail.send(msg)
   
  
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
    return render_template('register.html', msg = msg_to_send, result = result, date = date, time = time)


@app.route('/blogs')
def blogs():
	return render_template('blog.html')

@app.route('/blog1')
def blog1():
	return render_template('parent_blog.html')

@app.route('/course1')
def course1():
    return render_template("course1.html")
@app.route('/course2')
def course2():
    return render_template("course2.html")
@app.route('/course3')
def course3():
    return render_template("courses.html")
@app.route('/course4')
def course4():
    return render_template("course4.html")


@app.route('/admin')
def admin():
    sql1 = text('select * from course') 
    sql2 = text('select * from book')
    sql3 = text('select * from callback')
    sql5 = text('select * from time_slot')
    res1 = db.engine.execute(sql1)
    res2 = db.engine.execute(sql2)
    res3 = db.engine.execute(sql3)
    res5 = db.engine.execute(sql5)
    res1 = list(res1)
    res2 = list(res2)
    res3 = list(res3)
    res4 = '0'
    res5 = list(res5)
    return render_template('admin.html', res1 = res1, res2 = res2, res3 = res3, res4 = res4, res5 = res5)





@app.route('/admin', methods=['POST'])
def admin_post():
    sql1 = text('select * from course') 
    sql2 = text('select * from book')
    sql3 = text('select * from callback')
    sql5 = text('select * from time_slot')
    sql4 = text('select * from book where book.courseName = :courseName')
    res1 = db.engine.execute(sql1)
    res2 = db.engine.execute(sql2)
    res3 = db.engine.execute(sql3)
    res5 = db.engine.execute(sql5)
    res4 = db.engine.execute(sql4, courseName = request.form.get('courseName'))
    res1 = list(res1)
    res2 = list(res2)
    res3 = list(res3)
    res4 = list(res4)
    res5 = list(res5)
    return render_template('admin.html', res1 = res1, res2 = res2, res3 = res3, res4 = res4, res5 = res5)


@app.route('/insert_slot', methods = ['POST'])
def insert_slot():
 
    if request.method == 'POST':
 
        slotDate = request.form['slotDate']
        slotTime = request.form['slotTime']
         
        my_data = Time_slot(slotDate, slotTime)
        db.session.add(my_data)
        db.session.commit()
 
        flash("Time slot inserted Successfully")
 
        return redirect(url_for('admin'))




@app.route('/update_slot', methods = ['GET', 'POST'])
def update_slot():
    
    if request.method == 'POST':
        my_data = Time_slot.query.get(request.form.get('slotId'))
 
        my_data.slotDate = request.form['slotDate']
        my_data.slotTime = request.form['slotTime']
 
        db.session.commit()
        flash("Time slot Updated Successfully")
 
        return redirect(url_for('admin'))



@app.route('/delete_slot/<slotId>/', methods = ['GET', 'POST'])
def delete_slot(slotId):
    my_data = Time_slot.query.get(slotId)
    db.session.delete(my_data)
    db.session.commit()
    flash("Time Slot Deleted Successfully")
 
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
 

@app.route("/getR")
def get_bot_response():
    userText = request.args.get('msg')
    return str(chatbot.get_response(userText)) 

@app.route("/chatbot")
def chat_bot():
    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)
    