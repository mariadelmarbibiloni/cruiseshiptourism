import ast
import logging
from math import floor
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

def update_utility_metrics(tourist_metrics, ntourist, tourists_obj, t, time):
    n_task= tourists_obj[ntourist].task_route[t+1]
    n_utility = tourists_obj[ntourist].initial_tasks["utility"][n_task]

    if t == 0:
        tourist_metrics.loc[ntourist, "minimum utility"] = n_utility

    tourist_metrics.loc[ntourist, "cumulative utility"] = tourist_metrics.loc[ntourist, "cumulative utility"] + n_utility
    tourist_metrics.loc[ntourist, "maximum utility"] = max(tourist_metrics.loc[ntourist, "maximum utility"], n_utility)
    tourist_metrics.loc[ntourist, "minimum utility"] = min(tourist_metrics.loc[ntourist, "minimum utility"], n_utility)
    tourist_metrics.loc[ntourist, "average utility"] = tourist_metrics.loc[ntourist, "average utility"] + n_utility/(time-1)

    return tourist_metrics

def update_distance_metrics(tourist_metrics, ntourist, tourists_obj, t, time):
    c_task= tourists_obj[ntourist].task_route[t]
    n_task= tourists_obj[ntourist].task_route[t+1]
    dist = tourists_obj[ntourist].dist_matrix[c_task,n_task]

    if t==0:
        tourist_metrics.loc[ntourist, "minimum distance"] = dist

    tourist_metrics.loc[ntourist, "cumulative distance"] = tourist_metrics.loc[ntourist, "cumulative distance"] + dist
    tourist_metrics.loc[ntourist, "maximum distance"] = max(tourist_metrics.loc[ntourist, "maximum distance"], dist)
    tourist_metrics.loc[ntourist, "minimum distance"] = min(tourist_metrics.loc[ntourist, "minimum distance"], dist)
    tourist_metrics.loc[ntourist, "average distance"] = tourist_metrics.loc[ntourist, "average distance"] + dist/(time-1)

    return tourist_metrics

def update_mass_visited_sites(tourist_metrics, ntourist, tourists_obj, t):
    n_task = tourists_obj[ntourist].task_route[t+1]
    if n_task > tourists_obj[ntourist].alpha:
        tourist_metrics.loc[ntourist, "mass visited sites"] += 1

    return tourist_metrics

def simulation(df_tasks_, ntourists, aggregation_function, decision_method, ct_agglomeration, time=20, u_noise_sigma=0.25, af_weight=[]):
    df_tasks = df_tasks_.copy()
    summary_df = pd.DataFrame(np.zeros(shape=(time, df_tasks.shape[0])),
                              columns=df_tasks['place'].values)
    tourist_routes = pd.DataFrame(np.zeros(shape=(ntourists, time + 1)),
                                  columns=[str(i) for i in range(0, time + 1)])
    tourist_metrics = pd.DataFrame(np.zeros(shape=(ntourists, 10)),
                                  columns=["cumulative utility", "maximum utility", "minimum utility", "average utility",
                                    "cumulative distance", "maximum distance", "minimum distance", "average distance",
                                    "different visited sites", "mass visited sites",
                                  ])

    dist_matrix = tsk.get_distance_matrix(df_tasks.latitude, df_tasks.longitude)
    ct_threshold =  tsk.threshold(dist_matrix) #[max, min]

    tourists_obj = [None for i in range(0, ntourists)]
    for t in range(0, time-1):
        logging.info("Time " + str(t) + " to " + str(t+1))

        for ntourist in range(0, ntourists):
            if ntourist == 0:
                logging.info("Num. Tourist: " + str(ntourist))
            if ntourist:
                if ntourist % floor(0.1*ntourists) == 0:
                    logging.info("Num. Tourist: " + str(ntourist))

            if t == 0: #1st time we create a Tourist obj for each toruist
                t_threshold = tsk.threshold_add_noise(ct_threshold)
                t_agglomeration = ct_agglomeration + tsk.ct_add_noise(ct_agglomeration, sigma=0.25*ct_agglomeration)
                
                cruise_ut = df_tasks.loc[[0], ["utility"]]
                df_tasks.utility = tsk.ct_add_noise(df_tasks.utility, sigma=u_noise_sigma)
                df_tasks.loc[[0], ["utility"]] = cruise_ut

                tourists_obj[ntourist] = Tourist(df_tasks, dist_matrix, time, t_threshold, t_agglomeration)
                df_tasks = df_tasks_.copy()
                
            tourists_obj[ntourist].tourist_route(t, aggregation_function, decision_method, summary_df,
                u_noise_sigma=u_noise_sigma, af_weight=af_weight)

            if t==0: #count selected tasks in t = 0 and t+1. After t = 1, sum t+1.
                tourist_routes.iloc[ntourist, t] = tourists_obj[ntourist].task_route[t]
                summary_df.iloc[t, tourists_obj[ntourist].task_route[t]] += 1

            tourist_routes.iloc[ntourist, t+1] = tourists_obj[ntourist].task_route[t+1]
            summary_df.iloc[t+1, tourists_obj[ntourist].task_route[t+1]] += 1

            if t != time-1:
                tourist_metrics = update_utility_metrics(tourist_metrics, ntourist, tourists_obj, t, time)
                tourist_metrics = update_distance_metrics(tourist_metrics, ntourist, tourists_obj, t, time)

        for ntourist in range(0, ntourists): #review mass loc. at the end of each time.
            if t not in [0, time-2]: #no mass cruiseship
                tourist_metrics = update_mass_visited_sites(tourist_metrics, ntourist, tourists_obj, t)
            tourist_metrics.loc[ntourist, "different visited sites"] = len(tourist_routes.iloc[ntourist].drop_duplicates())

    return {"tourist_routes": tourist_routes, "summary": summary_df, "tourist_metrics": tourist_metrics}

def dataframe_mean(df_list):
    n = len(df_list)
    df = df_list[0]
    for i in range(1, n):
        df = df.add(df_list[i])
    return (1/n)*df

if __name__ == "__main__":

    ntourists, time, aggregation_function, decision_method, noise_sigma, af_weight, niterations, ct_agglomeration = sa.get_sysarg()
    if not (ntourists or time or aggregation_function or decision_method or noise_sigma or af_weight or niterations or ct_agglomeration):
        message = """
        You must introduce all the parameters:
            simulation.py -n <ntourists> -t <time> -a <aggregation_function> -d <decision_method> -s <noise_sigma>
                 -w <af_weight> -i <niterations> -g <ct_agglomeration>
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
            "reviews": 'float',
            "utility": 'float'
        }
    )
    tasks = add_utility(tasks)
    
    niterations = int(niterations)
    sim_summaries = [None] * niterations
    sim_metrics = [None] * niterations
    
    for i in range(0, niterations):
        print ("Iteration " + str(i))
        sim_results = simulation(tasks, int(ntourists), aggregation_function, decision_method, float(ct_agglomeration), time=int(time),
            u_noise_sigma=float(noise_sigma), af_weight=ast.literal_eval(af_weight))
        print("\n")
        
        sim_summaries[i] = sim_results["summary"]
        sim_metrics[i] = sim_results["tourist_metrics"]

        #1st simulation result
        if i == 0:
            if not ast.literal_eval(af_weight):
                sim_results["tourist_routes"].to_csv(
                    f'test_sim/data_6500_1it/palma_poi_troutes_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_sigma_{noise_sigma}_it-{niterations}_agg-{ct_agglomeration}.csv',
                    index=False)
            else:
                sim_results["tourist_routes"].to_csv(
                    f'test_sim/data_6500_1it/palma_poi_troutes_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_sigma_{noise_sigma}_afw_{af_weight}_it-{niterations}_agg-{ct_agglomeration}.csv',
                    index=False)

    # mean of all simulations
    sim_summary=dataframe_mean(sim_summaries)
    sim_metrics_mean=dataframe_mean(sim_metrics)
    if not ast.literal_eval(af_weight):
        sim_summary.to_csv(
            f'test_sim/data_6500_1it/palma_poi_summary_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_sigma_{noise_sigma}_it-{niterations}_agg-{ct_agglomeration}.csv',
            index=False)
        sim_metrics_mean.to_csv(
            f'test_sim/data_6500_1it/palma_poi_metrics_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_sigma_{noise_sigma}_it-{niterations}_agg-{ct_agglomeration}.csv',
            index=False)
    else:
        sim_summary.to_csv(
            f'test_sim/data_6500_1it/palma_poi_summary_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_sigma_{noise_sigma}_afw_{af_weight}_it-{niterations}_agg-{ct_agglomeration}.csv',
            index=False)
        sim_metrics_mean.to_csv(
            f'test_sim/data_6500_1it/palma_poi_metrics_{ntourists}_{time}_{aggregation_function}_{decision_method}_noise_sigma_{noise_sigma}_afw_{af_weight}_it-{niterations}_agg-{ct_agglomeration}.csv',
            index=False)

executionTime = (t.time() - startTime)
logging.info('Execution time: ' + str(executionTime) + ' seconds')
