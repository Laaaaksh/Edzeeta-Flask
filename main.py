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


@app.route('/',methods=['POST'])
def callback_post():
    callbackId = str(uuid.uuid1())
    name = request.form.get('name')
    phoneNo = request.form.get('phoneNo')
    time = request.form.get('time')
    print(name, phoneNo, time)
    callback_ = Callback(callbackId = callbackId, name = name, phoneNo = phoneNo, time = time)
    db.session.add(callback_)
    db.session.commit()
    with app.app_context():
        msg = Message(subject="Callback Confirmation",
                        sender=app.config.get("MAIL_USERNAME"),
                        recipients=["saxenavedant61@gmail.com"], # replace with your email for testing
                        body="Hey "+name+"!\n\nWe have noted your request, you will get a call from us at around "+ time+ ". Have a good day!\n\nRegards\nTeam Edzeeta")
        mail.send(msg)

    return redirect(url_for('home'))

@app.route('/about')
def about():
	return render_template('about.html')

@app.route('/courses')
def courses():
	return render_template('courses.html')

@app.route('/bookNow')
def book():
	return render_template('book.html')

@app.route('/bookNow',methods=['POST'])
def book_post():
    childId = str(uuid.uuid1())
    childName = request.form.get('childName')
    parentName = request.form.get('parentName')
    phoneNo = request.form.get('phoneNo')
    emailId = request.form.get('emailId')
    age = request.form.get('age')
    courseName = request.form.get('courseName')
    print(courseName)
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
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
    