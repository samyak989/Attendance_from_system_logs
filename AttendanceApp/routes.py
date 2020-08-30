from flask import render_template, url_for, flash, redirect
from AttendanceApp import app
from AttendanceApp.forms import RollNoForm
from AttendanceApp.models import Student, Attendance

posts = [
    {
        'author' : 'Bhgt',
        'title' : 'Post 3',
        'content' : 'I dunno why I posted this.',
        'date' : 'August 29, 2020'
    },
    {
        'author' : 'Smyk',
        'title' : 'Post 4',
        'content' : 'This website sucks.',
        'date' : 'August 29, 2020'
    },
    {
        'author' : 'Meseeks',
        'title' : 'Oweee!',
        'content' : 'EXISTENCE IS PAIN!!',
        'date' : 'August 1, 2020'
    }
]

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts= posts)


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