import ast
import logging
import numpy as np
import pandas as pd
import sys_arguments as sa
import tasks as tsk
import time as t
from tourist import Tourist

startTime = t.time()
logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)


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

def add_agglomeration(df):
    df["agglomeration_ct"] = 100
    df["agglomeration"] = 1
    return df

def simulation(df_tasks, ntourists, aggregation_function, decision_method, time=20, noise_it = 100, u_noise_mean=0.25, owa_weight=[]):
    summary_df = pd.DataFrame(np.zeros(shape=(time, df_tasks.shape[0])),
                              columns=df_tasks['place'].values)
    tourist_routes = pd.DataFrame(np.zeros(shape=(ntourists, time + 1)),
                                  columns=[str(i) for i in range(0, time + 1)])

    for tourist in range(0, ntourists):
        logging.info("Number of tourist: " + str(tourist))
        get_tourist = Tourist(df_tasks, time)
        get_tourist.tourist_route(aggregation_function, decision_method, noise_it=noise_it, u_noise_mean=u_noise_mean, owa_weight=owa_weight)
        for t in range(0, time):
            tourist_routes.iloc[tourist, t] = get_tourist.task_route[t]
            summary_df.iloc[t, get_tourist.task_route[t]] += 1
        print("\n")

    return {"tourist_routes": tourist_routes, "summary": summary_df}


if __name__ == "__main__":

    ntourists, time, aggregation_function, decision_method, noise_numit, noise_mean, owa_weight = sa.get_sysarg()
    if not (ntourists or time or aggregation_function or decision_method or noise_numit or noise_mean or owa_weight):
        message = """
        You must introduce all the parameters:
            simulation.py -n <ntourists> -t <time> -a <aggregation_function> -d <decision_method> -i <noise_numit> -m <noise_mean> -w <owa_weight>
        """
        raise Exception(message)

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
    tasks = add_agglomeration(tasks)
    
    sim_results = simulation(tasks, int(ntourists), aggregation_function, decision_method, time=int(time),
         noise_it=int(noise_numit), u_noise_mean=float(noise_mean), owa_weight=ast.literal_eval(owa_weight))

    if not owa_weight:
        sim_results["tourist_routes"].to_csv(
            f'test_sim/palma_poi_troutes_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_{noise_numit}_{noise_mean}.csv',
            index=False)
        sim_results["summary"].to_csv(
            f'test_sim/palma_poi_summary_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_{noise_numit}_{noise_mean}.csv',
            index=False)
    else:
        sim_results["tourist_routes"].to_csv(
            f'test_sim/palma_poi_troutes_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_{noise_numit}_{noise_mean}_{owa_weight}.csv',
            index=False)
        sim_results["summary"].to_csv(
            f'test_sim/palma_poi_summary_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_{noise_numit}_{noise_mean}_{owa_weight}.csv',
            index=False)

executionTime = (t.time() - startTime)
logging.info('Execution time: ' + str(executionTime) + ' seconds')
