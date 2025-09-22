import pygame
from pygame.math import Vector2
from physicObject import PhysicObject
from math import sqrt
from animator import Animator

class Enemy:
    def __init__(self, speed, damage):
        self.direction = Vector2(0)
        self.speed = speed
        self.damage = damage