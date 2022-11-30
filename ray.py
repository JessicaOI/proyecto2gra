from mathlib import *
from materials import *
from figures import *
from map import *
from math import pi, tan

BLACK = color(0, 0, 0)
WHITE = color(255, 255, 255)
FONDO = color(50, 50, 200)
RED = color(255, 0, 0)
SKY = color(29, 142, 185)
MAX_RECURSION_DEPTH = 3


class Raytracer(object):
  def __init__(self, width, height):
    self.width = width
    self.height = height
    self.background_color = SKY
    self.light = None
    self.scene = []
    self.map = None
    self.clear()

  def clear(self):
    self.pixels = [
      [self.background_color for x in range(self.width)]
      for y in range(self.height)
    ]

  def write(self, filename):
    writebmp(filename, self.width, self.height, self.pixels)

  def display(self, filename='out.bmp'):
    self.render()
    self.write(filename)

  def point(self, x, y, c = None):
    try:
      self.pixels[y][x] = c or self.current_color
    except:
      pass

  def scene_intersect(self, orig, direction):
    zbuffer = float('inf')

    material = None
    intersect = None

    for obj in self.scene:
      hit = obj.ray_intersect(orig, direction)
      if hit is not None:
        if hit.distance < zbuffer:
          zbuffer = hit.distance
          material = obj.material
          intersect = hit

    return material, intersect

  def cast_ray(self, orig, direction, recursion = 0):
    material, intersect = self.scene_intersect(orig, direction)

    if material is None or recursion >= MAX_RECURSION_DEPTH: 
      if self.map:
        return self.map.get_color(direction)
      return self.background_color

    offset_normal = mul(intersect.normal, 1.1)

    if material.albedo[2] > 0:
      reverse_direction = mul(direction, -1)
      reflect_dir = reflect(reverse_direction, intersect.normal)
      reflect_orig = sub(intersect.point, offset_normal) if dot(reflect_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
      reflect_color = self.cast_ray(reflect_orig, reflect_dir, recursion + 1)
    else:
      reflect_color = color(0, 0, 0)

    if material.albedo[3] > 0:
      refract_dir = refract(direction, intersect.normal, material.refractive_index)
      refract_orig = sub(intersect.point, offset_normal) if dot(refract_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
      refract_color = self.cast_ray(refract_orig, refract_dir, recursion + 1)
    else:
      refract_color = color(0, 0, 0)

    light_dir = norm(sub(self.light.position, intersect.point))
    light_distance = length(sub(self.light.position, intersect.point))

    shadow_orig = sub(intersect.point, offset_normal) if dot(light_dir, intersect.normal) < 0 else sum(intersect.point, offset_normal)
    shadow_material, shadow_intersect = self.scene_intersect(shadow_orig, light_dir)
    shadow_intensity = 0

    if shadow_material and length(sub(shadow_intersect.point, shadow_orig)) < light_distance:
        shadow_intensity = 0.9

    intensity = self.light.intensity * max(0, dot(light_dir, intersect.normal)) * (1 - shadow_intensity)

    reflection = reflect(light_dir, intersect.normal)
    specular_intensity = self.light.intensity * (
      max(0, -dot(reflection, direction))**material.spec
    )

    diffuse = material.diffuse * intensity * material.albedo[0]
    specular = color(255, 255, 255) * specular_intensity * material.albedo[1]
    reflection = reflect_color * material.albedo[2]
    refraction = refract_color * material.albedo[3]

    return diffuse + specular + reflection + refraction

  def render(self):
    alfa = int(pi/2)
    for y in range(self.height):
      for x in range(self.width):
        i =  (2*(x + 0.5)/self.width - 1)*self.width/self.height*tan(alfa/2)
        j =  (2*(y + 0.5)/self.height - 1 )*tan(alfa/2)
        direction = norm(V3(i, j, -1))
        self.pixels[y][x] = self.cast_ray(V3(0,0,0), direction)

#1500,600
r = Raytracer(1000, 600)
r.map = Map('sunset.bmp')
r.light = Light(
  position=V3(1, 1, 15),
  intensity=1.5
)

r.scene = [
  #sol
  Sphere(V3(10, 5, -13 ), 1, orange),
  #piramide izquierda
        #lado izquierda atas, el vector de la punta s, la punta inferior derecha, inferior izquierda
  Pyramid([V3(-11, -1, -10), V3(-4, 1.6, -5), V3(-4, -1, -7.5), V3(-7.5, -1, -7.5)], brown),
  #piramide de enmedio
  Pyramid([V3(-7, -1, -10), V3(-1.5, 2.5, -5), V3(2, -1.1, -8), V3(-4, -1, -7.5)], brown),
  #piramide derecha
  Pyramid([V3(-2, -1, -10), V3(1.2, 1.5, -5), V3(5, -1, -8), V3(0.5, -1, -7.5)], brown),
  Cube(V3(0, -8, -15), 15, darkbrown),
  #oro
  Cube(V3(3, 0, -4), 0.6, yellow),
  #nube
  Sphere(V3(7, 5.5, -13 ), 0.6, white),
  Sphere(V3(4, 5.5, -13 ), 0.6, white),
  Sphere(V3(6, 6, -13 ), 0.6, white),
  Sphere(V3(5, 6, -13 ), 0.6, white),
  Sphere(V3(6, 4.5, -13 ), 0.6, white),
  Sphere(V3(5, 4.5, -13 ), 0.6, white),
]
r.display()