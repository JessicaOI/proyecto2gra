from mathlib import *
# from dataclasses import dataclass


class Light(object):
  def __init__(self, position=V3(0,0,0), intensity=1):
    self.position = position
    self.intensity = intensity

class Material(object):
  def __init__(self, diffuse=color(255, 255, 255), albedo=(1, 0, 0, 0), spec=0, refractive_index = 1):
    self.diffuse = diffuse
    self.albedo = albedo
    self.spec = spec
    self.refractive_index = refractive_index

class Intersect(object):
  def __init__(self, distance, point, normal):
    self.distance = distance
    self.point = point
    self.normal = normal

#materiales
brown = Material(diffuse=color(229,  183, 125), albedo=(0.6, 0.6, 0, 0, 0), spec=10)
darkbrown = Material(diffuse=color(71, 51, 10), albedo=(0.3,  0.3, 0, 0, 0), spec=10)
orange = Material(diffuse=color(255, 181, 44), albedo=(0.8,  0.8, 0, 0), spec=55, refractive_index=0.2)
yellow = Material(diffuse=color(255, 239, 81), albedo=(0.8,  0.8, 0, 0), spec=55, refractive_index=0.2)
white = Material(diffuse=color(255, 255, 255), albedo=(0.2,  0.2, 0, 0), spec=55)