from parse import *
from heuristic import *
from collections import defaultdict
def f():
    return 0
class Node():
    def __init__(self,core_id = None,parent = None, task_to_add = None, time_task_start = None, time_task_end = None):
        '''Create a Node object ie a partial scheduling
        parent = parent Node, None if root
        task_to_add : task added to the partial schedule
        time_task_start : time when the core will start computing the task
        time_task_end :  time  when the core will end computing the task
        '''   

        if parent is None:
            self.parent = None
            self.tasks_done_time = dict()
            self.g = 0
            self.hist = []
            self.schedule = dict()
            self.cores = defaultdict(f,{})
            
        else:
            self.parent = parent
            self.task_end_time = time_task_end
            self.tasks_done_time = parent.tasks_done_time.copy()
            self.tasks_done_time[task_to_add] = time_task_end
            
            self.cores = parent.cores.copy()
            self.cores[core_id] = time_task_end 
            self.g = max(parent.g, time_task_end)
            self.schedule = parent.schedule.copy()
            self.schedule[task_to_add] = (time_task_start, time_task_end)
            self.hist = parent.hist.copy()
            self.hist.append({'id':str(task_to_add),'startingTime':time_task_start,'duration':time_task_end-time_task_start,'process':str(core_id)})
                 
    def __repr__(self):
        return self.hist
    

class Tree():
    def __init__(self,path,cores):
        self.root= Node()
        self.task_graph = TaskGraph(path)
        self.cores = cores
        self.tasks = self.task_graph.tasks
        self.duration = {task.id:task.get_process_time() for task in self.tasks.values()}
        #print(self.duration)
        self.tasks_size = len(list(self.duration))
        self.sbl_tasks = get_sbl(self.tasks)

    def n_children(self,node):
        return len(self.children(node))

    def children(self,node):
        successors = []
        for task_id in self.tasks.keys():
            if task_id in node.tasks_done_time:
                continue
            #print([(x in self.tasks_done_time) for x in [task_.id for task_ in self.tasks[task_id].predecessors]]) 
            if not all([(x in node.tasks_done_time) for x in [task_.id for task_ in self.tasks[task_id].get_my_dependencies()]]):
                continue
            mx = max([0]+[node.tasks_done_time[x.id] for x in self.tasks[task_id].get_my_dependencies()])
            for core_id in range(self.cores):
                next_node = Node(core_id,node,task_id,max(node.cores[core_id],mx),max(node.cores[core_id],mx)+self.duration[task_id])
                successors.append(next_node)
        return successors
        
    def is_terminal(self,node):
        return (len(node.tasks_done_time) == self.tasks_size)

    def h(self,node):
            sbl = self.sbl_tasks
            ans = 0
            for task in self.tasks.keys():
                if task in node.tasks_done_time:
                    continue 
                else:
                    ans = max(ans,sbl[task])
            return ans 
                