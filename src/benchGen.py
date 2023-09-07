import datetime
import random
import dictToJSON

nbProcess = 50
nbJobs = 1300
nbDependencies = nbJobs*2
totalTime = datetime.timedelta(days = 0, hours = 6, minutes = 0, seconds = 0)

def generatingTasks(nbProcess, nbJobs, totalTime, nbDependencies):
    tasks = []
    nbTasksPerProcess = partitioningJobs(nbJobs, nbProcess)

    firstJob = 0

    for i in range(nbProcess):

        if i == nbProcess - 1:
            lastJob = nbJobs
        else :
            lastJob = nbTasksPerProcess[i]

        jobs = lastJob - firstJob + 1
        durationsJobs = partitioningTime(totalTime,jobs)
        beginning = datetime.timedelta()
        for j in range(len(durationsJobs)):

            if j == len(durationsJobs) - 1:
                end = totalTime
            
            else :
                end = durationsJobs[j]
            
            task = {'process' : i + 1, 'Data' : end - beginning, 'beginning' : beginning, 'end' : end, 'Dependencies' : []}
            tasks.append(task)

            beginning = end
        
        firstJob = lastJob

    random.shuffle(tasks)

    for i in range(len(tasks)):
        tasks[i]['id'] = str(i + 1)
    
    for i in range(nbDependencies):
        done = False 
        while not done :
            job1 = random.randint(1, nbJobs)
            job2 = random.randint(1, nbJobs)

            if job1 != job2 :
                dependencies1 = tasks[job1-1]['Dependencies']
                dependencies2 = tasks[job2-1]['Dependencies']

                if tasks[job1-1]['end'] - tasks[job2-1]['beginning'] <= datetime.timedelta() and job1 not in dependencies2:
                    tasks[job2-1]['Dependencies'].append(job1)
                    done = True
                
                if tasks[job2-1]['end'] - tasks[job1-1]['beginning'] <= datetime.timedelta() and job2 not in dependencies1:
                    tasks[job1-1]['Dependencies'].append(job2)
                    done = True
    
    for i in tasks:
        i['Data'] = str(i['Data'])
        i['beginning'] = str(i['beginning'])
        i['end'] = str(i['end'])

    return tasks        

def checkDependencies(tasks):
    nbDep = 0
    for task in tasks :
        for id in task['Dependencies']:
            nbDep += 1
            indix = getIndix(id, tasks)
            dep = tasks[indix]
            if dep['end'] > task['beginning']:
                return False

    return nbDep

def getIndix(id, tasks):

    for i in range(len(tasks)):
        if tasks[i]['id'] == id:
            return i
    
    return None
     
def partitioningJobs(totalLength, nbPart):
    L=[]

    for i in range(nbPart-1):
        partPos = random.randint(1,totalLength-1)
        while partPos in L:
            partPos = random.randint(1,totalLength-1)
        L.append(partPos)
    
    return(sorted(L))

def partitioningTime(totalDelta, nbPart):
    L=[]

    for i in range(nbPart-1):
        partTime = randomDelta(datetime.timedelta(0),totalDelta)
        while partTime in L:
            partTime = randomDelta(datetime.timedelta(0),totalDelta)
        L.append(partTime)
    
    return(sorted(L))

def randomDelta(beginning, end):
    return beginning + (end - beginning)*random.random()

tasks = generatingTasks(nbProcess, nbJobs, totalTime, nbDependencies)

name = str(nbProcess) + 'P_' + str(nbJobs) + 'J_' + str(nbDependencies) + 'D_'

dictToJSON.benchToJSON(tasks,name, totalTime)