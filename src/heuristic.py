from parse import *
sbl = {}
def sbl_function(task):
    if task.id in sbl:
        return sbl[task.id]
    if task.is_terminal():
        sbl[task.id] = task.time
    else:
        sbl[task.id] = task.time + max([sbl_function(u) for u in task.get_my_dependents()])
    return sbl[task.id]

def get_sbl(tasks):
    global sbl
    for task in tasks.values():
        sbl[task.id] = sbl_function(task)
    return sbl

    