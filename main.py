'''
    File name: main.py
    Author: Tyche Analytics Co.
'''
from flask import Flask, request, g
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
import os
import json
import datetime
from tyche_binding_model import jr_model_stub
import hashlib
from tyche_db import Record
from tyche_db import query_db

app = Flask(__name__)
api = Api(app)
auth = HTTPTokenAuth(scheme='Token')

# Load config
with open('config.json', 'r') as infile:
    config = json.load(infile)

# Set database params
if(config["GAE"] == True):
    # Set URI for GAE
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % config['postgres']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Initialize Binding Model
bindingmodel = jr_model_stub.JRModel()

tokens = config['api_token_map']

@auth.verify_token
def verify_token(token):
    if token in tokens:
        g.current_user = tokens[token]
        return True
    return False

class api_version(Resource):
    @auth.login_required
    def get(self):
        return config['api_version']

class model_version(Resource):
    @auth.login_required
    def get(self):
        return config['model']

class binding_probability(Resource):
    @auth.login_required
    def post(self):
        # Retrieve POST json
        submission = request.get_json(force=True)
        
        currenttime = datetime.datetime.utcnow()
        
        username = g.current_user
        #username = "DEV"

        submission_md5 = hashlib.md5(json.dumps(submission, sort_keys=True).encode('utf-8')).hexdigest()

        # Generate model input and calculate probability
        modelinput = {"companycode": submission['CompanyCode'],
                       "divisioncode": submission['DivisionCode'], 
                       "insuredcity": submission['InsuredCity'],
                       "insuredstate": submission['InsuredState'], 
                       "insuredzip": submission['InsuredZip'],
                       "insuredname": submission['InsuredName'],
                       "groupline": submission['GroupLine']}

        probability, percentile = bindingmodel.predict(modelinput)
        
        # Construct return (MD5, etc.)
        newrecord = Record(uid = str(currenttime) + '*' + submission_md5, user = username, 
            timestamp = currenttime, submissionnumber = submission['SubmissionNumber'], companycode = 
            submission['CompanyCode'], divisioncode = submission['DivisionCode'], insuredname = 
            submission['InsuredName'], insuredaddress = submission['InsuredAddress'], insuredcity = 
            submission['InsuredCity'], insuredstate = submission['InsuredState'], insuredzip = 
            submission['InsuredZip'], groupline = submission['GroupLine'], product = 
            submission['Product'], submissionmd5 = submission_md5, modelname = 
            config['model']['model name'], modelversion = config['model']['model version'], 
            bindingprobability = probability, bindingpercentile = percentile, errorfield = "")
        
        # Add record to database
        db.session.add(newrecord)

        try:                                                                
            db.session.commit()
        except Exception as exception:  
            db.session.rollback()                                              
            print((str(exception)))                    
            return dict(message=type(exception).__name__), 400

        # Return
        return {"estimated probability": probability, "estimated percentile": percentile, 
        "md5sum": submission_md5}

class meter_count(Resource):
    @auth.login_required
    def get(self):
        
        #Collect datetime and user arguments
        date1 = request.args['startDate']
        date2 = request.args['endDate']

        username = g.current_user
        
        #Construct DB query
        try:
            record_count = query_db(username, date1, date2)
        except Exception as exception:
            print((str(exception)))
            return dict(message=type(exception).__name__), 400

        return record_count

api.add_resource(api_version, '/api_version')
api.add_resource(model_version, '/model_version')
api.add_resource(binding_probability, '/model/binding_probability')
api.add_resource(meter_count, '/meter_count')

if __name__ == '__main__':
    
    app.run(port=5000, ssl_context='adhoc', threaded=True, debug=True)
