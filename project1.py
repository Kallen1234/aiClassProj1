import random
import math

#neighbor function -> generates job sequence using swap method
def generateJobSeq(job_sequence):
    #generate list of allowed indexes to swap -> avoid duplicate indexes
    allowed = [ind for ind in range(len(job_sequence))]

    #generate two random indexes to swap
    ind1 = random.choice(allowed)
    allowed.pop(ind1)
    ind2 = random.choice(allowed)

    #perform job swap between ind1 & ind2
    job1 = job_sequence[ind1]
    job2 = job_sequence[ind2]

    job_sequence[ind1] = job2
    job_sequence[ind2] = job1

    return job_sequence

#decreases time per simulated annealing iteration using exponential cooling
def timeSchedule(temp, it):
    return temp * (0.85 ** it)


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
        #changed op_index to i so it will map to all machines even if J < M
        m = i % M
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


#finds makespan of current job schedule
def compMakespan(schedule):
        makespan = 0
        for machine in schedule:
            if machine:
                lastEnd = machine[-1][1]

                if lastEnd > makespan:
                    makespan = lastEnd
                
        return makespan
        


#for simulated annealing algorithm
def simAnneal(initial_sequence, proc_times, M):
    #lower temp -> find the current best solution over more iterations for exploration
    temp = 5
    iteration = 0

    #get initial makespan of job sequence
    current_sequence = initial_sequence
    current_schedule = allocate_ops_to_machines(current_sequence, proc_times, M)
    current_makespan = compMakespan(current_schedule)

    #simulated annealing -> iterate until time runs out
    while True:
        temp = timeSchedule(temp, iteration)

        if temp <= 0:
            return current_schedule, current_makespan

        #get neighbor/next states
        next_sequence = generateJobSeq(current_sequence)
        next_schedule = allocate_ops_to_machines(next_sequence, proc_times, M)
        next_makespan = compMakespan(next_schedule)

        #find change: improvement of current state or not
        makespan_change = next_makespan - current_makespan

        #if next state/schedule is better than current (smaller makespan), just accept it
        if makespan_change < 0:
            current_sequence = next_sequence
            current_schedule = next_schedule
            current_makespan = next_makespan
        else:
            #calculate acceptance probability. avoid integer division
            #needed to make the makespan change negative as small positive int / very small float = overflow error
            acceptance_prob = math.exp(float(-1 * makespan_change)/float(temp))
            #get random value for deciding whether to accept worse condition
            random_val = random.random()

            #accept worse condition if random value < probability
            #else, maintain current values
            if random_val < acceptance_prob:
                current_sequence = next_sequence
                current_schedule = next_schedule
                current_makespan = next_makespan

        iteration += 1
#this is the brute force for optimality 
def perms(jobs):
    if len(jobs) == 1:
        return [jobs]
    allO = []

    for i in range(len(jobs)):
        picked = jobs[i]

        remain = jobs[:i] + jobs[i+1:]
        for O in perms(remain):
            allO.append([picked] + O)
    return allO

#R4. Random large instance (more machines than ops/job)
def r4():
    random.seed(42)
    proc_timesR4 = [[random.randint(5,50) for _ in range(3)] for _ in range(50)]
    init_secR4 = list(range(50))

    random.shuffle(init_secR4)
    init_makespanR4 = compMakespan(allocate_ops_to_machines(init_secR4,proc_timesR4,5))
    saS4,saMakeS4 = simAnneal(init_secR4, proc_timesR4, 5)
    pctR4 = ((init_makespanR4 - saMakeS4) / init_makespanR4) * 100
    print("R4 init: ", init_makespanR4, "| R4 SA: ", saMakeS4, "| Improved ---> ", round(pctR4,1), "%" )

#these are almost identical 
#R5. Random large instance (more ops/job than machines)
def r5():
    random.seed(42)
    proc_timesR5 = [[random.randint(5,50) for _ in range(5)] for _ in range(50)]
    init_secR5 = list(range(50))

    random.shuffle(init_secR5)
    init_makespanR5 = compMakespan(allocate_ops_to_machines(init_secR5,proc_timesR5,3))
    saS5,saMakeS5 = simAnneal(init_secR5, proc_timesR5, 3)
    pctR5 = ((init_makespanR5 - saMakeS5) / init_makespanR5) * 100
    print("R5 init: ", init_makespanR5, "| R5 SA: ", saMakeS5, "| Improved ---> ", round(pctR5,1),"%")


#Data should be right i think 
proc_times = [
    [5, 2, 7, 4],  # the 6 jobs :)
    [3, 6, 2, 5],  
    [4, 5, 3, 6],  
    [2, 4, 6, 3],  
    [7, 3, 5, 2],  
    [6, 7, 4, 5],  
]
sequence = list(range(6))
M = 4
J = 6
N = 4
mOptimal = float('inf')
for perm in perms(list(range(6))):
    mksp = compMakespan(allocate_ops_to_machines(perm, proc_times, M))
    if mksp < mOptimal:
        mOptimal =mksp


schedule, makespan = simAnneal(sequence, proc_times, M)

print("Final makespan:", makespan, "| Optimal: ", mOptimal)
print()
print("Final schedule:", schedule, "\n")
r4()
r5()