import cruiseshiptourism.tasks as tsk


class Tourist:
    def __init__(self, initial_tasks, visit_time):
        self.initial_tasks = initial_tasks
        self.visit_time = visit_time
        self.task_route = [None] * (visit_time + 1)
        self.task_list = [None] * (visit_time + 1)

    def tourist_route(self):
        time = 0
        i = 0  # cruise ship must be task 0
        tasks = self.initial_tasks.copy()
        self.task_route[time] = 0
        self.task_list[time] = self.initial_tasks
        dist_matrix = tsk.get_distance_matrix(tasks.latitude, tasks.longitude)
        theta = dist_matrix.max() / 2

        print("time:", end=" ")
        while time < 20:
            posibilities = tsk.get_transition_matrix(dist_matrix[i], tasks.utility, theta, 2)
            i = tsk.choice_task(posibilities)
            time += 1
            print(time, end=" ")
            self.task_route[time] = i
            if i:
                tasks.utility[i] = tasks.update_utility[i](tasks.utility[i])
            tasks.utility[0] = tsk.cruise_utility(time, tasks.utility, breaks=(8, 10))
            self.task_list[time] = tasks.iloc[:, 0:-1].copy()
