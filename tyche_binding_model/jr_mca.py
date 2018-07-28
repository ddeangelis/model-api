'''
    File name: jr_mca.py
    Author: Tyche Analytics Co.
    Note: truncated file, suitable for model inference, but not development
'''
import numpy as np

# Thu Nov 9 14:36:28 EST 2017 We refactor the mca function to return
# the necessary data elements to make an MCA transformer, to be passed
# on to mca_transformer below, rather than simply returning the
# function directly.  We do this so that we can pickle the transformer
# data and load it into make_transformer on the production server at
# runtime, because pickling python code can lead to unpredictable bugs.

def mca_transformer(transform_data):
    """accept data from an mca call and make a transformer"""
    M, dims, index, v0v1 = transform_data
    def transform(dfp):
        # dims, index, v0v1
        P = np.zeros((len(dfp), dims), dtype=float)
        print("transforming")
        for i, (_, row) in (enumerate(dfp.iterrows())):
            ivec = np.zeros(M)
            for col, val in zip(row.index, row):
                if (col, val) in index:
                    ivec[index[col, val]] = 1
            proj = ivec.dot(v0v1)
            assert(all(proj.imag == 0))
            P[i,:] = proj.real
        return P
    return transform

