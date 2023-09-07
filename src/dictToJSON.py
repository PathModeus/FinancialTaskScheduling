import json

def benchToJSON(list, name, time):
    dictBench = { "totalTime" : str(time), "nodes" : {} }
    dictTest = { "nodes" : {} }

    for task in list :
        id = task['id']

        nodeBench = task

        nodeTest = { "Data" : task['Data'], "Dependencies" : task['Dependencies'] }

        dictBench['nodes'][id] = nodeBench

        dictTest["nodes"][id] = nodeTest

    with open('data/generated_graphs/' + name + 'test.json','w') as outfile:
        json.dump(dictTest,outfile)
    
    with open('data/generated_graphs/' + name + 'benchmark.json','w') as outfile:
        json.dump(dictBench,outfile)
    