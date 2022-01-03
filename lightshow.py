from itertools import product
from collections import Counter
from time import sleep
import heapq
import itertools
from datetime import datetime, timedelta
from random import random as rand
from random import randint
import random
import math
def clamp(x):
  return max(min(x, 1),0)
bias = 0.3


def random_walk(min_v, max_v, transition_speed = 0.1):
  p = random.random()
  while True:
    direction = 1 if (random.random() < 0.5 + bias * (0.5 - p)) else -1
    p = clamp(p+direction/10)
    yield (p * (max_v-min_v)) + min_v

transition_time_max = random_walk(0.3,0.5)
duration_const = 0.2
speed = random_walk(150, 230)
color_bias = [random_walk(0,255, 0.01) for _ in range(3)] 
skip_back_percent = 0.0
def time_between_transitions():
    delay = next(transition_time_max) / next(speed)
    return timedelta(seconds = delay)
transitions = [
  # Circle: sqrt(point-center)
  lambda point, center, speed: (-1, math.sqrt(sum([math.pow(point[i]-center[i],2) for i in range(len(point))]))/speed),
  lambda point, center, speed: (math.sqrt(sum([math.pow(point[i]-center[i],2) for i in range(len(point))]))/speed, -1),
  # Plane:
  lambda point, plane_rot, speed: (-1, sum(point[i]*plane_rot[i] for i in range(len(point)))/speed),
  # Rectangle:
  #lambda point, rect, speed, : (point[0]/(.01*speed) if min(rect)/2<=point[1]<=max(rect)/2 else -1, -1),
  #lambda point, rect, speed, : (point[1]/speed if (.5+min(rect)/2)<=point[0]<=(.5+max(rect)/2) else -1, -1)
]
def transition(lights, now):
    color = [randint(0,255), randint(0,255), randint(0,255)]
    bias_amount = min(rand(), rand())
    color = [int((1-bias_amount) * color[i] + bias_amount * next(color_bias[i])) for i in range(3)]

    trans_func = transitions[randint(0,len(transitions)-1)]
    rect = [rand(), rand()]
    trans_speed = pow(next(speed),2)
    duration = (.5+rand()) * next(speed) * duration_const

    trans = lambda p: trans_func(p, rect, trans_speed)
    times = [trans(p) for p in lights]
    skip_background = rand() < skip_back_percent
    c = Counter([max(t) for t in times])
    if skip_background:
        print(f"Skipping {set([max(t) for t in times if c[max(t)] >= 4])}")
        times = [t for t in times if c[max(t)] < 4]

    foreground_times, background_times = zip(*times)
    foreground_times_new = zip(foreground_times, range(len(lights)), itertools.repeat(1))
    foreground_end_times = zip(foreground_times, range(len(lights)), itertools.repeat(-1))
    foreground_times = foreground_times_new
#    foreground_times = [fg for fg in foreground_times if fg[0] != -1]
    foreground_times = [(now+timedelta(seconds=fg[0]), fg[1], fg[2], color) for fg in foreground_times if fg[0] != -1]
    foreground_end_times = [(now+timedelta(seconds=fg[0]+duration), fg[1], fg[2], color) for fg in foreground_end_times if fg[0] != -1]
    background_times = zip(background_times, range(len(lights)), itertools.repeat(0))
    background_times = [(now+timedelta(seconds=fg[0]), fg[1], fg[2], color) for fg in background_times if fg[0] != -1]
    return foreground_times + foreground_end_times + background_times

def controller(lights):
    schedule = [((datetime.now(),0), None)]
    light_colors = [[(0,0,0)] for _ in range(len(lights))]
    started = False
    while True:

#        if started and len(schedule) > 1:
            #sleep(max(0,(schedule[0][0][0] - datetime.now()).total_seconds()))
        next_event = heapq.heappop(schedule)
        scheduled_time = next_event[0][0]
        next_event = next_event[1]
        if next_event == None:#len(next_event[1]) < 2:
#            print("Scheduling new thing")
            heapq.heappush(schedule, ((scheduled_time+time_between_transitions(), rand()), (None)))
            new_transitions = transition(lights, scheduled_time)
            for t in new_transitions:

                heapq.heappush(schedule, ((t[0], rand()), (t[1],t[2],t[3])))
            continue
        light_ids = [next_event[0]]
        if next_event[1] == 0:
            for light_id in light_ids:
                light_colors[light_id][0] = next_event[2]
        elif next_event[1] == 1:
            for light_id in light_ids:
                light_colors[light_id].append(next_event[2])
        else:
            for light_id in light_ids:
                light_colors[light_id].pop()
        yield (light_ids, light_colors[next_event[0]][-1])
        started = True
