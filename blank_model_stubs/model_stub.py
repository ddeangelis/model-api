'''
    File name: model_stub.py
    Author: Tyche Analytics Co.
'''
import pandas as pd
import dill
        
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
        """initialize a BindingModel instance, reading rfc_model and z_model from current directory"""
        with open("rfc_model.pkl", 'rb') as f:
            self.rfc = dill.load(f)
        with open("transform.pkl", 'rb') as f:
            self.transform = dill.load(f)
        with open("z_model.pkl", 'rb') as f:
            self.z_model = dill.load(f)
        self.cat_predictors = ['companycode',
                               'divisioncode',
                               'insuredstate',
                               'groupline']

    def predict(self, submission_dict):
        """Accept a submission in dict format and return the estimated binding probability."""
        sub_df = pd.DataFrame(submission_dict, index=[0])
        X = np.hstack([self.transform(sub_df[self.cat_predictors]),
                       np.matrix([self.z_model[submission_dict['insuredzip']]])])
        return rfc.predict_proba(X)[0, 1]
        
        