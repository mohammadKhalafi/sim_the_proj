import numpy as np
from numpy import random

T = 40
x = 5 #arrival rate
y = 10 #serivce rate
num_pros = 1

queue_limit = 2

# create betweens
sum_of_betweens = 0
betweens = np.array([])

while sum_of_betweens < T:
    betweens_ = random.exponential(scale=x, size=10)
    betweens = np.append(betweens, betweens_)
    sum_of_betweens += sum(betweens_)


# concat redundant betweens
split_point = 0
sum_of_betweens = 0
for between in betweens:
    split_point += 1

    sum_of_betweens += between
    if sum_of_betweens > T:
        break
betweens = betweens[:split_point-1]


# create arrival times
arrival_times = [0]
for between in betweens:
    arrival_times.append(between + arrival_times[len(arrival_times)-1])

# create n
n = len(arrival_times)

# create service times
service_times = random.exponential(scale=y, size=n)

#create priorities
def get_priority():
    r = random.random()
    if r < 0.2:
        return 0
    if r < 0.5:
        return 1
        
    return 2

task_priorities = [get_priority() for _ in range(n)]

# mock

'''
n = 5
arrival_times = [0,0.1,0.2,1,2]
service_times = [2,2,2,2,2]
task_priorities = [0,1,0,0,0]
'''

# create start and end of the service times for fifo
end_service_times = []
start_service_times = []
end_service_times_for_entered_tasks = []

for i in range(n):
    number_of_tasks_in_queue_after_task_arrival = \
        len(list(filter(lambda k : start_service_times[k] != 'err' and \
            start_service_times[k] > arrival_times[i], range(0, i))))
    
    if number_of_tasks_in_queue_after_task_arrival == queue_limit:
        start_service_times.append('err')
        end_service_times.append('err')
        continue

    l = len(end_service_times_for_entered_tasks)
    past_ends = [0 for _ in range(num_pros-l)] + \
        end_service_times_for_entered_tasks[max(0, l-num_pros) : l]
    assert len(past_ends) == num_pros

    start_service_times.append(max(arrival_times[i], min(past_ends)))

    end_service_time = start_service_times[i] + service_times[i]
    end_service_times.append(end_service_time)
    end_service_times_for_entered_tasks.append(end_service_time)


'''
print('arrival_times', arrival_times)
print('start_service_times', start_service_times)
print('service_times', service_times)
print('end_service_times', end_service_times)
'''

# create start and end of the service times for priority queue

start_service_times = [-1 for _ in range(n)]
end_service_times = [-1 for _ in range(n)]

service_started_tasks_in_order = []
pending_tasks_in_order = list(range(n))

task_states = ['pending' for _ in range(n)]

counter_for_check_canceled_tasks = 0

while len(pending_tasks_in_order) != 0:
    lst_len = len(service_started_tasks_in_order)
    service_ends_to_check = [0 for _ in range(num_pros - lst_len)] +\
        [end_service_times[i] for i in service_started_tasks_in_order\
            [max(0, lst_len - num_pros) : lst_len]]

    time_to_fetch_task = min(service_ends_to_check)

    pending_tasks_could_fetch = []
    for pending_task in pending_tasks_in_order:
        if arrival_times[pending_task] <= time_to_fetch_task:
            pending_tasks_could_fetch.append(pending_task)
        else:
            break
    
    # detect canceled tasks
    for pending_task in pending_tasks_could_fetch:
        if pending_task <= counter_for_check_canceled_tasks:
            continue

        if arrival_times[pending_task] == time_to_fetch_task:
            continue

        in_queue_tasks_before_pending_task = \
            sum([task_state == 'pending' for task_state in task_states[0:pending_task]])
        assert(in_queue_tasks_before_pending_task <= queue_limit)

        if in_queue_tasks_before_pending_task == queue_limit:
            task_states[pending_task] = 'canceled'
            pending_tasks_in_order.remove(pending_task)
    
    counter_for_check_canceled_tasks = \
        pending_tasks_could_fetch[len(pending_tasks_could_fetch)-1]

    pending_tasks_could_fetch = list(filter(lambda t : task_states[t] != 'canceled',\
        pending_tasks_could_fetch))


    if len(pending_tasks_could_fetch) == 0:
        if len(pending_tasks_in_order) == 0:
            break

        task_to_fetch = pending_tasks_in_order[0]
        
        start_service_times[task_to_fetch] = arrival_times[task_to_fetch]

    else:
        priorities_of_pending_tasks_could_fetch = [task_priorities[i] for i in pending_tasks_could_fetch]
        task_to_fetch_index = priorities_of_pending_tasks_could_fetch.index\
            (min(set(priorities_of_pending_tasks_could_fetch)))
        task_to_fetch = pending_tasks_could_fetch[task_to_fetch_index]

        start_service_times[task_to_fetch] = time_to_fetch_task

    #common works for task to fetch
    task_states[task_to_fetch] = 'started'
    end_service_times[task_to_fetch] = \
        start_service_times[task_to_fetch] + service_times[task_to_fetch]

    service_started_tasks_in_order.append(task_to_fetch)
    pending_tasks_in_order.remove(task_to_fetch)


print(arrival_times)
print(service_times)
print(task_priorities)
print(start_service_times)
print(end_service_times)
print(task_states)