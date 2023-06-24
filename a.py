import numpy as np
from numpy import random

T = 20
x = 5
y = 8

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


