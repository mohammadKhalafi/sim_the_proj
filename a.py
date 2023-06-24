import numpy as np
from numpy import random

T = 40
x = 5
y = 10
num_pros = 3

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


# create service times
service_times = random.exponential(scale=y, size=len(arrival_times))


# create start and end of the service times
n = len(service_times)

end_service_times = []
start_service_times = []

for i in range(n):
    past_ends = [0 for _ in range(num_pros-i)] + end_service_times[max(0, i-num_pros) : i]
    assert len(past_ends) == num_pros
    start_service_times.append(max(arrival_times[i], min(past_ends)))
    end_service_times.append(start_service_times[i] + service_times[i])


print(arrival_times)
print(start_service_times)
print(service_times)
print(end_service_times)