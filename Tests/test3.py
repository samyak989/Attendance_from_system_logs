from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RollNoForm, SearchForm, DownloadForm
import sqlite3

app = Flask(__name__)

app.config['SECRET_KEY'] = '2989eccc09f4696c18b79bfe04bafbc6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class Student(db.Model):
    rollNo = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(30), nullable= False)
    attendance = db.relationship('Attendance', backref='attendee', lazy= True)

    # Print output
    def __repr__(self):
        return f'Student({self.name}, {self.rollNo})'

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key= True)
    dateTime = db.Column(db.DateTime, nullable= False)
    subjectCode = db.Column(db.String(6), nullable= False)
    subjectName = db.Column(db.String(20), nullable= False)
    attended = db.Column(db.Boolean)
    studentRollNo = db.Column(db.Integer, db.ForeignKey('student.rollNo'), nullable= False)

    # Print output
    def __repr__(self):
        return f'Attendance({self.dateTime}, {self.studentRollNo}, {self.subjectCode}, {self.attended})'

@app.route("/")
@app.route("/home")
@app.route("/home/<rollNo>")
def home(rollNo= ''):
    if rollNo == '':
        return redirect(url_for('login'))
    
    conn = sqlite3.connect('Attendance_database.db')
    c = conn.cursor()
    c.execute("SELECT * FROM ATTENDANCE WHERE Roll_no = '"+str(rollNo)+"'")

    records = c.fetchmany(500)

    for record in records:
        print(record)
    
    return render_template('home.html', records= records)

@app.route("/show_all", methods= ['GET', 'POST'])
def show_all():
    form = SearchForm()
    downloadForm = DownloadForm()
    conn = sqlite3.connect('Attendance_database.db')
    c = conn.cursor()
    records = []
    
    if form.validate_on_submit():
        print(f'Form submitted. Retrieving data for {form.date.data}.')
        
        c.execute(f"SELECT * FROM ATTENDANCE WHERE day = {form.date.data.day} AND month = {form.date.data.month} AND year = {form.date.data.year} AND (hour >= {form.fromTime.data.hour} AND minute >= {form.fromTime.data.minute}) AND (hour <= {form.toTime.data.hour} AND minute <= {form.toTime.data.minute});")
        
        records = c.fetchall()
        print('Fetch_all result')
        for record in records:
            print(record)
        print('Records fetched of length: '+str(len(records)))
    print('sending new page')
    return render_template('showAll.html', title= 'All Records', records= records, form= form, downloadForm= downloadForm)


@app.route("/about")
def about():
    return render_template('about.html', title= 'About')


@app.route("/login", methods= ['GET', 'POST'])
def login():
    form = RollNoForm()
    if form.validate_on_submit():
        if form.rollNo.data != None:
            return redirect(url_for('home', rollNo = form.rollNo.data))
        else:
            flash('Login unsuccessful. Check roll no.', 'danger')
    return render_template('login.html', title= 'Login', form= form)


if __name__=="__main__":
    app.run(host= '0.0.0.0', debug=True)