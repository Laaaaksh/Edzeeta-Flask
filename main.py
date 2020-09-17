from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from datetime import datetime
import random
import uuid
from flask_mail import Mail, Message

app = Flask(__name__) #App instance
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
    "MAIL_USERNAME": 'edzeeta.test@gmail.com',
    "MAIL_PASSWORD": '@edzeeta1'
    }

app.config.update(mail_settings)
mail = Mail(app)





#DB class for booking a class
class Student_book(db.Model):
    __tablename__ = 'book'
    childId = db.Column(db.String(100), primary_key=True)
    childName = db.Column(db.String(50), nullable = False)
    parentName = db.Column(db.String(50), nullable = True)
    phoneNo = db.Column(db.String(10), nullable = False)
    emailId = db.Column(db.String(50), nullable = False)
    age = db.Column(db.String(2), nullable = False)	
    courseName = db.Column(db.String(50), nullable = False)
    courseId = db.Column(db.String(10), db.ForeignKey('course.courseId'))
    def __repr__(self):
    	return "{},{},{},{},{},{},{},{}".format(self.childId, self.childName, self.parentName, self.phoneNo, self.emailId, self.age, self.courseName, self.courseId)


#DB class for storing time slots
class Time_slot(db.Model):
    __tablename__ = 'time_slot'
    slotId = db.Column(db.String(100), primary_key=True)
    slotDate = db.Column(db.String(100))
    slotTime = db.Column(db.String(100))
    def __repr__(self):
    	return "{},{},{}".format(self.slotId,self.slotDate, self.slotTime)




#DB class for callback feature
class Callback(db.Model):
    __tablename__ = 'callback'
    callbackId = db.Column(db.String(100), primary_key=True)
    name = db.Column(db.String(50), nullable = False)
    phoneNo = db.Column(db.String(10), nullable = False)
    time = db.Column(db.String(20), nullable = False)
    def __repr__(self):
    	return "{},{},{},{}".format(self.callbackId, self.name, self.phoneNo, self.time)



#DB for all courses
class Course(db.Model):
    __tablename__ = 'course'
    courseId = db.Column(db.String(10), primary_key=True)
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
    callbackId = str(uuid.uuid1())
    #name = request.form.get('name') #Remove from db
    phoneNo = request.form.get('phoneNo')
    date = request.form.get('date')
    time = request.form.get('time')
    print(callbackId, phoneNo, date, time)
    # callback_ = Callback(callbackId = callbackId, name = name, phoneNo = phoneNo, time = time)
    # db.session.add(callback_)
    # db.session.commit()
    # with app.app_context():
    #     msg = Message(subject="Callback Confirmation",
    #                     sender=app.config.get("MAIL_USERNAME"),
    #                     recipients=["saxenavedant61@gmail.com"], # replace with your email for testing
    #                     body="Hey "+name+"!\n\nWe have noted your request, you will get a call from us at around "+ time+ ". Have a good day!\n\nRegards\nTeam Edzeeta")
    #     mail.send(msg)

    return redirect(url_for('register'))

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
    return render_template('register.html', result = result)

@app.route('/register',methods=['POST'])
def register_post():
    childId = str(uuid.uuid1())
    parentName = request.form.get('parentName')
    emailId = request.form.get('emailId')
    phoneNo = request.form.get('phoneNo')
    childName = request.form.get('childName')
    age = request.form.get('age')
    courseName = request.form.get('courseName')
    slotDate = request.form.get('slotDate') #Add to db
    slotTime = request.form.get('slotTime') #Add to db
    laptop = request.form.get('laptop') #Add to db    
    print(childId, parentName, emailId, phoneNo, childName, age, courseName, slotDate, slotTime, laptop)
    
    '''
    sql_q=text('select courseId from Course where Course.courseName = :courseName')
    result = db.engine.execute(sql_q, courseName = courseName)
    result = list(result)
    courseId = result[0][0]
    student_book_ = Student_book(childId = childId, childName = childName, parentName = parentName, phoneNo = phoneNo, emailId = emailId, age = age, courseName = courseName, courseId = courseId)
    db.session.add(student_book_)
    db.session.commit()
    with app.app_context():
        msg = Message(subject="Booking confirmation",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=["yashmverma7@gmail.com"], # replace with your email for testing
                        body="Hey "+ childName +"\n\nYour course "+courseName+" has been booked! Have a good day!\n\nRegards\nTeam Edzeeta")
        mail.send(msg)
    '''
    return redirect(url_for('home'))


@app.route('/blogs')
def blogs():
	return render_template('blog.html')

@app.route('/blog1')
def blog1():
	return render_template('parent_blog.html')

@app.route('/course1')
def course1():
    return render_template("courses.html")
@app.route('/course2')
def course2():
    return render_template("courses.html")
@app.route('/course3')
def course3():
    return render_template("courses.html")
@app.route('/course4')
def course4():
    return render_template("courses.html")


@app.route('/admin')
def admin():
    sql1 = text('select * from course') 
    sql2 = text('select * from book')
    sql3 = text('select * from callback')
    res1 = db.engine.execute(sql1)
    res2 = db.engine.execute(sql2)
    res3 = db.engine.execute(sql3)
    res1 = list(res1)
    res2 = list(res2)
    res3 = list(res3)
    res4 = '0'
    return render_template('admin.html', res1 = res1, res2 = res2, res3 = res3, res4 = res4)





@app.route('/admin', methods=['POST'])
def admin_post():
    sql1 = text('select * from course') 
    sql2 = text('select * from book')
    sql3 = text('select * from callback')
    sql4 = text('select * from book where book.courseName = :courseName')
    res1 = db.engine.execute(sql1)
    res2 = db.engine.execute(sql2)
    res3 = db.engine.execute(sql3)
    res4 = db.engine.execute(sql4, courseName = request.form.get('courseName'))
    res1 = list(res1)
    res2 = list(res2)
    res3 = list(res3)
    res4 = list(res4)
    return render_template('admin.html', res1 = res1, res2 = res2, res3 = res3, res4 = res4)





if __name__ == '__main__':
    app.run(debug=True)
    