#!/usr/bin/env python3
# coding: utf-8

from ast import arg
from game import play
import sys

def main(args):
    if len(args) == 1:
        play()
    if len(args) == 2:
        play(output=args[1])
    if len(args) == 3:
        play(output=args[1], frames=int(args[2]))
    if len(args) == 4:
        play(output=args[1], frames=int(args[2]), configuration=int(args[3]))
    if len(args) == 5:
        play(output=args[1], frames=int(args[2]), configuration=int(args[3]), width=int(args[4]))
    if len(args) == 6:
        play(output=args[1], frames=int(args[2]), configuration=int(args[3]), width=int(args[4]), p=float(args[5]))
   
if __name__ == '__main__':
    main(sys.argv)
