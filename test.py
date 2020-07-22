import cruiseshiptourism.tasks as tsk
import numpy as np
import pandas as pd
from cruiseshiptourism.tourist import Tourist


t0 = ("barco", 39.568276, 2.637640, 0, tsk.cruise_utility)
t1 = ("catedral", 39.567425, 2.648299, 0.9, tsk.low_penalitation)
t2 = ("castell", 39.563814,	2.619354, 0.9, tsk.low_penalitation)
t3 = ("almudaina", 39.567886, 2.647022, 0.6, tsk.standard_penalitation)
t4 = ("tren de soller", 39.576665, 2.653782, 0.5, tsk.high_penalitation)
t5 = ("Plaza mayor", 39.571371, 2.651813, 0.35, tsk.standard_penalitation)

tasks_ls = [t0, t1, t2, t3, t4, t5]
tasks = pd\
    .DataFrame(data=np.array(tasks_ls,
                             dtype=[("name", np.object),
                                    ("latitude", np.float64),
                                    ("longitude", np.float64),
                                    ("utility", np.float64),
                                    ("update_utility", np.object)]))


touristt = Tourist(tasks, 20)
touristt.tourist_route()
touristt.task_route
tasks.name[touristt.task_route]
