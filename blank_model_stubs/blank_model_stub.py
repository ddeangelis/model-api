'''
    File name: blank_model_stub.py
    Author: Tyche Analytics Co.
'''
import pandas as pd
import dill
import time
        
class BindingModel(object):
    """Make A Binding Model instance.  

    Example Usage:

    model = BindingModel() 
    p = model.predict({"companycode":"01",
                       "divisioncode": "GC", 
                       "insuredcity":"Baton Rouge",
                       "insuredstate":"LA", 
                       "insuredzip":23456, 
                       "groupline":"Comm'l General Liab"})"""

    def __init__(self):
        """initialize a Model instance"""
        time.sleep(.1)

    def predict(self, submission_dict):
        """Accept a submission in dict format and return 0."""
        time.sleep(1)
        return 0
        