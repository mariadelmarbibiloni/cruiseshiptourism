import getopt
import sys


def get_sysarg():
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'n:t:a:d:i:s:w:i:',
            ['ntourists=',
             'time=',
             'aggregation_function=',
             'decision_method=',
             'noise_sigma=',
             'owa_weight=',
             'niterations=',
             ])
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)

    ntourists, time, aggregation_function, decision_method, noise_sigma, owa_weight, niterations = [None for i in range(7)]
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
        elif opt in ('-w', '--owa_weight'):
            owa_weight = arg
        elif opt in ('-i', '--niterations'):
            niterations = arg

    return ntourists, time, aggregation_function, decision_method, noise_sigma, owa_weight, niterations
