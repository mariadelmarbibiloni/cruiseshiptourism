import math 
import numpy as np
from scipy.spatial.distance import pdist, squareform
from vincenty import vincenty


class AggregationFunctions:  # function is a list of numpy matrix functions with the same shape

    @staticmethod
    def _raise_dimension_exception(functions):
        shapes = [f.shape for f in functions]
        if len(set(shapes)) != 1:
            message = """
            Functions cannot be aggregated.
            Check if all numpy matrices or arrays have the same shape.
            """
            raise Exception(message)

    @staticmethod
    def product(functions):
        AggregationFunctions._raise_dimension_exception(functions)
        return np.multiply(*functions)

    @staticmethod
    def minimum(functions):
        AggregationFunctions._raise_dimension_exception(functions)
        return np.minimum(*functions)

    @staticmethod
    def harmonic_mean(functions):
        AggregationFunctions._raise_dimension_exception(functions)
        functions = functions
        n = len(functions)
        functions_inv = [1/f for f in functions]
        base_agg = (1/n)*np.add(*functions_inv)
        return np.array([[1/f for f in base_agg]])


    @staticmethod
    def owa(functions, owa_vweight):
        AggregationFunctions._raise_dimension_exception(functions)
        f_matrix = np.matrix([i[0] for i in functions])
        f_sort = np.sort(f_matrix, axis=0)
        return np.array(np.average(f_sort, axis=0, weights=df['wheight'])).ravel()
        
 
    @staticmethod
    def select(af_name):
        if af_name == "product":
            return AggregationFunctions.product
        elif af_name == "minimum":
            return AggregationFunctions.minimum
        elif af_name == "harmonic_mean":
            return AggregationFunctions.harmonic_mean
        elif af_name == "owa":
            return AggregationFunctions.owa
        else:
            message = """
            You must select one of the following aggregation functions:
                * product
                * minimum
                * harmonic_mean
                * owa
            """
            raise Exception(message)


class DecisionMethods:

    @staticmethod
    def intervals(possibilities):
        possibilities = possibilities.ravel()
        rng = np.random.default_rng()
        task_list = range(0, len(possibilities))
        p_prob = possibilities/np.sum(possibilities)
        return rng.choice(task_list, 1, p=p_prob)[0]

    @staticmethod
    def maximum(possibilities):
        possibilities = possibilities.ravel()
        idx_max = np.flatnonzero(possibilities == np.max(possibilities))
        len_ = len(idx_max)
        if len_ > 1:
            rng = np.random.default_rng()
            idx_max_winner = rng.choice(idx_max, 1)[0]
        else:
            idx_max_winner = idx_max[0]
        return idx_max_winner

    @staticmethod
    def select(dm_name):
        if dm_name == "intervals":
            return DecisionMethods.intervals
        elif dm_name == "maximum":
            return DecisionMethods.maximum
        else:
            message = """
            You must select one of the following decision methods:
                * intervals
                * maximum
            """
            raise Exception(message)


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

    return lambda_*u_max/2 + (1-lambda_)*2*u_min


def euclidean_distance(x, y):
    return np.linalg.norm(x-y)


def get_distance_matrix(lat, lon):
    coor_list = list(zip(lat, lon))
    return squareform(pdist(coor_list, lambda p1, p2: vincenty(p1, p2, miles=False)))


def ut_add_noise(tasks_utility, numit=100, mean=0.25):
    main_task_utility = tasks_utility.copy()
    utilities = tasks_utility.copy()

    white_noise = list(np.random.normal(0, mean, size=len(utilities)))
    utilities  += white_noise
    if numit > 1:
        for n in range(1, numit):
            white_noise = list(np.random.normal(0, mean, size=len(utilities)))
            utilities += main_task_utility + white_noise

    utilities = utilities/numit

    for task in range(0, len(utilities)):
        if utilities[task] <= 0:
            utilities[task] = 10**(-6)
        elif utilities[task] > 1:
            utilities[task] = 1
            
    return utilities

def threshold_add_noise(tasks, dist_matrix, numit=100):
    dist_max = dist_matrix.max()
    sort_dist = np.sort(np.ravel(dist_matrix.tolist()))
    pos_dist = [d for d in sort_dist if d > 0]
    dist_noise_mean = np.mean([np.random.normal(0, dist_max / 4) for i in range(1, numit)])
    theta = max(dist_max / 2 + dist_noise_mean, np.min(pos_dist)) # Compare with minimum distance not 0

    return theta


# Insert row i as dist_matrix to get possibilities vector for task i
def get_transition_matrix(dist_matrix, utilities, theta, n, aggregation_function, owa_weight=[]):
    utilities_list = np.array(utilities)
    utilities_matrix = np.tile(utilities_list, (dist_matrix.shape[0], 1))
    rf_distance_matrix = theta**n/ (theta**n + dist_matrix**n)
    aggregate = AggregationFunctions.select(aggregation_function)
    if owa_weight:
        return aggregate([utilities_matrix, rf_distance_matrix], owa_weight)
    return aggregate([utilities_matrix, rf_distance_matrix])

