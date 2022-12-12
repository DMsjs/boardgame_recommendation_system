from numpy import dot
from numpy.linalg import norm
import numpy as np

def cos_sim(A, B):
    A, B = np.array(A), np.array(B)
    return dot(A, B)/(norm(A)*norm(B))