from flask import render_template, url_for, flash, redirect
from AttendanceApp import app, db, bcrypt
from AttendanceApp.forms import RollNoForm, AdminForm
from AttendanceApp.models import Attendance

hashed_admin_password = '$2b$12$gM2Do7SJHqWjWaNcgOnlNOCaPjJ7oi7RHnmNOITFqhPDyzkIqsCSK' 

@app.route("/")
@app.route("/home")
def home():
    records = []
    
    return render_template('home.html', records= records)


@app.route("/about")
def about():
    return render_template('about.html', title= 'About')


@app.route("/login", methods= ['GET', 'POST'])
def login():
    form = RollNoForm()
    if form.validate_on_submit():
        if form.rollNo.data == '1803310068':
            flash(f'Login successful for user: {form.rollNo.data}', 'success')
            return redirect(url_for('home'))
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