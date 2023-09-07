import json


from datetime import datetime,timedelta
from collections import OrderedDict


class Task:
    def __init__(self,id,time,dependencies):
        self.id = int(id)
        self.time =(datetime.strptime(time[:-1],"%H:%M:%S.%f")-datetime(1900,1,1)).total_seconds()
        self.dependencies_ids = dependencies
        self.my_dependencies = []
        self.my_dependents = []
        self.is_finished = False
        self.start = None
        self.processing = False
        self.end = None

        if self.my_dependencies:
            self.is_ready = True
        else:
            self.is_ready = False

        self.id = int(id)
        

    def get_my_dependents(self):
        return self.my_dependents
    
    def get_my_dependencies(self):
        return self.my_dependencies
    
    def update_ready_to_start(self):
        # I don't think this is the best way to do this,
        # Maybe a better way is
        if not self.is_finished:
            ready = True
            for task in self.my_dependencies:
                ready = ready and task.is_finished()
            
            self.ready = ready
        else:
            return False

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def set_start(self,start):
        self.start = start
        self.processing = True

    def set_end(self, end):
        self.end = end
        self.processing = False
        self.is_finished = True

    def get_process_time(self):
        return self.time

    def is_already_finished(self):
        return self.is_finished

    def is_ready_to_start(self):
        return self.is_ready

    # Funtions used only on the construction of the Graph
    def set_new_dependencie(self,new_dependencie):
        self.my_dependencies.append(new_dependencie)
    def set_new_dependent(self,new_dependent):
        self.my_dependents.append(new_dependent)
    def get_my_dependencies(self):
        return self.my_dependencies
    def get_dependencies_ids(self):
        return self.dependencies_ids
    
    def is_terminal(self):
        return len(self.my_dependents)==0
    
    
    


class TaskGraph:
    def __init__(self,file_path):
        self.tasks = OrderedDict({})

        f = open(file_path)
        data = json.load(f)
        f.close()

        data = data['nodes']

        for k, v in data.items():
            self.tasks[int(k)] = Task(k,v['Data'],v['Dependencies'])

        for k in self.tasks.keys():
            for id in self.tasks[k].get_dependencies_ids():
                self.tasks[k].set_new_dependencie(self.tasks[id])
                self.tasks[id].set_new_dependent(self.tasks[k])

    def get_task(self,id):
        return self.tasks[id]
    
    def get_available_tasks(self):
        available_tasks_ids = []
        for id in self.tasks.keys():
            self.tasks[id].update_ready_to_start()
            if self.tasks[id].is_ready_to_start():
                available_tasks_ids.append(id)
        return available_tasks_ids


