import random

#neighbor function -> generates job sequence
def generateJobSeq():
    pass

#decreases time per simulated annealing iteration
def timeSchedule():
    pass


#creates a job schedule
def allocate_ops_to_machines(job_sequence, proc_times, M):
    schedule = [[] for _ in range(M)]

    #to understand where the operations are mapped -> helpful to find the previous operation of a job
    mapping = [[] for _ in range(M)]
    time_unit = None

    #for iterating through jobs in a round robin fashion
    queue = job_sequence.copy()

    #indexing
    i = 0
    unsched_index = 0
    size = sum(len(ops) for ops in proc_times)

    #to ensure we go through each & every op
    while i < size:
        #obtain job from queue and current unscheduled operation
        job_index = queue.pop(0)
        op_index = unsched_index

        #obtain machine mapping index & current operation processing time
        m = op_index % M
        print(m)
        proc = proc_times[job_index][op_index]

        #if machine empty, start time = 0
        if len(schedule[m]) == 0:
            time_unit = 0
        else:
            #get start time by getting the previous end time of last op in machine m
            time_unit = schedule[m][len(schedule[m]) - 1][1]

            list_index = None
            time_index = None
            
            #find the previous operation of current job
            #so that we can ensure no operations of same job are running concurrently
            for ind, li in enumerate(mapping):
                if (job_index, op_index - 1) in li:
                    #get list and operation start & end time indexes for accessing previous operation
                    time_index = li.index((job_index, op_index - 1))
                    list_index = ind
                    break

            #if current op start time will conflict with previous operation processing time, adjust start time of current op
            if time_index != None and time_unit < schedule[list_index][time_index][1]:
                difference = schedule[list_index][time_index][1] - time_unit
                time_unit = difference + time_unit

        #get start & end times of current operation
        start_time = time_unit
        end_time = time_unit + proc

        #add operation to schedule & mapping array
        schedule[m].append((start_time, end_time))
        mapping[m].append((job_index, op_index))

        #add back job to the end of the queue
        queue.append(job_index)

        i += 1

        #for keeping track of which operation (holistically) we're on
        #if we scheduled all operations at an index, increment it
        if i % len(job_sequence) == 0:
            unsched_index += 1

    return schedule


def compMakespan(schedule):
        makespan = 0
        for machine in schedule:
            if machine:
                lastEnd = machine[-1][1]

                if lastEnd > makespan:
                    makespan = lastEnd
                
        return makespan
        


#for simulated annealing algorithm
def simAnneal():
    pass
