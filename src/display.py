import matplotlib.pyplot as plt
import numpy as np

# #test data 
# data = [{'id': '1', 'startingTime': 0, 'process' : '1', 'duration': 10}, 
# {'id': '2', 'startingTime': 0, 'process' : '2', 'duration': 5},
# {'id': '3', 'startingTime': 0, 'process' : '3', 'duration': 10},
# {'id': '4', 'startingTime': 10, 'process' : '2', 'duration': 10}]

# data2 = [{'id': '1', 'startingTime': 0, 'process' : '1', 'duration': 10}, 
# {'id': '2', 'startingTime': 0, 'process' : '2', 'duration': 5},
# {'id': '3', 'startingTime': 0, 'process' : '3', 'duration': 10},
# {'id': '4', 'startingTime': 10, 'process' : '2', 'duration': 5},
# {'id': '5', 'startingTime': 0, 'process' : '4', 'duration': 10},
# {'id': '6', 'startingTime': 0, 'process' : '5', 'duration': 5},
# {'id': '7', 'startingTime': 10, 'process' : '4', 'duration': 5},
# {'id': '8', 'startingTime': 5, 'process' : '5', 'duration': 10},
# {'id': '9', 'startingTime': 5, 'process' : '2', 'duration': 5},
# {'id': '11', 'startingTime': 10, 'process' : '1', 'duration': 5},
# {'id': '10', 'startingTime': 10, 'process' : '3', 'duration': 5}]

def showChronogram(tasksList, timeScale = 'sec', showId = True ): 

    fig, ax = plt.subplots(1, figsize=(16,6))

    factor = 1 

    if timeScale == 'hour' :
        factor = 1/3600
    
    elif timeScale == 'day' :
        factor = 1/(3600 * 24)

    for task in tasksList :
        ax.barh(task['process'],factor*task['duration'],left=task['startingTime']*factor, label=task['id'], color = "royalblue", edgecolor="black")
        
        if showId :
            ax.text((task['startingTime']+task['duration']/2)*factor,task['process'], task['id'],fontsize = 'xx-large')
    
    plt.title('Chronogram of tasks by process')

    if timeScale == 'hour':
        plt.xlabel('Date in hours')

    if timeScale == 'sec' :
        plt.xlabel('Date in seconds')

    if timeScale == 'day' :
        plt.xlabel('Date in days')

    plt.ylabel('Process Number')
    plt.show()
