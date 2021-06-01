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
    def select(af_name):
        if af_name == "product":
            return AggregationFunctions.product
        elif af_name == "minimum":
            return AggregationFunctions.minimum
        elif af_name == "harmonic_mean":
            return AggregationFunctions.harmonic_mean
        else:
            message = """
            You must select one of the following aggregation functions:
                * product
                * minimum
                * harmonic_mean
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


# Insert row i as dist_matrix to get possibilities vector for task i
def get_transition_matrix(dist_matrix, utilities, theta, n, aggregation_function="product"):
    utilities_list = np.array(utilities)
    utilities_matrix = np.tile(utilities_list, (dist_matrix.shape[0], 1))

    rf_distance_matrix = theta**n / (theta**n + dist_matrix**n)
    aggregate = AggregationFunctions.select(aggregation_function)
    return aggregate([utilities_matrix, rf_distance_matrix])

