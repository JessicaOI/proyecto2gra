from mathlib import *
from materials   import *


class Sphere(object):
  def __init__(self, center, radius, material):
    self.center = center
    self.radius = radius
    self.material = material

  def ray_intersect(self, orig, direction):
    L = sub(self.center, orig)
    tca = dot(L, direction)
    l = length(L)
    d2 = l**2 - tca**2
    if d2 > self.radius**2:
      return None
    thc = (self.radius**2 - d2)**1/2
    t0 = tca - thc
    t1 = tca + thc
    if t0 < 0:
      t0 = t1
    if t0 < 0:
      return None

    hit = sum(orig, mul(direction, t0))
    normal = norm(sub(hit, self.center))

    return Intersect(
      distance=t0,
      point=hit,
      normal=normal
    )


class Plane(object):
  def __init__(self, position, normal, material):
    self.position = position
    self.normal = norm(normal)
    self.material = material

  def ray_intersect(self, orig, dir):
    denom = dot(dir, self.normal)

    if abs(denom) > 0.0001:
      t = dot(self.normal, sub(self.position, orig)) / denom
      if t > 0:
        hit = sum(orig, mul(dir, t))

        return Intersect(distance = t,
                         point = hit,
                         normal = self.normal)

    return None



class Cube(object):
  def __init__(self, position, size, material):
    self.position = position
    self.size = size
    self.material = material
    self.planes = []

    halfSize = size / 2
    #Se crean las 6 paredes del cubo con planos
    self.planes.append( Plane( sum(position, V3(halfSize,0,0)), V3(1,0,0), material))
    self.planes.append( Plane( sum(position, V3(-halfSize,0,0)), V3(-1,0,0), material))

    self.planes.append( Plane( sum(position, V3(0,halfSize,0)), V3(0,1,0), material))
    self.planes.append( Plane( sum(position, V3(0,-halfSize,0)), V3(0,-1,0), material))

    self.planes.append( Plane( sum(position, V3(0,0,halfSize)), V3(0,0,1), material))
    self.planes.append( Plane( sum(position, V3(0,0,-halfSize)), V3(0,0,-1), material))


  def ray_intersect(self, orig, direction):

    epsilon = 0.001
    
    #bbox
    minLimits = [0,0,0]
    maxLimits = [0,0,0]

    for i in range(3):
      minLimits[i] = self.position[i] - (epsilon + self.size / 2)
      maxLimits[i] = self.position[i] + (epsilon + self.size / 2)



    t = float('inf')
    intersect = None

    for plane in self.planes:
      intersectPlane = plane.ray_intersect(orig, direction)

      if intersectPlane is not None:
        if intersectPlane.point[0] >= minLimits[0] and intersectPlane.point[0] <= maxLimits[0]:
          if intersectPlane.point[1] >= minLimits[1] and intersectPlane.point[1] <= maxLimits[1]:
            if intersectPlane.point[2] >= minLimits[2] and intersectPlane.point[2] <= maxLimits[2]:
              if intersectPlane.distance < t:
                t = intersectPlane.distance
                intersect = intersectPlane

    if intersect is None:
      return None

    return Intersect(distance = intersect.distance,
                     point = intersect.point,
                     normal = intersect.normal)


class Pyramid(object):
  def __init__(self, arrayV3, material):
    self.arrayV3 = arrayV3
    self.material = material

  def side(self, v0, v1, v2, origin, direction):
    v0v1 = sub(v1, v0)
    v0v2 = sub(v2, v0)

    N = mul(cross(v0v1, v0v2),1)

    raydirection = dot(N, direction)

    if abs(raydirection) < 0.0001:
        return None
    
    d = dot(N, v0)
    t = (dot(N, origin) + d)/raydirection
    
    
    
    if t < 0:
      return None

    P = sum(origin, mul(direction, t))
    U, V, W = barycentric(v0, v1, v2, P)

    if U<0 or V<0 or W<0:
      return None
    else: 
      return Intersect(distance = d,
                      point = P,
                      normal = norm(N))

  def ray_intersect(self, origin, direction):
    v0, v1, v2, v3 = self.arrayV3
    planes = [
    self.side(v0, v3, v2, origin, direction),
    self.side(v0, v1, v2, origin, direction),
    self.side(v1, v3, v2, origin, direction),
    self.side(v0, v1, v3, origin, direction)
    ]


    t = float('inf')
    intersect = None

    for plane in planes:
        if plane is not None:
            if plane.distance < t:
                t = plane.distance
                intersect = plane

    if intersect is None:
        return None

    return Intersect(distance = intersect.distance,
                     point = intersect.point,
                     normal = intersect.normal)
