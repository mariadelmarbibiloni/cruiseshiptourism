import getopt
import sys


def get_sysarg():
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'n:t:a:d:',
            ['ntourists=',
             'time=',
             'aggregation_function=',
             'decision_method='
             ])
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)

    ntourists, time, aggregation_function, decision_method = [None for i in range(4)]
    for opt, arg in options:
        if opt in ('-n', '--ntourists'):
            ntourists = arg
        elif opt in ('-t', '--time'):
            time = arg
        elif opt in ('-a', '--aggregation_function'):
            aggregation_function = arg
        elif opt in ('-d', '--decision_method'):
            decision_method = arg

    return ntourists, time, aggregation_function, decision_method
