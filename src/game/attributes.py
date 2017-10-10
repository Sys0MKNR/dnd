#!/usr/bin/env python3.5

class Attributes(object):
    def __init__(self, **stats):
        self.strength = 0
        self.agility = 0
        self.speed = 0
        self.defense = 0
        self.__dict__.update(stats)