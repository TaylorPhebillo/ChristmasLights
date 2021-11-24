#!/usr/bin/python3
momentum = 3
drawdown = 0.85
import board
import copy
import math
from random import random as rand
from random import randint
import neopixel
from time import sleep
i = 0

locations = [821, 150,
686, 161 ,
774, 150 ,
861, 162 ,
922, 164 ,
999, 240 ,
938, 288 ,
962, 377 ,
888, 371 ,
854, 376 ,
768, 367 ,
749, 368 ,
652, 322 ,
606, 408 ,
529, 305 ,
547, 346 ,
570, 352 ,
665, 282 ,
717, 268 ,
779, 379 ,
834, 293 ,
895, 409 ,
956, 350 ,
998, 400 ,
972, 460 ,
951, 499 ,
850, 517 ,
762, 419 ,
728, 424 ,
695, 437 ,
621, 532 ,
543, 525 ,
465, 427 ,
585, 490 ,
648, 442 ,
697, 472 ,
732, 526 ,
800, 572 ,
854, 628 ,
787, 679 ,
793, 714 ,
753, 622 ,
697, 651 ,
695, 567 ,
589, 583 ,
549, 484 ,
503, 453 ,
459, 418 ,
387, 481 ,
337, 365]

x = locations[0::2]
y = locations[1::2]
x = [(p-min(x))/(max(x)-min(x)) for p in x]
y = [(p-min(y))/(max(y)-min(y)) for p in y]
zero = [(0,0,0)] * len(x)
pixels = neopixel.NeoPixel(board.D18, len(x), brightness=0.1)
pixels.fill((0,0,0))
pixels.show()
#lights = list(zip(range(len(locations)), x, y, zero))
#
#transitions = [
#        lambda l:l[1]*x_r + l[2]*y_r,
#        lambda l:abs(l[1]-x_r) + abs(l[2]-y_r),
#        lambda l:pow(l[1]-x_r,2) + pow(l[2]-y_r,2),
#        lambda l:pow(l[1]-x_r,10) + pow(l[2]-y_r,10)
#        ]
#
#def transition(lights):
#    color = [randint(0,255), randint(0,255), randint(0,255)]
#    lights_s = list(sorted(copy.copy(lights), key = transitions[randint(0,len(transitions)-1)], reverse=True if rand() < 0.5 else False))
#    for i in range(len(lights_s)):
##        print("Drawing from "+str(color))
#        yield (lights_s[i][0], color, 12-int(math.log2(randint(1,4096))))
#
#def ongoing_transitions(lights):
#    trans = [transition(list(lights)) for _ in range(2)]
#    i = 0
#    while True:
#        if rand() < (drawdown/len(lights)) or len(trans) == 0:
#            trans.append(transition(list(lights)))
#            print(f"Now have {len(trans)} pattens ongoing")
#        try:
##            print(f"transition {i}/{len(trans)}")
#            yield next(trans[i])
#        except StopIteration:
#            trans.pop(i)
#            print(f"Now have {len(trans)} pattens ongoing")
#        i += 1
#        if i >= len(trans):
#            i = 0
#
#while True:
#    x_r = rand() - 0.5
#    y_r = rand() - 0.5
##    lights = sorted(lights, key = transitions[randint(0,len(transitions)-1)])
#    #print(f"Resorting by {x_r} {y_r}, ended with {lights}")
#    ong = ongoing_transitions(lights)
#    count = 0
#    for i, color, strength in ong:
#            l_no = lights[i][0]
#            current_val = [(strength * color[j] + momentum * lights[i][3][j])//(strength+momentum) for j in range(3)]
#            lights[i] = (lights[i][0], lights[i][1], lights[i][2],tuple(current_val))
#            pixels[l_no] = tuple(current_val)
##            if count % 100 == 0:
#            print(f"Writing light{l_no}")
#            if count % 1000 == 0:
#                pixels.fill((0,0,0))
#            sleep(0.015)
#            count += 1
#    #        pixels[l_no] = (0,0,0)
#
