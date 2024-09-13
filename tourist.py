import tasks as tsk
import numpy as np


class Tourist:
    def __init__(self, initial_tasks, visit_time):
        self.initial_tasks = initial_tasks
        self.visit_time = visit_time
        self.task_route = [None] * (visit_time + 1)
        self.task_list = [None] * (visit_time + 1)

    def tourist_route(self, aggregation_function, decision_method, tship=None, u_noise_mean=0.25, owa_weight=[]):
        if not tship:
            tship = round(0.75*self.visit_time, 0)
        time = 0
        i = 0  # cruise ship must be task 0
        tasks = self.initial_tasks.copy()
        self.task_route[time] = 0
        self.task_list[time] = self.initial_tasks

        dist_matrix = tsk.get_distance_matrix(tasks.latitude, tasks.longitude)

        # def tourist distance threshold
        theta = tsk.threshold_add_noise(tasks, dist_matrix)

        # def tourist task utility
        tasks.utility = tsk.ut_add_noise(tasks.utility, mean=u_noise_mean)

        # def tourist task agglomeration
        tasks.agglomeration_ct = tsk.ut_add_noise(tasks.agglomeration_ct, mean=25)

        print("time:", end=" ")
        while time < self.visit_time:
            possibilities = tsk.get_transition_matrix(dist_matrix[i:i+1], tasks.utility, tasks.agglomeration, theta, 2, aggregation_function, owa_weight=owa_weight)
            get_winner = tsk.DecisionMethods.select(decision_method)
            i = get_winner(possibilities)
            time += 1
            print(str(time), end=" ")
            self.task_route[time] = i
            if i:
                tasks.loc[[i], ["utility"]] = tasks.update_utility[i](tasks.utility[i])
                tasks.loc[[i], ["agglomeration"]] =  agglomeration(tasks.agglomeration[i],          )
            elif time == tship or (time > 10 and self.task_route[time-1] == 0):
                # If the tourist goes to the ship in time >= timeship, the tourist should stay in the ship
                tasks.loc[[0], ["utility"]] = 1
            tasks.loc[[0], ["utility"]] = tsk.cruise_utility(time, tasks.utility,
                                                             breaks=(round(0.4*self.visit_time, 0), tship))
            self.task_list[time] = tasks.iloc[:, 0:-1].copy()
