from config import db

class Employer(db.Model):
    __tablename__='employer'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    jobs = db.relationship('Jobs', backref='employer')