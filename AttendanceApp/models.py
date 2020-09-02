from AttendanceApp import db

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    id = db.Column(db.Integer, primary_key= True)
    dateTime = db.Column(db.DateTime, nullable= False)
    name = db.Column(db.String(30), nullable= False)
    rollNo = db.Column(db.Integer, nullable= False)
    className = db.Column(db.String(6), nullable= False)
    duration = db.Column(db.Integer, nullable= False)
    attended = db.Column(db.Boolean, nullable= False)

    ipAddress = db.Column(db.String(12), nullable= False)

    # Print output
    def __repr__(self):
        return f'Attendance({self.dateTime}, {self.rollNo}, {self.className}, {self.attended})'