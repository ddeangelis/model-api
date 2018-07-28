'''
    File name: jr_model_stub.py
    Author: Tyche Analytics Co.
'''
import pandas as pd
import dill
import numpy as np
import os
from tyche_binding_model.jr_mca import mca_transformer
from tyche_binding_model.jr_wildcat import unpickle_defaultdict_data

class JRModel(object):
    """Make A JR Model instance.  

    Example Usage:

    model = JRModel() 
    p, perc = model.predict({"companycode":"01",
                       "divisioncode": "GC", 
                       "insuredcity":"Baton Rouge",
                       "insuredstate":"LA", 
                       "insuredzip":"23456", 
                       "groupline":"Comm'l General Liab"})"""

    def __init__(self):
        """initialize a JRModel instance, reading rfc_model and z_model from current directory"""
        time_str = "Fri_Jan_12_15:27:52_2018"
        prefix = "tyche_binding_model"
        with open(os.path.join(prefix, "rfc_model_%s.pkl" % time_str), 'rb') as f:
            self.rfc = dill.load(f)
        with open(os.path.join(prefix, "transform_data_%s.pkl" % time_str), 'rb') as f:
            transform_data = dill.load(f)
            self.transform = mca_transformer(transform_data)
        with open(os.path.join(prefix, "z_model_data_%s.pkl" % time_str), 'rb') as f:
            z_model_data = dill.load(f)
            self.z_model = unpickle_defaultdict_data(z_model_data)
        # with open("name_hashes.pkl", 'rb') as f:
        #     self.name_hashes = dill.load(f)
        with open(os.path.join(prefix, "train_percs_%s.pkl" % time_str), 'rb') as f:
            self.train_percs = dill.load(f)
        self.cat_predictors = ['companycode',
                               'divisioncode',
                               'insuredstate',
                               'groupline']
        
    def predict(self, submission_dict):
        """Accept a submission in dict format and return the estimated binding
        probability and percentile."""
        sub_df = pd.DataFrame(submission_dict, index=[0])
        z_score = self.z_model[submission_dict['insuredzip']]
        # bound_before = self.bound_before(submission_dict['insuredname'])
        X = np.hstack([self.transform(sub_df[self.cat_predictors]),
                       np.matrix([z_score]),
                       # np.matrix([bound_before])
        ])
        prob = self.rfc.predict_proba(X)[0, 1]
        perc = self.get_percentile(prob)
        return prob, perc

    def bulk_predict(self, val_df):
        bound_before = [self.bound_before(n) for n in val_df.insuredname]
        X = np.hstack([self.transform(val_df[self.cat_predictors]),
                             np.matrix([self.z_model[z] for z in val_df.insuredzip]).transpose(),
                            np.matrix([bound_before]).transpose()])
        probs = self.rfc.predict_proba(X)[:,1]
        return probs
        

    def get_percentile(self, p):
        if p < self.train_percs[0]:
            ans = 0
        elif p > self.train_percs[-1]:
            ans = 100
        else:
            for (i, ip), (j, jp) in pairs(list(zip(np.linspace(1, 99, 99), (self.train_percs)))):
                if ip <= p < jp:
                    ans = i
                    break
        return ans
            
        
        
def pairs(xs):
    return list(zip(xs[:-1],xs[1:]))

def test():
    model = JRModel() 
    prob, perc = model.predict({"companycode":"01",
                       "divisioncode": "GC", 
                       "insuredcity":"Baton Rouge",
                       "insuredstate":"LA", 
                       "insuredzip":"23456",
                       "insuredname":"John Smith",
                       "groupline":"Comm'l General Liab"})
    print(prob, perc)

if __name__ == '__main__':
    test()
