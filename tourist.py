import tasks as tsk
import numpy as np


class Tourist:
    def __init__(self, initial_tasks, dist_matrix, visit_time, theta, alpha):
        self.initial_tasks = initial_tasks
        self.dist_matrix = dist_matrix
        self.visit_time = visit_time
        self.theta = theta # distance threshold
        self.alpha = alpha # agglomeration threshold
        self.task_route = [None] * (visit_time)
        self.task_list = [None] * (visit_time)


    def tourist_route(self, time, aggregation_function, decision_method, summary_df, tship=None, u_noise_sigma=0.25, owa_weight=[]):
        tasks = self.initial_tasks.copy()

        if not tship:
            tship = round(0.75*self.visit_time, 0)

        if time == 0:
            i = 0
            self.task_route[time] = 0
            self.task_list[time] = self.initial_tasks
        else:
            i = self.task_route[time]

        ntourists_4task = summary_df.iloc[time+1].values.tolist()
        tasks_agglomeration = [tsk.agglomeration(self.alpha, ntourists_task) for ntourists_task in ntourists_4task]

        possibilities = tsk.get_transition_matrix(self.dist_matrix[i:i+1], tasks.utility, tasks_agglomeration,
            self.theta, 2, aggregation_function, owa_weight=owa_weight)
        get_winner = tsk.DecisionMethods.select(decision_method)
        i = get_winner(possibilities)

        time += 1
        self.task_route[time] = i
        if i:
            tasks.loc[[i], ["utility"]] = tasks.update_utility[i](tasks.utility[i])
        elif time == tship and self.task_route[time-1] == 0:
            # If the tourist goes to the ship in time >= timeship, the tourist should stay in the ship
            tasks.loc[[0], ["utility"]] = 1

        tasks.loc[[0], ["utility"]] = tsk.cruise_utility(time, tasks.utility,
                                                        breaks=(round(0.4*self.visit_time, 0), tship))
        
        self.initial_tasks = tasks.copy()
        self.task_list[time] = tasks.iloc[:, 0:-1].copy()