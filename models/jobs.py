from config import db

class Jobs(db.Model):
    __tablename__='jobs'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    CTC_offered = db.Column(db.String(200), nullable=False)
    job_location = db.Column(db.String(200), nullable=False)
    job_desc = db.Column(db.String(200), nullable=False)
    job_experience = db.Column(db.String(200), nullable=False)
    job_status = db.Column(db.String(200), nullable=False)
    employer_id = db.Column(db.Integer, db.ForeignKey('employer.id'))
    candidatesApplied = db.relationship('CandidatesApplied', backref='jobs')