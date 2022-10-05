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

rtx = Raytracer(width, height)

rtx.envMap = Texture("isla.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
rtx.lights.append( PointLight(point = (0,0,0)))

''' rtx.scene.append(Plane(position = (0,-20,0), normal = (0,1,0), material = oro))
rtx.scene.append(Plane(position = (0,20,0), normal = (0,-1,0), material = oro))
rtx.scene.append(Plane(position = (-30,0,0), normal = (1,0,0), material = esmeralda))
rtx.scene.append(Plane(position = (30,0,0), normal = (-1,0,0), material = esmeralda))
rtx.scene.append(AABB(position = (0,0,-30), size = (6,4,4), material = lapis))

rtx.scene.append(AABB(position = (2, 2, -10), size = (2,2,2), material = diamond))
rtx.scene.append(AABB(position = (-2, -2, -10), size = (2,2,2), material = ruby))
 '''
 
rtx.scene.append( Disk2(position = (0,-2,-7), radius = 4, radius2 = 2, normal = (0,1,0), material = gota ))

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

rtx.glFinish("outputs/preuba.bmp")
''' SOL(gmt)
gmt tiene que ser un numero de 0-20 representando la hora del dia:
    coor12 = (51,0.00)
    if gmt >12:
        desplazo = 15*(gmt-12)
        coor = (coor12[0], coor12[1] + desplazo)
    elif gmt <12:
        desplazO = 15*(12-gmt)
        coor = (coor12[0], coor12[1]-desplazo)
    else:
        coor  = coor12
    return coor
    '''