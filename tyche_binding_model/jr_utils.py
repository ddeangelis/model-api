'''
    File name: jr_utils.py
    Author: Tyche Analytics Co.
    Note: truncated file, suitable for model inference, but not development
'''
"""Collect various utility functions for JR model"""

def mean(xs):
    if hasattr(xs,"__len__"):
        return sum(xs)/float(len(xs))
    else:
        acc = 0
        n = 0
        for x in xs:
            acc += x
            n += 1
        return acc/float(n)

def variance(xs,correct=True):
    n = len(xs)
    correction = n/float(n-1) if correct else 1
    mu = mean(xs)
    return correction * mean([(x-mu)**2 for x in xs])

def se(xs,correct=True):
    return sd(xs,correct)/sqrt(len(xs))
