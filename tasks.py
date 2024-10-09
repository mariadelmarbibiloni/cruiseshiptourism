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
        return np.multiply.reduce(functions)

    @staticmethod
    def minimum(functions):
        AggregationFunctions._raise_dimension_exception(functions)
        return np.asarray(functions).min(0)

    @staticmethod
    def harmonic_mean(functions):
        AggregationFunctions._raise_dimension_exception(functions)
        n = len(functions)
        min_ = 10**(-6)*np.ones(len(functions[0][0]))

        functions_inv = [1/np.asarray([f, [min_]]).max(0) for f in functions] #No divide by 0
        base_agg = (1/n)*np.add(*functions_inv)
        return np.array([[1/f for f in base_agg]])

    @staticmethod
    def owa(functions, owa_weight):
        AggregationFunctions._raise_dimension_exception(functions)
        f_matrix = np.matrix([i[0] for i in functions])
        f_sort = np.sort(f_matrix, axis=0) #ascending
        return np.array(np.average(f_sort, axis=0, weights=owa_weight)).ravel()

    @staticmethod
    def weighted_minimum(functions, weights):
        AggregationFunctions._raise_dimension_exception(functions)
        n_weights = [1 - w for w in weights]
        
        max_w_f = functions.copy()
        for i in range(0, len(functions)):
            max_w_f[i] = [max(n_weights[i], f) for f in functions[i][0]]
        
        return np.asarray(max_w_f).min(0)

    @staticmethod
    def all_or_nothing(functions):
        AggregationFunctions._raise_dimension_exception(functions)
        minimum = np.asarray(functions).min(0)[0]

        all_or_nothing = np.zeros(len(functions))
        for i in range(0, len(minimum)):
            if minimum[i] == 1:
                all_or_nothing[i] = 1
        
        return np.array(all_or_nothing)

    @staticmethod
    def wmean_of_mean_minimum(functions, p_list):
        AggregationFunctions._raise_dimension_exception(functions)
        p = p_list[0]

        mean = np.asarray(functions).mean(0)[0]
        minimum = np.asarray(functions).min(0)[0]

        return np.array([p*mean[i] + (1-p)*minimum[i] for i in range(0, len(mean))])

    @staticmethod
    def luk_weighted_mean(functions, weights):
        AggregationFunctions._raise_dimension_exception(functions)
        wmean = np.average(np.array(functions), axis=0, weights=weights)
        sw = sum(weighs)

        return np.array([max(0, wmean[i] + 1 - sw) for i in range(0, len(wmean))])

    @staticmethod
    def weighted_mean(functions, weights):
        AggregationFunctions._raise_dimension_exception(functions)

        return np.average(np.array(functions), axis=0, weights=weights)

    @staticmethod
    def dombi_mean(functions, weights, lambda_=2):
        AggregationFunctions._raise_dimension_exception(functions)

        dombi_f = functions.copy()

        min_ = 10**(-6)*np.ones(len(functions[0][0]))
        functions_inv = [1/np.asarray([f, [min_]]).max(0) for f in functions] #No divide by 0

        for i in range(0, len(functions)):
            dombi_f[i] = [ weights[i]*(1-f/f)**lambda_ for f in functions_inv[i][0]]
        
        dombi_m = np.asarray(dombi_f).sum(0)
        dombi_m = [1/(1 + (dombi_m[i])**(1/lambda_)) for i in range(0, len(dombi_m))]

        return np.array(dombi_m)
 
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
        elif af_name == "weighted_minimum":
            return AggregationFunctions.weighted_minimum
        elif af_name == "all_or_nothing":
            return AggregationFunctions.all_or_nothing
        elif af_name == "wmean_of_mean_minimum":
            return AggregationFunctions.wmean_of_mean_minimum
        elif af_name == "luk_weighted_mean":
            return AggregationFunctions.wmean_of_mean_minimum
        elif af_name == "weighted_mean":
            return AggregationFunctions.weighted_mean
        elif af_name == "dombi_mean":
            return AggregationFunctions.dombi_mean
        else:
            message = """
            You must select one of the following aggregation functions:
                * product
                * minimum
                * harmonic_mean
                * owa
                * weighted_minimum
                * all_or_nothing
                * wmean_of_mean_minimum
                * luk_weighted_mean
                * weighted_mean
                * dombi_mean
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


def agglomeration(alpha, ntourists):
    if ntourists < alpha:
        return 1 - (1/alpha)*ntourists
    else:
        return 10**(-6)


def ct_add_noise(tasks_parameter, sigma=0.25):
    if type(tasks_parameter) == float:
        parameter = [tasks_parameter]
    else:
        parameter = tasks_parameter.copy()

    white_noise = list(np.random.normal(0, sigma, size=len(parameter)))
    parameter  += white_noise

    for task in range(0, len(parameter)):
        if parameter[task] <= 0:
            parameter[task] = 10**(-6)
        elif parameter[task] > 1:
            parameter[task] = 1 

    if type(tasks_parameter) == float:
        return parameter[0]        
    else:
        return parameter


def threshold(dist_matrix):
    dist_max = dist_matrix.max()
    theta = dist_max / 2
    sort_dist = np.sort(np.ravel(dist_matrix.tolist()))
    pos_dist = [d for d in sort_dist if d > 0]

    return [theta, np.min(pos_dist)/2] # [theta, minimum dist != 0] 


def threshold_add_noise(threshold):
    max_ = threshold[0]
    min_ = threshold[1]
    
    dist_noise = np.random.normal(0, max_/4)
    theta = max(max_ + dist_noise, min_) # Compare with minimum distance not 0

    return theta


# Insert row i as dist_matrix to get possibilities vector for task i
def get_transition_matrix(dist_matrix, utilities, agglomeration, theta, n, aggregation_function, af_weight=[]):
    utilities_list = np.array(utilities)
    utilities_matrix = np.tile(utilities_list, (dist_matrix.shape[0], 1))
    
    agglomeration_matrix = np.tile(agglomeration, (dist_matrix.shape[0], 1))

    rf_distance_matrix = theta**n/ (theta**n + dist_matrix**n)

    aggregate = AggregationFunctions.select(aggregation_function)
    if af_weight:
        return aggregate([utilities_matrix, rf_distance_matrix, agglomeration_matrix], af_weight)
    return aggregate([utilities_matrix, rf_distance_matrix, agglomeration_matrix])

