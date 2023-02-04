from math import atan2
import numpy as np


# angle
def intersection(vect1,vect2):

    alpha = atan2(vect1[1],vect1[0])
    beta = atan2(vect2[1],vect2[0])

    if alpha >= beta:
        theta = alpha - beta
    else:
        theta = beta - alpha
    return np.degrees(theta)
    if np.degrees(theta) < 180:
        return np.degrees(theta)
    elif 180 < np.degrees(theta) < 360:
        return 360 - np.degrees(theta)
