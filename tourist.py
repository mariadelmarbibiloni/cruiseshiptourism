import tasks as tsk
import numpy as np


class Tourist:
    def __init__(self, initial_tasks, dist_matrix, visit_time):
        self.initial_tasks = initial_tasks
        self.dist_matrix = dist_matrix
        self.visit_time = visit_time
        self.task_route = [None] * (visit_time)
        self.task_list = [None] * (visit_time)
        self.theta = None

    def tourist_route(self, time, aggregation_function, decision_method, tship=None, u_noise_sigma=0.25, owa_weight=[]):
        if not tship:
            tship = round(0.75*self.visit_time, 0)

        if time == 0:
            i = 0
            self.task_route[time] = 0
            self.task_list[time] = self.initial_tasks

            tasks = self.initial_tasks.copy()
            # def tourist task utility
            tasks.utility = tsk.ut_add_noise(tasks.utility, sigma=u_noise_sigma)
            # def tourist distance threshold
            self.theta = tsk.threshold_add_noise(tasks, self.dist_matrix)
            # def tourist task agglomeration
            #tasks.agglomeration_ct = tsk.ut_add_noise(tasks.agglomeration_ct, sigma=25)
        else:
            tasks = self.initial_tasks.copy()
            i = self.task_route[time]

        possibilities = tsk.get_transition_matrix(self.dist_matrix[i:i+1], tasks.utility,#
            # tasks.agglomeration,
            self.theta, 2, aggregation_function, owa_weight=owa_weight)
        get_winner = tsk.DecisionMethods.select(decision_method)
        i = get_winner(possibilities)

        time += 1
        self.task_route[time] = i
        if i:
            tasks.loc[[i], ["utility"]] = tasks.update_utility[i](tasks.utility[i])
            tasks.loc[[i], ["tourist_num"]] += 1
        elif time == tship and self.task_route[time-1] == 0:
            # If the tourist goes to the ship in time >= timeship, the tourist should stay in the ship
            tasks.loc[[0], ["utility"]] = 1

        tasks.loc[[0], ["utility"]] = tsk.cruise_utility(time, tasks.utility,
                                                        breaks=(round(0.4*self.visit_time, 0), tship))
        self.initial_tasks = tasks.copy()
        self.task_list[time] = tasks.iloc[:, 0:-1].copy()