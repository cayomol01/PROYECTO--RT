import numpy as np
from matlib import matlib

WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

lib = matlib()


class Intersect(object):
    def __init__(self, distance, point, normal, texcoords, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObj = sceneObj
        self.texcoords = texcoords

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0,texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType
        


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = list(center)
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        dir = list(dir)
        orig = list(orig)
        L = lib.Subtract(self.center,orig)
        tca = lib.dot(L,dir)
        d = (lib.norm(L) ** 2 - tca ** 2) ** 0.5

        if d > self.radius:
            return None

        thc = (self.radius ** 2 - d ** 2) ** 0.5

        t0 = tca - thc
        t1 = tca + thc

        if t0 < 0:
            t0 = t1
        if t0 < 0:
            return None
        
        # P = O + t0 * D
        P = lib.Add(orig, lib.ScalarMul(dir, t0))
        normal = lib.Subtract(P, self.center)
        normal = lib.scalarDiv(normal, lib.norm(normal))
        
        u = 1 - ((np.arctan2(normal[2], normal[0]) / (2 * np.pi)) + 0.5)
        v = np.arccos(-normal[1]) / np.pi

        uvs = (u,v)

        return Intersect(distance = t0,
                        point = P,
                        normal = normal,
                        texcoords=uvs,
                        sceneObj = self)

class Disk(object):
    def __init__(self, position, radius, normal,  material):
        self.plane = Plane(position, normal, material)
        self.material = material
        self.radius = radius

    def ray_intersect(self, orig, dir):

        intersect = self.plane.ray_intersect(orig, dir)

        if intersect is None:
            return None
        
        contact = lib.Subtract(intersect.point, self.plane.position)
        contact = lib.norm(contact)

        if contact > self.radius:
            return None

        return Intersect(distance = intersect.distance,
                        point = intersect.point,
                        normal = self.plane.normal,
                        texcoords=None,
                        sceneObj = self)

class Disk2(object):
    def __init__(self, position, radius, radius2,  normal,  material):
        self.plane = Plane(position, normal, material)
        self.material = material
        self.radius = radius
        self.radius2 = radius2

    def ray_intersect(self, orig, dir):

        intersect = self.plane.ray_intersect(orig, dir)

        if intersect is None:
            return None

        contact = np.subtract(intersect.point, self.plane.position)
        contact = lib.norm(contact)

        if contact > self.radius or contact < self.radius2:
            return None

        return Intersect(distance = intersect.distance,
                        point = intersect.point,
                        normal = self.plane.normal,
                        texcoords= None,
                        sceneObj = self)

class Plane(object):
    def __init__(self, position, normal, material) -> None:
        normal = list(normal)
        self.position = list(position)
        self.normal =lib.scalarDiv(normal, lib.norm(list(normal)))
        self.material = material
        
    
    def ray_intersect(self, orig, dir):
        orig = list(orig)
        dir = list(dir)
        denom = lib.dot(dir,self.normal)
        
        if abs(denom) > 0.0001:
            num = lib.dot(lib.Subtract(self.position, orig), self.normal)

            
            t = num / denom
            
            if t > 0:
                P = lib.Add(orig, lib.ScalarMul(dir,t))
                return Intersect(distance = t,
                        point = P,
                        normal = self.normal,
                        texcoords= None,
                        sceneObj = self)
        return None
#Contents Möller-Trumbore algorithm  
#obtenido de: https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection             
class Triangle(object):
    def __init__(self, v0, v1, v2, material) -> None:
        self.v0 = list(v0)
        self.v1 = list(v1)
        self.v2 = list(v2)
        self.material = material
        
    def ray_intersect(self, orig, dir):
        orig = list(orig)
        dir = list(dir)
        epsilon = 0.001
        
        v0v1 = lib.Subtract(self.v1,self.v0)
        v0v2 = lib.Subtract(self.v2, self.v0)
        
        pvec = lib.cross(dir, v0v2)
        det = lib.dot(v0v1, pvec)
        
        if det < epsilon: return None
        if abs(det) < epsilon: return None
        
        invDet = 1/det
        
        tvec = np.subtract(orig,self.v0)
        u = lib.dot(tvec, pvec)*invDet
        
        if (u<0 or u>1): return None
        
        qvec = lib.cross(tvec, v0v1)
        v = lib.dot(dir, qvec)*invDet
        
        if (v<0 or u+v >1): return None
        
        t = lib.dot(v0v2, qvec)*invDet
        
        if t > 0:
            P = lib.Add(orig, lib.ScalarMul(dir, t))
            normal = lib.cross(v0v1, v0v2)
            normal = lib.scalarDiv(normal, lib.norm(normal))
            return Intersect(distance = t,
                            point = P,
                            texcoords = (u,v),
                            normal = normal,
                            sceneObj = self)    
            
        return None
        
    
class AABB(object):
    # Axis Aligned Bounding Box

    def __init__(self, position, size, material):
        self.position = list(position)
        self.size = list(size)
        self.material = material

        self.planes = []

        halfSizes = [0,0,0]

        halfSizes[0] = size[0] / 2
        halfSizes[1] = size[1] / 2
        halfSizes[2] = size[2] / 2

        # Sides
        self.planes.append( Plane( lib.Add(position, list(halfSizes[0],0,0)), (1,0,0), material ))
        self.planes.append( Plane( lib.Add(position, list(-halfSizes[0],0,0)), (-1,0,0), material ))

        # Up and Down
        self.planes.append( Plane( lib.Add(position, list(0,halfSizes[1],0)), (0,1,0), material ))
        self.planes.append( Plane( lib.Add(position, list(0,-halfSizes[1],0)), (0,-1,0), material ))

        # Front and back
        self.planes.append( Plane( lib.Add(position, list(0,0,halfSizes[2])), (0,0,1), material ))
        self.planes.append( Plane( lib.Add(position, list(0,0,-halfSizes[2])), (0,0,-1), material ))

        #Bounds
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]

        epsilon = 0.001

        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.boundsMax[i] = self.position[i] + (epsilon + halfSizes[i])


    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')

        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:

                planePoint = planeInter.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:

                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter

                                # Tex Coords

                                u, v = 0, 0

                                # Las uvs de las caras de los lados
                                if abs(plane.normal[0]) > 0:
                                    # Mapear uvs para el eje x, usando las coordenadas de Y y Z
                                    u = (planeInter.point[1] - self.boundsMin[1]) / self.size[1]
                                    v = (planeInter.point[2] - self.boundsMin[2]) / self.size[2]

                                elif abs(plane.normal[1] > 0):
                                    # Mapear uvs para el eje y, usando las coordenadas de X y Z
                                    u = (planeInter.point[0] - self.boundsMin[0]) / self.size[0]
                                    v = (planeInter.point[2] - self.boundsMin[2]) / self.size[2]

                                elif abs(plane.normal[2] > 0):
                                    # Mapear uvs para el eje z, usando las coordenadas de X y Y
                                    u = (planeInter.point[0] - self.boundsMin[0]) / self.size[0]
                                    v = (planeInter.point[1] - self.boundsMin[1]) / self.size[1]


        if intersect is None:
            return None

        return Intersect(distance = t,
                        point = intersect.point,
                        normal = intersect.normal,
                        texcoords = (u,v),
                        sceneObj = self)
        
class Prueba(object):
    def __init__(self,position, size, material) -> None:
        self.position = position
        self.size = size
        self.material = material
        self.planes = []
        
        halfSizes = [0,0,0]
        
        halfSizes[0] = size[0]/2
        halfSizes[1] = size[1]/2
        halfSizes[2] = size[2]/2
        
        #position: 4,4,8 plano ;
        #position : 2,2,-10
        #sumando : 2,2,2
        #np.add : 4,4,8
        
        #sides
        self.planes.append( Plane(np.add(position, (halfSizes[0], 0,0)), (1,0,0), material))
        self.planes.append( Plane(np.add(position, (-halfSizes[0], 0,0)), (-1,0,0), material))
        
        #up and down
        self.planes.append( Plane(np.add(position, (0, halfSizes[1], 0)), (0,1,0), material))
        self.planes.append( Plane(np.add(position, (0, -halfSizes[1], 0)), (0,-1,0), material))
        
        #front and back
        self.planes.append( Plane(np.add(position, (0,0,halfSizes[2])), (0,0,1), material))
        self.planes.append( Plane(np.add(position, (0,0,halfSizes[2])), (0,0,-1), material))
        
        #inicializaron;
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
        
        #Donde pega el rayo; 
        epsilon = 0.001
        
        for i in range(3):
            self.boundsMin[i] = self.position[i] - (epsilon + halfSizes[i])
            self.boundsMax[i] = self.position[i] + (epsilon + halfSizes[i])
        
        
    def ray_intersect(self, orig, dir):
        intersect = None
        t = float('inf')
        
        for plane in self.planes:
            planeInter = plane.ray_intersect(orig, dir)
            if planeInter is not None:
                planePoint = planeInter.point
                
                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:
                            if planeInter.distance < t:
                                t = planeInter.distance
                                intersect = planeInter
        
        if intersect is None:
            return None
                        
                        
        return Intersect(distance = t,
                        point = intersect.point,
                        normal = intersect.normal,
                        sceneObj = self)
                    
        