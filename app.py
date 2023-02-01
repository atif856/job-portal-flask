from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ
from config import db, SECRET_KEY
from dotenv import load_dotenv
from models.candidate import Candidate
from models.personalDetails import PersonalDetails
from models.experiences import Experiences
from models.projects import Projects
from models.skills import Skills
from models.education import Education
from models.certificates import Certificates
from models.jobs import Jobs
from models.jobsApplied import JobsApplied
from models.employer import Employer
from models.candidatesApplied import CandidatesApplied


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
        @app.route('/sign_up', methods=['POST'])
        def sign_up():
            new_user = request.get_json()
            new_user_details = Candidate(
                email=new_user['email'],
                password=new_user['password'],
                username=new_user['username']
            )
            db.session.add(new_user_details)
            db.session.commit()
            return jsonify(msg="User Added Successfully")




        db.drop_all()
        db.create_all()
        db.session.commit()
        return app


if __name__=="__main__":
    app = create_app()
    app.run(debug=True)