from config import db

class CandidatesApplied(db.Model):
    __tablename__='candidatesApplied'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    job_title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey("jobs.id"))