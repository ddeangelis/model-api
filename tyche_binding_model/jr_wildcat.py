'''
    File name: jr_wildcat.py
    Author: Tyche Analytics Co.
    Note: truncated file, suitable for model inference but not development
'''
"""wildcat is a library for handling categorical variables"""

from collections import defaultdict

def unpickle_defaultdict_data(defval_dict):
    defval, _dict = defval_dict
    return defaultdict(lambda: defval, _dict)
