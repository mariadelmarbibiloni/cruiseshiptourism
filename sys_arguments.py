import getopt
import sys


def get_sysarg():
    try:
        options, remainder = getopt.getopt(
            sys.argv[1:],
            'n:t:',
            ['ntourists=',
             'time=',
             ])
    except getopt.GetoptError as err:
        print('ERROR:', err)
        sys.exit(1)

    ntourists, time = None, None
    for opt, arg in options:
        if opt in ('-n', '--ntourists'):
            ntourists = arg
        elif opt in ('-t', '--time'):
            time = arg

    return ntourists, time
