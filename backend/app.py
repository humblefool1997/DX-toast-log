import os
from flask import Flask,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
import pandas as pd
from flask_cors import CORS
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "VaccineTrails.sql"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)
CORS(app)


class UserNotFoundError(Exception):
    def __init__(self, message):
        self.message = message
@dataclass
class User(db.Model):
    email: str
    password: str
    full_name: str
    gender: str
    age: str
    address: str
    email = db.Column(db.String, primary_key=True)
    password = db.Column(db.String, unique=False, nullable=False)
    full_name = db.Column(db.String, unique=False, nullable=False)
    gender =db.Column(db.String, unique=False, nullable=False)
    age = db.Column(db.String, unique=False, nullable=False)
    address = db.Column(db.String, unique=False, nullable=False)
    


class VaccineTrails(db.Model):
    email = db.Column(db.String, primary_key=True)
    vaccine_group = db.Column(db.String, unique=False, nullable=False)
    dose = db.Column(db.String, unique=False, nullable=False)
    covid_test_result = db.Column(db.String, unique=False, nullable=False)
    


db.create_all()
db.session.commit()

@app.route('/')
def warmup():
    return jsonify("Backend REST API")

@app.route('/login',methods=['POST'])
def login():
    login_data = request.get_json()
    login_id = login_data['email']
    password =  login_data['password']
    login = User.query.filter_by(email=login_id, password=password).first()
    if login is not None:
        message = "Success"
    else:
        message = "Fail"
    return jsonify(message)

@app.route('/signup',methods=['POST'])
def signup():
    try:
            signup_volunteer_data = request.get_json()
            user = User(email = signup_volunteer_data['email'],
            password = signup_volunteer_data['password'],
            full_name = signup_volunteer_data['full_name'],
            gender = signup_volunteer_data['gender'],
            age = signup_volunteer_data['age'],
            address = signup_volunteer_data['address'],
            )
            db.session.add(user)
            db.session.commit()
    except Exception as e:
            print("Failed to add User")
            print(e)
    message = { "message":"Details updated successfully" }
    return message;

@app.route('/vaccine/applicant',methods=['POST'])
def collect_details():
    try:
        details = request.get_json()
        vaccineTrails = VaccineTrails(
        email = details['email'],
        vaccine_group = details['vaccine_group'],
        dose = details['dose'],
        covid_test_result = details['covid_test_result'])
        db.session.add(vaccineTrails)
        db.session.commit()
    except Exception as e:
            print("Failed to Update Vaccination Details")
            print(e)
    message = { "message":"Vaccine updated successfully" }
    return jsonify(message)


    

@app.route('/vaccine/all_result',methods=['GET'])
def consolidated_trail_results():
    mock_data = {
        "name":"SLCV2020",
         "type":"vaccine", 
         "vaccineGroup":"A", 
         "efficacy_rate":"0.9506",
          "result":{
              "volunteer":100,
              "confirm_positive":1
    }
    }
    return jsonify(mock_data)


@app.route('/vaccine/results',methods=['GET'])
def result_groupset():
    mock_data = {
        "name":"SLCV2020", "type":"vaccine", "vaccineGroup":"A", "dose":0.5, "efficacy_rate":"0.7500", "result":{
"volunteer":50,
"confirm_positive":2 }}
    error_message = {
 "error_message":"Phase 3 Trial in progress, please wait."
    }
    flag = True
    if flag  == True:
        error_message = mock_data;
    return jsonify(error_message)
      
    
if __name__ == '__main__':
    app.run(debug=True)