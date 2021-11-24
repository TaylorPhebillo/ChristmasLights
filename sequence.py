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
num = 100
pixels = neopixel.NeoPixel(board.D18, num, brightness=0.1)
pixels.fill((0,0,0))
while True:
    for i in range(num):
            pixels[i] = (255,255,255)
#            if count % 100 == 0:
            print(f"Writing light{i}")
            pixels.show()
            sleep(1.0)
            pixels[i] = (0,0,0)

