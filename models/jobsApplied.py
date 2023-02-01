from config import db

class JobsApplied(db.Model):
    __tablename__ = 'jobsApplied'
    id = db.Column(db.Integer, primary_key=True)
    job_title = db.Column(db.String(200), nullable=False)
    company_name = db.Column(db.String(200), nullable=False)
    candidate_id = db.Column(db.Integer, db.ForeignKey('candidate.id'))
    
