from config import db

class Candidate(db.Model):
    __tablename__='candidate'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(200), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False)
    jobsApplied = db.relationship('JobsApplied', backref='candidate')
    
