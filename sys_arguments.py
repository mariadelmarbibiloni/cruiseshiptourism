import getopt
import sys


def get_sysarg():
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'n:t:a:d:i:m:',
            ['ntourists=',
             'time=',
             'aggregation_function=',
             'decision_method=',
             'noise_numit='
             'noise_mean='
             ])
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)

    ntourists, time, aggregation_function, decision_method, noise_numit, noise_mean = [None for i in range(6)]
    for opt, arg in options:
        if opt in ('-n', '--ntourists'):
            ntourists = arg
        elif opt in ('-t', '--time'):
            time = arg
        elif opt in ('-a', '--aggregation_function'):
            aggregation_function = arg
        elif opt in ('-d', '--decision_method'):
            decision_method = arg
        elif opt in ('-i', '--noise_numit'):
            noise_numit = arg
        elif opt in ('-m', '--noise_mean'):
            noise_mean = arg

    return ntourists, time, aggregation_function, decision_method, noise_numit, noise_mean
