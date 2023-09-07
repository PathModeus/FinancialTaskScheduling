

##################
# Batch account  #
##################

batch = {
    "name": "ab03centralesupelec",
    "key": "fj30Fw0ptMifYvtl4ccQN3rcTR5ArFGaNuTUsI0Q6N/8X3FClbdFGiIcCtzwLd9ZNyU+FQgq4BPB+ABaDM2QWA==",
    "url": "https://ab03centralesupelec.centralus.batch.azure.com"
}


###################################################
# Blob container which will store results of runs #
###################################################

blob_container = {
    "url": "https://as03centralesupelec.blob.core.windows.net/results",
    "sas_token": "?sv=2021-10-04&st=2023-03-29T11%3A15%3A10Z&se=2023-04-05T11%3A15%3A00Z&skoid=b3833228-1b9a-4ed4-8bf9-bf7394141afb&sktid=a8b8437b-013b-4de2-b105-e96932b6a9c5&skt=2023-03-29T11%3A15%3A10Z&ske=2023-04-05T11%3A15%3A00Z&sks=b&skv=2021-10-04&sr=c&sp=racwl&sig=I4mqD3k9bSJW7fJlJxFwHrkmi7vjBEDKB78kkfBPmMA%3D"
}
######################
# Configuration Pool #
######################

#rule of scability of pool
rule_scaling = (
                '// Get pending tasks for the past 5 minutes.\n'
                '$samples = $ActiveTasks.GetSamplePercent(TimeInterval_Minute * 5);\n'
                '// If we have fewer than 70 percent data points, we use the last sample point, otherwise we use the maximum of last sample point and the history average.\n'
                '$tasks = $samples < 70 ? max(0, $ActiveTasks.GetSample(1)) : '
                'max( $ActiveTasks.GetSample(1), avg($ActiveTasks.GetSample(TimeInterval_Minute * 5)));\n'
                '// If number of pending tasks is not 0, set targetVM to pending tasks, otherwise half of current dedicated.\n'
                '$targetVMs = $tasks > 0 ? $tasks : max(0, $TargetDedicatedNodes / 2);\n'
                '// The pool size is capped. This value should be adjusted according to your use case.\n'
                'cappedPoolSize = 128;\n'
                '$TargetLowPriorityNodes = max(0, min($targetVMs, cappedPoolSize));\n'
                '// Set node deallocation mode - keep nodes active only until tasks finish\n'
                '$NodeDeallocationOption = taskcompletion;'
               )


#####################
# Configuration Job #
#####################

#Repository (Github,Gitlab, etc.) contenant les inputs
repository = 'https://gitlab-student.centralesupelec.fr/tom.bray/st7-blob-repo.git'
#'https://fbitoo@dev.azure.com/fbitoo/demo_azure_batch/_git/demo_azure_batch'


#Commandes de la tâche de préparation(clonage d'un repo Azure Devops et installation des packages python nécessaires pour le process mpi)
cmd_prep_task = (
                  "bash -c 'git clone {0} ; cd st7-blob-repo ; chmod +x install.sh; ./install.sh'".format(repository)
                 )



######################
# Configuration Task #
######################

nb_processes = 5

#copier le script d'execution dans le dossier partagé du noeud
coordination_command = "bash -c 'ls; cp $AZ_BATCH_JOB_PREP_DIR/wd/st7-blob-repo/script.py $AZ_BATCH_NODE_SHARED_DIR; cp -r $AZ_BATCH_JOB_PREP_DIR/wd/st7-blob-repo/src $AZ_BATCH_NODE_SHARED_DIR; cp -r $AZ_BATCH_JOB_PREP_DIR/wd/st7-blob-repo/data $AZ_BATCH_NODE_SHARED_DIR'"

start_command = (
       "bash -c 'mpirun -np {0} -host $AZ_BATCH_HOST_LIST -wdir $AZ_BATCH_NODE_SHARED_DIR python3 $AZ_BATCH_NODE_SHARED_DIR/script.py --nb_process 2;'".format(nb_processes)
      )