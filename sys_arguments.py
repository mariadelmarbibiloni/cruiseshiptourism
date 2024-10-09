import getopt
import sys


def get_sysarg():
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'n:t:a:d:s:w:i:g:',
            ['ntourists=',
             'time=',
             'aggregation_function=',
             'decision_method=',
             'noise_sigma=',
             'af_weight=',  #If is p, add as [p]
             'niterations=',
             'ct_agglomeration='
             ])
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)

    ntourists, time, aggregation_function, decision_method, noise_sigma, af_weight, niterations, ct_agglomeration = [None for i in range(8)]
    for opt, arg in options:
        if opt in ('-n', '--ntourists'):
            ntourists = arg
        elif opt in ('-t', '--time'):
            time = arg
        elif opt in ('-a', '--aggregation_function'):
            aggregation_function = arg
        elif opt in ('-d', '--decision_method'):
            decision_method = arg
        elif opt in ('-s', '--noise_sigma'):
            noise_sigma = arg
        elif opt in ('-w', '--af_weight'):
            af_weight = arg
        elif opt in ('-i', '--niterations'):
            niterations = arg
        elif opt in ('-g', '--ct_agglomeration'):
            ct_agglomeration = arg

    return ntourists, time, aggregation_function, decision_method, noise_sigma, af_weight, niterations, ct_agglomeration
