#!/usr/bin/python3
import random
import board
import copy
import math
from random import random as rand
from random import randint
import neopixel
from time import sleep
i = 0

def clamp(x):
  return max(min(x, 1),0)
bias = 0.3

def random_walk(min_v, max_v, transition_speed = 0.1):
  p = random.random()
  while True:
    direction = 1 if (random.random() < 0.5 + bias * (0.5 - p)) else -1
    p = clamp(p+direction/10)
    yield (p * (max_v-min_v)) + min_v

drawdown = random_walk(.7,.95)
speed = random_walk(0,0.1, 0.01)
color_bias = [random_walk(0,255) for _ in range(3)] 
light_positions = [
[379, 155],
[365, 155],
[341, 106],
[325, 164],
[305, 108],
[263, 131],
[248, 172],
[295, 158],
[289, 183],
[241, 157],
[232, 209],
[204, 219],
[143, 197],
[188, 243],
[228, 211],
[230, 250],
[282, 251],
[300, 263],
[319, 308],
[313, 332],
[309, 366],
[278, 383],
[238, 347],
[280, 310],
[256, 310],
[246, 281],
[200, 256],
[182, 271],
[161, 298],
[211, 267],
[225, 312],
[226, 362],
[183, 328],
[165, 383],
[157, 372],
[157, 407],
[102, 378],
[167, 374],
[122, 393],
[99, 387],
[43, 380],
[76, 424],
[119, 418],
[140, 374],
[134, 446],
[166, 460],
[140, 477],
[179, 445],
[189, 421],
[268, 447],
[293, 454],
[255, 484],
[237, 498],
[211, 499],
[255, 503],
[285, 496],
[317, 460],
[340, 476],
[364, 474],
[401, 459],
[411, 444],
[447, 446],
[457, 430],
[474, 420],
[478, 393],
[490, 370],
[488, 357],
[471, 324],
[454, 288],
[423, 277],
[387, 284],
[383, 235],
[353, 215],
[330, 215],
[288, 215],
[336, 230],
[351, 223],
[379, 256],
[375, 276],
[406, 301],
[371, 324],
[404, 362],
[400, 391],
[373, 404],
[356, 450],
[338, 456],
[321, 457],
[298, 488],
[268, 511],
[220, 475],
[213, 524],
[171, 533],
[128, 528],
[188, 532],
[193, 557],
[221, 535],
[261, 550],
[275, 574],
[278, 580],
[278, 577]]

x = list(zip(*light_positions))[0]
y = list(zip(*light_positions))[1]
x = [(p-min(x))/(max(x)-min(x)) for p in x]
y = [(p-min(y))/(max(y)-min(y)) for p in y]
zero = [(0,0,0)] * len(x)
pixels = neopixel.NeoPixel(board.D18, len(x), brightness=.3)
pixels.fill((0,0,0))
pixels.show()
lights = list(zip(range(len(x)), x, y, zero))

transitions = [
        lambda l:l[1]*x_r + l[2]*y_r,
        lambda l:pow(l[1]-x_r,2) + pow(l[2]-y_r,2),
        ]

def transition(lights):
    color = [randint(0,255), randint(0,255), randint(0,255)]
    bias_amount = min(rand(), rand())
    color = [int((1-bias_amount) * color[i] + bias_amount * next(color_bias[i])) for i in range(3)]
    lights_s = list(sorted(copy.copy(lights), key = transitions[randint(0,len(transitions)-1)], reverse=True if rand() < 0.5 else False))
    for i in range(len(lights_s)):
        yield (lights_s[i][0], color)

def ongoing_transitions(lights):
    trans = [transition(list(lights)) for _ in range(2)]
    i = 0
    while True:
        if rand() < (next(drawdown)/len(lights)) or len(trans) == 0:
            trans.append(transition(list(lights)))
        try:
            yield (next(trans[i]), len(trans))
        except StopIteration:
            trans.pop(i)
        i += 1
        if i >= len(trans):
            i = 0

while True:
    x_r = rand() - 0.5
    y_r = rand() - 0.5
    ong = ongoing_transitions(lights)
    for (i, color), num_trans in ong:
            l_no = lights[i][0]
            lights[i] = (lights[i][0], lights[i][1], lights[i][2],tuple(color))
            pixels[l_no] = color
            pixels.show()
            sleep(next(speed)/num_trans)

