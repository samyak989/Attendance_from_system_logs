from AttendanceApp import db

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