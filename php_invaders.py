#/usr/bin/env python

#Import Modules
import pygame
from gameengine import GameEngine
from sys import argv

if not pygame.font:
    print('Warning, fonts disabled')


def main():

    modes = {
        'cheater': False
    }

    if len(argv) > 1:
        for arg in argv:
            if arg == '--cheater':
                modes['cheater'] = True

    ge = GameEngine(modes)

    while 1:
        if ge.handle_events() == -1:
            return
        ge.do_play()

if __name__ == '__main__': main()
