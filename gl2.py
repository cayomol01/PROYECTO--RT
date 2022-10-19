import struct
from collections import namedtuple
import numpy as np
from figures2 import *
from lights2 import *
from math import cos, sin, tan, pi
from obj import Obj
from matlib import matlib


STEPS = 1
OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2
MAX_RECURSION_DEPTH = 3
lib = matlib()

V2 = namedtuple('Point2', ['x', 'y'])
V3 = namedtuple('Point3', ['x', 'y', 'z'])
V4 = namedtuple('Point4', ['x', 'y', 'z', 'w'])

def char(c):
    #1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    #2 bytes
    return struct.pack('=h', w)

def dword(d):
    #4 bytes
    return struct.pack('=l', d)

def color(r, g, b):
    return bytes([int(b * 255),
                  int(g * 255),
                  int(r * 255)] )

def baryCoords(A, B, C, P):

    areaPBC = (B.y - C.y) * (P.x - C.x) + (C.x - B.x) * (P.y - C.y)
    areaPAC = (C.y - A.y) * (P.x - C.x) + (A.x - C.x) * (P.y - C.y)
    areaABC = (B.y - C.y) * (A.x - C.x) + (C.x - B.x) * (A.y - C.y)

    try:
        # PBC / ABC
        u = areaPBC / areaABC
        # PAC / ABC
        v = areaPAC / areaABC
        # 1 - u - v
        w = 1 - u - v
    except:
        return -1, -1, -1
    else:
        return u, v, w
    

class Raytracer(object):
    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.fov = 60
        self.nearPlane = 0.1
        self.camPosition = [0,0,0]

        self.scene = [ ]
        self.lights = [ ]

        self.envMap = None


        self.clearColor = color(0,0,0)
        self.currColor = color(1,1,1)

        self.glViewport(0,0,self.width, self.height)
        
        self.glClear()

    def glViewport(self, posX, posY, width, height):
        self.vpX = posX
        self.vpY = posY
        self.vpWidth = width
        self.vpHeight = height

    def glClearColor(self, r, g, b):
        self.clearColor = color(r,g,b)

    def glColor(self, r, g, b):
        self.currColor = color(r,g,b)

    def glClear(self):
        self.pixels = [[ self.clearColor for y in range(self.height)]
                        for x in range(self.width)]

    def glClearViewport(self, clr = None):
        for x in range(self.vpX, self.vpX + self.vpWidth):
            for y in range(self.vpY, self.vpY + self.vpHeight):
                self.glPoint(x,y,clr)


    def glPoint(self, x, y, clr = None): # Window Coordinates
        if (0 <= x < self.width) and (0 <= y < self.height):
            self.pixels[x][y] = clr or self.currColor

    def scene_intersect(self, orig, dir, sceneObj):
        depth = float('inf')
        intersect = None

        for obj in self.scene:
            hit = obj.ray_intersect(orig, dir)
            if hit != None:
                if sceneObj != hit.sceneObj:
                    if hit.distance < depth:
                        intersect = hit
                        depth = hit.distance

        return intersect

    def cast_ray(self, orig, dir, sceneObj = None, recursion = 0):
        intersect = self.scene_intersect(orig, dir, sceneObj)

        if intersect == None or recursion >= MAX_RECURSION_DEPTH:
            if self.envMap:
                return self.envMap.getEnvColor(dir)
            else:
                return (self.clearColor[0] / 255,
                        self.clearColor[1] / 255,
                        self.clearColor[2] / 255)

        material = intersect.sceneObj.material

        finalColor =    [0,0,0]
        objectColor = [material.diffuse[0],
                        material.diffuse[1],
                        material.diffuse[2]]

        if material.matType == OPAQUE:
            for light in self.lights:
                diffuseColor = light.getDiffuseColor(intersect, self)
                specColor = light.getSpecColor(intersect, self)
                shadowIntensity = light.getShadowIntensity(intersect, self)

                lightColor = lib.ScalarMul(lib.Add(diffuseColor, specColor), (1 - shadowIntensity))

                finalColor = lib.Add(finalColor, lightColor)

        elif material.matType == REFLECTIVE:
            reflect = reflectVector(intersect.normal, lib.ScalarMul(list(dir), -1))
            reflectColor = self.cast_ray(intersect.point, reflect, intersect.sceneObj, recursion + 1)
            reflectColor = list(reflectColor)

            specColor = [0,0,0]
            for light in self.lights:
                specColor = lib.Add(specColor, light.getSpecColor(intersect, self))

            finalColor = lib.Add(reflectColor, specColor)
        
        elif material.matType == TRANSPARENT:
            
            outside = lib.dot(list(dir), intersect.normal) < 0.0
            #print("dir", dir, "intesect", intersect.normal)
            #print("mul:", lib.dot(list(dir), intersect.normal))
            bias = lib.ScalarMul(intersect.normal, 0.001)
            
            specColor = [0,0,0]
            for light in self.lights:
                specColor = lib.Add(specColor, light.getSpecColor(intersect, self))
            
            reflect = reflectVector(intersect.normal, lib.ScalarMul(list(dir),-1))
            reflectOrig = lib.Add(intersect.point, bias) if outside else lib.Subtract(intersect.point, bias)
            reflectColor = self.cast_ray(reflectOrig, reflect, None, recursion +1)
            reflectColor = list(reflectColor)
            
            kr = fresnel(intersect.normal, dir, material.ior)
            refractColor =[0,0,0]
            if kr < 1:
                refract = refractVector(intersect.normal, dir, material.ior)
                refractOrig = lib.Subtract(intersect.point, bias) if outside else lib.Add(intersect.point, bias)
                refractColor = self.cast_ray(refractOrig, refract, None, recursion +1)
                refractColor = list(refractColor)
            finalColor = lib.Add(lib.Add(lib.ScalarMul(reflectColor,kr), lib.ScalarMul(refractColor, (1-kr))),specColor)
            


        finalColor = lib.mul(finalColor,objectColor)

            
        if material.texture and intersect.texcoords:
            texColor = material.texture.getColor(intersect.texcoords[0], intersect.texcoords[1])
            if texColor is not None:
                finalColor = lib.mul(finalColor,list(texColor))

        r = min(1, finalColor[0])
        g = min(1, finalColor[1])
        b = min(1, finalColor[2])

        return (r,g,b)


    def glRender(self):
        # Proyeccion
        t = tan((self.fov * np.pi / 180) / 2) * self.nearPlane
        r = t * self.vpWidth / self.vpHeight

        for y in range(self.vpY, self.vpY + self.vpHeight + 1, STEPS):
            for x in range(self.vpX, self.vpX + self.vpWidth + 1, STEPS):
                # Pasar de coordenadas de ventana a
                # coordenadas NDC (-1 a 1)
                Px = ((x + 0.5 - self.vpX) / self.vpWidth) * 2 - 1
                Py = ((y + 0.5 - self.vpY) / self.vpHeight) * 2 - 1

                Px *= r
                Py *= t

                direction = list((Px, Py, -self.nearPlane))
                #print("Direction", direction, "norm: ",lib.norm(direction))
                direction = lib.scalarDiv(direction, lib.norm(direction))
                #print("Direction", direction)
                #print(direction[4])

                rayColor = self.cast_ray(self.camPosition, direction)

                if rayColor is not None:
                    rayColor = color(rayColor[0],rayColor[1],rayColor[2])
                    self.glPoint(x, y, rayColor)

    def glFinish(self, filename):
        with open(filename, "wb") as file:
            # Header
            file.write(bytes('B'.encode('ascii')))
            file.write(bytes('M'.encode('ascii')))
            file.write(dword(14 + 40 + (self.width * self.height * 3)))
            file.write(dword(0))
            file.write(dword(14 + 40))

            #InfoHeader
            file.write(dword(40))
            file.write(dword(self.width))
            file.write(dword(self.height))
            file.write(word(1))
            file.write(word(24))
            file.write(dword(0))
            file.write(dword(self.width * self.height * 3))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))
            file.write(dword(0))

            #Color table
            for y in range(self.height):
                for x in range(self.width):
                    file.write(self.pixels[x][y])