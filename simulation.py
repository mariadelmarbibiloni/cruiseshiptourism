import tasks as tsk
import numpy as np
import pandas as pd
from tourist import Tourist
import sys
import getopt


def set_penalty(row, lows, highs):
    if row.place == "cruise ship":
        return tsk.cruise_utility
    elif row.place in lows:
        return tsk.low_penalty
    elif row.place in highs:
        return tsk.high_penalty
    else:
        return row.update_utility


def add_utility(df):
    df["update_utility"] = tsk.standard_penalty
    low = [
        "Plaça de Cort",
        "Plaça de toros de Palma",
        "Plaza Del Mercat",
        "Plaça del Rei Joan Carles I"
    ]
    high = [
        "Catedral-Basílica de Santa María de Mallorca",
        "Castell de Bellver",
        "Royal Palace of La Almudaina",
        "Museu Fundación Juan March, Palma",
        "Museo de Mallorca",
        "Museu Diocesà de Mallorca"
    ]

    df["update_utility"] = df.apply(lambda row: set_penalty(row, low, high), axis=1)

    return df


def simulation(df_tasks, ntourists, time=20):
    summary_df = pd.DataFrame(np.zeros(shape=(time, df_tasks.shape[0])),
                              columns=df_tasks['place'].values)
    tourist_routes = pd.DataFrame(np.zeros(shape=(ntourists, time + 1)),
                                  columns=[str(i) for i in range(0, time + 1)])

    for tourist in range(0, ntourists):
        get_tourist = Tourist(df_tasks, time)
        get_tourist.tourist_route()
        for t in range(0, time):
            tourist_routes.iloc[tourist, t] = get_tourist.task_route[t]
            summary_df.iloc[t, get_tourist.task_route[t]] += 1
        print("\n")

    return {"tourist_routes": tourist_routes, "summary": summary_df}


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


if __name__ == "__main__":

    ntourists, time = get_sysarg()
    if not (ntourists or time):
        print('simulation.py -n <ntourists> -t <time>')
        sys.exit(1)

    tasks = pd.read_csv(
        "palmadata/palmapointsofinterest_cleaned.csv",
        header=0,
        dtype={
            "place": 'str',
            "description": 'str',
            "latitude": 'float',
            "longitude": 'float',
            "stars": 'float',
            "reviews": 'float'
        }
    )
    tasks = add_utility(tasks)

    sim_results = simulation(tasks, int(ntourists), time=int(time))

    sim_results["tourist_routes"].to_csv(f'palmadata/palma_poi_troutes_{ntourists}_{time}.csv', index=False)
    sim_results["summary"].to_csv(f'palmadata/palma_poi_summary_{ntourists}_{time}.csv', index=False)