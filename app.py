from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
from config import db, SECRET_KEY,AWS_ACCESS_KEY_ID,SECRET_ACCESS_KEY
from dotenv import load_dotenv
import boto3
from models.candidate import Candidate
from models.jobs import Jobs
from models.jobsApplied import JobsApplied
from models.employer import Employer
from models.candidatesApplied import CandidatesApplied

s3_client = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID,
                        aws_secret_access_key=SECRET_ACCESS_KEY, region_name = 'us-west-2')


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = environ.get("DB_URI")
    app.config["SQLALCHEMY_TRACK_NOTIFICATIONS"] = False
    app.config["SQLALCHEMY_ECHO"] = False
    app.secret_key = SECRET_KEY
    db.init_app(app)
    print("DB Initialized Successfully")

    CORS(app)


    with app.app_context():
        @app.route('/candidate_sign_up', methods=['POST'])
        def candidate_sign_up():
            data = request.form.to_dict(flat=True)
            candidate = Candidate.query.filter_by(email=data["email"]).first()

            if candidate is None:
                new_user = Candidate(
                    email = data["email"],
                    password = data["password"],
                    username = data["username"]
                )
                db.session.add(new_user)
                db.session.commit()
            else:
                return "user already exist"

            return "user added successfully!"

        @app.route('/candidate_sign_in', methods=['POST'])
        def candidate_sign_in():
            data = request.form.to_dict(flat=True)

            candidate = Candidate.query.filter_by(email=data["email"]).first()

            if candidate is None:
                return "user not exist"
            else:
                candidate_id = candidate.id
                return str(candidate_id)


        
        @app.route('/employer_sign_up', methods=['POST'])
        def employer_sign_up():
            data = request.form.to_dict(flat=True)
            employer = Employer.query.filter_by(email=data["email"]).first()

            if employer is None:
                new_user = Employer(
                    company_name = data["company_name"],
                    email = data["email"]
                )
                db.session.add(new_user)
                db.session.commit()
            else:
                return "company already registered"

            return "user added successfully!"

        @app.route('/employer_sign_in', methods=['POST'])
        def employer_sign_in():
            data = request.form.to_dict(flat=True)

            # formEmail = data["email"]

            employer = Employer.query.filter_by(email=data["email"]).first()

            if employer is None:
                return "user not exist!"
            else:
                employer_id = Employer.id
                return str(employer_id)


        @app.route('/post_job', methods=['POST'])
        def post_job():
            company_name = request.args.get('company_name')
            employer = Employer.query.filter_by(company_name=company_name).first()

            job_details= request.get_json()

            if employer is None:
                return "Company not registered"
            else:
                new_job_details = Jobs(
                    company_name = job_details["company_name"],
                    CTC_offered =job_details ["CTC_offered"],
                    job_location = job_details["job_location"],
                    job_desc = job_details["job_desc"],
                    job_experience = job_details["job_experience"],
                    job_status = job_details["job_status"],
                    employer_id = employer.id
                )
                db.session.add(new_job_details)
                db.session.commit()
                return "job posted sucessfully!"

        @app.route('/view_company_wise_jobs',methods=['GET'])
        def view_company_wise_jobs():
            company_name = request.args.get('company_name')
            jobs = Jobs.query.filter_by(company_name=company_name).all()
            listed_jobs = {}
            active_jobs = []

            for job in jobs:
                active_jobs.append({
                    "company_name": job.company_name,
                    "CTC_offered": job.CTC_offered,
                    "job_location": job.job_location,
                    "job_desc": job.job_desc,
                    "job_experience": job.job_experience,
                    "job_status": job.job_status
                })
            listed_jobs["active job"] = active_jobs
            return listed_jobs



        @app.route('/apply_on_jobs', methods=['POST'])
        def apply_on_job():
            email = request.args.get('email')
            candidate = Candidate.query.filter_by(email=email).first()


            job_details = request.get_json()

            if candidate is None:
                return "please register first"
            
            else:
                job_applied = JobsApplied(
                    email = job_details['email'],
                    name = job_details['name'],
                    job_title = job_details['job_title'],
                    company_name = job_details['company_name'],
                    candidate_id = candidate.id
                )
                db.session.add(job_applied)
                db.session.commit()

                job_application = CandidatesApplied(
                    name = job_details['name'],
                    email = job_details['email'],
                    job_title = job_details['job_title'],
                    company_name = job_details['company_name'],
                    resume = "abc.com"
                )
                db.session.add(job_application)
                db.session.commit()
                return "application submitted successfully"
            

        @app.route('/view_applied_jobs', methods=['GET'])
        def view_applied_jobs():
            email = request.args.get('email')
            jobsApplied = JobsApplied.query.filter_by(email=email).all()

            applied_jobs = []
            applied_job_data = {}

            
            for job in jobsApplied:
                applied_jobs.append({
                    "job_tiltle": job.job_title,
                    "company_name": job.company_name
                })
            applied_job_data['jobs applied'] = applied_jobs
            return applied_job_data

        
        @app.route('/view_applications', methods=['GET'])
        def view_applications():
            company_name = request.args.get('company_name')
            candidatesApplied = CandidatesApplied.query.filter_by(company_name=company_name).all()

            application = []
            applications = {}

            
            for job in candidatesApplied:
                application.append({
                    "name": job.name,
                    "email": job.email,
                    "resume": job.resume
                })
            applications['application recieved'] = application
            return applications





        



        # db.drop_all()
        db.create_all()
        db.session.commit()
        return app


if __name__=="__main__":
    app = create_app()
    app.run(debug=True)