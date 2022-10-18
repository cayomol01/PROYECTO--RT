from re import M
from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 1024
height = 1054

# Materiales

oro = Material(diffuse = (0.6, 0.6, 0.2), spec = 100)
esmeralda = Material(diffuse = (0.0, 0.8, 0.0), spec = 100)
lapis = Material(diffuse = (0.0, 0.6, 0.6), spec = 100)

mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
diamond = Material(diffuse = (0.0, 0.8, 0.8), spec = 64, matType = REFLECTIVE)
ruby = Material(diffuse = (0.8, 0.0, 0.0), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), ior = 1.2, spec = 64, matType = TRANSPARENT)
gota = Material(diffuse = (0.8, 1, 0.8), ior = 1.8, spec = 64, matType = TRANSPARENT)

#Refracción del humor acuoso es de 1.34
eye = Material(diffuse = (0.9, 0.9, 0.9), ior = 1.34, spec = 64, matType = REFLECTIVE)
BLACK = Material(diffuse = (0.0, 0.0, 0.0), ior = 1.34, spec = 64, matType = OPAQUE)
brillo = Material(diffuse = (1.0, 1.0, 1.0), ior = 1.34, spec = 64, matType = OPAQUE)
BGREEN = Material(diffuse = (0.2, 0.9, 0.7), ior = 1.34, spec = 50,texture=Texture("Assets/BFeathers.bmp"), matType = REFLECTIVE)
HGREEN = Material(diffuse = (0.2, 0.9, 0.7), ior = 1.34, spec = 50,texture=Texture("Assets/HFeathers.bmp"), matType = REFLECTIVE)
PICO = Material(diffuse = (1.0, 0.5, 0.0), ior = 1.34, spec = 50, texture= Texture("Assets/Streak.bmp"), matType = OPAQUE)
PICOA = Material(diffuse = (0.9, 0.4, 0.0), ior = 1.34, spec = 50, texture= Texture("Assets/Streak.bmp"), matType = OPAQUE)
PATAS = Material(diffuse = (0.9, 0.4, 0.0), ior = 1.5, spec = 50, matType = OPAQUE)
DEDOS = Material(diffuse = (0.9, 0.4, 0.0), ior = 1.5, spec = 50, matType = TRANSPARENT)





#loro/quetzal
def Loro():
    rtx.scene.append(Sphere((0,0.0,-30), 3, material = HGREEN))
    rtx.scene.append(Sphere((0,0,-26), 1, material = eye))
    rtx.scene.append(Sphere((0,0,-23), 0.5, material = BLACK))
    rtx.scene.append(Sphere((-0.1,0.1,-12), 0.1, material = brillo))
    #PICO ABAJO
    rtx.scene.append( Triangle(v2 = (0.5,0.9,-10), v0 = (1.0,0.0,-10), v1 = (3.0,0.0,-10), material = PICOA) )
    rtx.scene.append( Triangle(v0 = (0.5,-0.9,-10), v1 = (3,0.0,-10), v2 = (1.0,0.0,-10), material = PICO) )
    #PICO ARRIBA
    #rtx.scene.append( Triangle(v0 = (-3,0,-7), v1 = (0,0,-7), v2 = (0,3,-7), material = gota) )
    rtx.scene.append(Sphere((-3,-6,-30), 5, material = BGREEN))
    rtx.scene.append(AABB((-4,-12,-30), (1,3,1), material=PATAS))
    rtx.scene.append(AABB((-1,-12,-30), (1,3,1), material=PATAS))
    rtx.scene.append(Disk((-0.5,-14,-30), 2, (0,1,0), material=DEDOS))
    rtx.scene.append(Disk((-3.5,-14,-30), 2, (0,1,0), material=DEDOS))
    
    
    
    
    
rtx = Raytracer(width, height)

rtx.envMap = Texture("Assets/studio.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
rtx.lights.append( PointLight(point = (0,0,0)))

Loro()
'''rtx.scene.append( Triangle(v0 = (-3,0,-7), v1 = (0,0,-7), v2 = (0,3,-7), material = gota) )
rtx.scene.append( Triangle(v0 = (0,0,-7), v1 = (3,1.5,-7), v2 = (0,3,-9), material = ruby) )
rtx.scene.append( Triangle(v0 = (-1.5,1.5,-7), v1 = (0,3,-7), v2 = (-3,3,-7), material = oro) )'''


''' rtx.scene.append(Plane(position = (0,-20,0), normal = (0,1,0), material = oro))
rtx.scene.append(Plane(position = (0,20,0), normal = (0,-1,0), material = oro))
rtx.scene.append(Plane(position = (-30,0,0), normal = (1,0,0), material = esmeralda))
rtx.scene.append(Plane(position = (30,0,0), normal = (-1,0,0), material = esmeralda))
rtx.scene.append(AABB(position = (0,0,-30), size = (6,4,4), material = lapis))

rtx.scene.append(AABB(position = (2, 2, -10), size = (2,2,2), material = diamond))
rtx.scene.append(AABB(position = (-2, -2, -10), size = (2,2,2), material = ruby))
 '''
 
''' rtx.scene.append( Disk2(position = (0,-2,-7), radius = 4, radius2 = 2, normal = (0,1,0), material = gota ))
 '''
''' 
rtx.scene.append( Sphere(V3(1.5,3,-10), 1, glass)  )
rtx.scene.append( Sphere(V3(-1.5,3,-10), 1, gota)  )

rtx.scene.append( Sphere(V3(3,0,-10), 1, oro)  )
rtx.scene.append( Sphere(V3(-3,0,-10), 1, esmeralda)  )

rtx.scene.append( Sphere(V3(1.5,-3,-10),1, diamond)  )
rtx.scene.append( Sphere(V3(-1.5,-3,-10), 1, ruby)  ) 
 '''
''' rtx.scene.append(Sphere(V3(0,0,-10),3,glass))


'''

rtx.glRender()

rtx.glFinish("outputs/output.bmp")
