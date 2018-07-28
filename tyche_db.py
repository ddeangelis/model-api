'''
    File name: tyche_db.py
    Author: Tyche Analytics Co.
'''
import os
import sys
import json
import csv
from sqlalchemy import create_engine  
from sqlalchemy import Column, String, Float, DateTime  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker

# How to load config from parent directory
with open('config.json', 'r') as infile:
    config = json.load(infile)

# Set up DB
if(config["GAE"] == True):
    # Set URI for GAE
    db_string = os.environ['SQLALCHEMY_DATABASE_URI']
else:
    db_string = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % config['postgres']

db = create_engine(db_string)  
base = declarative_base()

# Database Model
class Record(base):

    __tablename__ = 'records'

    uid = Column(String, primary_key=True)
    user = Column(String, unique=False, nullable=False)
    timestamp = Column(DateTime, unique=False, nullable=False)
    submissionnumber = Column(String, unique=False, nullable=False)
    companycode = Column(String, unique=False, nullable=False)
    divisioncode = Column(String, unique=False, nullable=False)
    insuredname = Column(String, unique=False, nullable=False)
    insuredaddress = Column(String, unique=False, nullable=False)
    insuredcity = Column(String, unique=False, nullable=False)
    insuredstate = Column(String, unique=False, nullable=False)
    insuredzip = Column(String, unique=False, nullable=False)
    groupline = Column(String, unique=False, nullable=False)
    product = Column(String, unique=False, nullable=True)
    submissionmd5 = Column(String, unique=False, nullable=False)
    modelname = Column(String, unique=False, nullable=False)
    modelversion = Column(String, unique=False, nullable=False)
    bindingprobability = Column(Float, unique=False, nullable=True)
    bindingpercentile = Column(Float, unique=False, nullable=True)
    errorfield = Column(String, unique=False, nullable=True)

    def __repr__(self):
        return '<Record %r>' % self.uid

def init_db():
    base.metadata.create_all(db)

# tyche_db.query_db("abc", "2017-12-20 02:59:38.609369", "2017-12-23 02:59:38.609369")
def query_db(username, t1, t2):

    print("Matching records...")

    Session = sessionmaker(db)
    session = Session()
    
    try:
        records = session.query(Record).filter_by(user = username).filter(Record.timestamp >= t1).filter(Record.timestamp < t2)
    except Exception as exception:
        print((str(exception)))
        session.close()
        return 
    
    session.close()
    return records.count()

def dump_db(outfile):
    
    print("Writing data dump")

    with open(outfile, 'w') as f:
        csvwriter = csv.writer(f, delimiter='|')
        csvwriter.writerow([column.name for column in Record.__mapper__.columns])
        
        datadump = db.execute("SELECT * FROM %s" % Record.__tablename__)
        csvwriter.writerows(datadump.fetchall())

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Error: requires more arguments. Try 'init', 'query', or 'dump'")
        sys.exit()
    if sys.argv[1] == "init":
        init_db()
    elif sys.argv[1] == "dump":
        if(len(sys.argv) != 3):
            print("Error: Unknown output file. Try 'python tyche_db.py dump <filename>'")
        else:
            outfile = sys.argv[2]
            dump_db(outfile)
    elif sys.argv[1] == "query":
        if(len(sys.argv) != 5):
            print("Error: Unknown query. Try 'python tyche_db.py query <user> <t1> <t2>'")
        else:
            user = sys.argv[2]
            t1 = sys.argv[3]
            t2 = sys.argv[4]
            meter_count = query_db(user, t1, t2)
            print("User: " + user + " t1: " + t1 + " t2: " + t2 + '\n'+ "meter_count: " + str(meter_count))
    else:
        print("Unknown argument: " + sys.argv[1])
            
