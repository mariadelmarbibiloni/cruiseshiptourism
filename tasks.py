import numpy as np
import math
from scipy.spatial.distance import pdist, squareform
from vincenty import vincenty


def standard_penalty(utility):
    return utility/4


def low_penalty(utility):
    return utility/2


def high_penalty(utility):
    return utility/8


def cruise_utility(time, utilities, breaks=(8, 10)):
    u_max = -math.inf
    u_min = math.inf
    for utility in utilities:
        u_max = max(u_max, utility)
        u_min = min(u_min, utility)

    if time <= breaks[0]:
        lambda_ = 0
    elif time < breaks[1]:
        lambda_ = (time - breaks[0])/(breaks[1]-breaks[0])
    else:
        lambda_ = 1

    return lambda_*u_max + (1-lambda_)*u_min


def euclidean_distance(x, y):
    return np.linalg.norm(x-y)


def get_distance_matrix(lat, lon):
    coor_list = list(zip(lat, lon))
    return squareform(pdist(coor_list, lambda p1, p2: vincenty(p1, p2, miles=False)))


# Insert row i as dist_matrix to get posibilities vector for task i
def get_transition_matrix(dist_matrix, utilities, theta, n):
    utilities_ = utilities
    if dist_matrix.ndim == 2:
        utilities_ = utilities.to_list()
    return (theta**n)*utilities_/(theta**n + dist_matrix**n)


def choice_task(posibilities):
    rng = np.random.default_rng()
    task_list = range(0, len(posibilities))
    p_prob = posibilities/np.sum(posibilities)
    return rng.choice(task_list, 1, p=list(p_prob))[0]
