'''
Tools to parallelize shell commands

The main function is:

    parallelize(tasks, ntasks)

where tasks is a list of tasks, where each task is a list of shell commands. The
number of concurrent tasks is given by ntasks.

Example to create some files then clean them up:
    [
        [ "touch example", "rm example" ],
        [ "touch example2", "rm example2" ],
    ]

Returns a list of tuples where:
    [
        ([ "touch example", "rm example" ], [ (stdout, stderr), (stdout, stderr) ],
        ...
    ]

Author: Evan K. Friis, UW Madison
'''


import shlex
import subprocess
import threading
from Queue import Queue

def run_task(task):
    '''
    Run a single task, by running each command in [task]
    '''
    outputs = []
    for subtask in task:
        command = shlex.split(subtask)
        print "Running: %s" % subtask
        proc = subprocess.Popen(command, stdout=subprocess.PIPE,
                               stderr = subprocess.PIPE)
        stdout, stderr = proc.communicate()
        outputs.append( (stdout, stderr) )
    return (task, outputs)

def run_task_from_queue(input, output):
    '''
    Consume from queue and process tasks
    '''
    while True:
        task = input.get()
        result = run_task(task)
        output.put(result)
        input.task_done()

def parallelize(tasks, ntasks):
    tasks_to_run = Queue()
    for task in tasks:
        tasks_to_run.put(tuple(task))

    results = Queue()
    workers = []
    for i in range(ntasks):
        worker = threading.Thread(target = run_task_from_queue,
                                  args = (tasks_to_run, results))
        worker.daemon = True
        worker.start()
        workers.append(worker)
    ## Wait for all to finish
    try:
        tasks_to_run.join()
    except KeyboardInterrupt:
        log.error("Caught Ctrl-C, quitting")

    outputs = []
    while not results.empty():
        outputs.append(results.get())

    print "Finished parallelize() call"
    ## Kill workers
    return outputs
