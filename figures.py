import numpy as np

WHITE = (1,1,1)
BLACK = (0,0,0)

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2


class Intersect(object):
    def __init__(self, distance, point, normal, sceneObj):
        self.distance = distance
        self.point = point
        self.normal = normal
        self.sceneObj = sceneObj

class Material(object):
    def __init__(self, diffuse = WHITE, spec = 1.0, ior = 1.0,texture = None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.ior = ior
        self.texture = texture
        self.matType = matType
        


class Sphere(object):
    def __init__(self, center, radius, material):
        self.center = center
        self.radius = radius
        self.material = material

    def ray_intersect(self, orig, dir):
        L = np.subtract(self.center, orig)
        tca = np.dot(L, dir)
        d = (np.linalg.norm(L) ** 2 - tca ** 2) ** 0.5

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
        P = np.add(orig, t0 * np.array(dir))
        normal = np.subtract(P, self.center)
        normal = normal / np.linalg.norm(normal)

        return Intersect(distance = t0,
                        point = P,
                        normal = normal,
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

        contact = np.subtract(intersect.point, self.plane.position)
        contact = np.linalg.norm(contact)

        if contact > self.radius:
            return None

        return Intersect(distance = intersect.distance,
                        point = intersect.point,
                        normal = self.plane.normal,
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
        contact = np.linalg.norm(contact)

        if contact > self.radius or contact < self.radius2:
            return None

        return Intersect(distance = intersect.distance,
                        point = intersect.point,
                        normal = self.plane.normal,
                        sceneObj = self)

class Plane(object):
    def __init__(self, position, normal, material) -> None:
        self.position = position
        self.normal = normal / np.linalg.norm(normal)
        self.material = material
        
    def ray_intersect(self, orig, dir):
        denom = np.dot(dir, self.normal)
        
        if abs(denom) > 0.0001:
            num = np.dot(np.subtract(self.position, orig), self.normal)
            
            t = num / denom
            
            if t > 0:
                P = np.add(orig, t*np.array(dir))
                
                return Intersect(distance = t,
                        point = P,
                        normal = self.normal,
                        sceneObj = self)

#Contents Möller-Trumbore algorithm  
#obtenido de: https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-rendering-a-triangle/moller-trumbore-ray-triangle-intersection             
class Triangle(object):
    def __init__(self, v0, v1, v2, material) -> None:
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.material = material
        
    def ray_intersect(self, orig, dir):
        
        epsilon = 0.001
        
        v0v1 = np.subtract(self.v1,self.v0)
        v0v2 = np.subtract(self.v2, self.v0)
        
        pvec = np.cross(dir, v0v2)
        det = np.dot(v0v1, pvec)
        
        if det < epsilon: return None
        if abs(det) < epsilon: return None
        
        invDet = 1/det
        
        tvec = np.subtract(orig,self.v0)
        u = np.dot(tvec, pvec)*invDet
        
        if (u<0 or u>1): return None
        
        qvec = np.cross(tvec, v0v1)
        v = np.dot(dir, qvec)*invDet
        
        if (v<0 or u+v >1): return None
        
        t = np.dot(v0v2, qvec)*invDet
        
        if t > 0:
            P = np.add(orig, t*np.array(dir))
            normal = np.cross(v0v1, v0v2)
            normal = normal/np.linalg.norm(normal)
            return Intersect(distance = t,
                            point = P,
                            normal = normal,
                            sceneObj = self)    
            
        return None
        
    
class AABB(object):
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
                    
        