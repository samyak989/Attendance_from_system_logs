from flask import render_template, url_for, flash, redirect
from sqlalchemy import and_
from datetime import datetime
from AttendanceApp import app, db, bcrypt
from AttendanceApp.forms import RollNoForm, SearchForm, AdminForm, DownloadForm
from AttendanceApp.models import Attendance

hashed_admin_password = '$2b$12$gM2Do7SJHqWjWaNcgOnlNOCaPjJ7oi7RHnmNOITFqhPDyzkIqsCSK' 


@app.route("/login", methods= ['GET', 'POST'])
def login():
    form = RollNoForm()
    if form.validate_on_submit():
        if form.rollNo.data != None:
            return redirect(url_for('home', inputRollNo = form.rollNo.data))
        else:
            flash('Login unsuccessful. Check roll no.', 'danger')
    return render_template('login.html', title= 'Login', form= form)


@app.route("/admin_login", methods=['GET', 'POST'])
def admin_login():
    form = AdminForm()

    if form.validate_on_submit():
        if form.username.data == 'Ligma' and bcrypt.check_password_hash(hashed_admin_password, form.password.data):
            flash(f'Admin login for user: {form.username.data}', 'success')
            return redirect(url_for('home'))

    return render_template('adminLogin.html', title= 'Admin Login', form= form)


@app.route("/")
@app.route("/home")
@app.route("/home/<inputRollNo>")
def home(inputRollNo= 0):
    records = Attendance.query.filter_by(rollNo= inputRollNo).all()

    return render_template('home.html', records= records)


@app.route("/show_all", methods= ['GET', 'POST'])
def show_all():
    form = SearchForm()
    downloadForm = DownloadForm()
    
    records = []
    
    if form.validate_on_submit():
        
        records = Attendance.query.filter(Attendance.dateTime == datetime(year= form.date.data.year, month= form.date.data.month, day= form.date.data.day)).all()
        
        print('Records fetched of length: '+str(len(records)))
    print('sending new page')
    return render_template('showAll.html', title= 'All Records', records= records, form= form, downloadForm= downloadForm)


@app.route("/about")
def about():
    return render_template('about.html', title= 'About')