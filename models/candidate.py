from config import db

class Candidate(db.Model):
    __tablename__='candidate'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    jobsApplied = db.relationship('JobsApplied', backref='candidate')
    personalDetails = db.relationship('PersonalDetails', backref='candidate')
    projects = db.relationship('Projects', backref='candidate')
    experiences = db.relationship('Experiences', backref='candidate')
    education = db.relationship('Education', backref='candidate')
    certificates = db.relationship('Certificates', backref='candidate')
    skills = db.relationship('Skills', backref='candidate')
