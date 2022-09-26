from gl import Raytracer, V3
from texture import *
from figures import *
from lights import *


width = 1024
height = 1054

# Materiales

oro = Material(diffuse = (0.6, 0.6, 0.2), spec = 16)
esmeralda = Material(diffuse = (0.0, 0.8, 0.0), spec = 8)

mirror = Material(diffuse = (0.9, 0.9, 0.9), spec = 64, matType = REFLECTIVE)
diamond = Material(diffuse = (0.0, 0.8, 0.8), spec = 64, matType = REFLECTIVE)
ruby = Material(diffuse = (0.8, 0.0, 0.0), spec = 64, matType = REFLECTIVE)
glass = Material(diffuse = (0.9, 0.9, 0.9), ior = 1.2, spec = 64, matType = TRANSPARENT)
gota = Material(diffuse = (0.8, 1, 0.8), ior = 1.8, spec = 64, matType = TRANSPARENT)

rtx = Raytracer(width, height)

rtx.envMap = Texture("isla.bmp")

rtx.lights.append( AmbientLight(intensity = 0.1 ))
rtx.lights.append( DirectionalLight(direction = (-1,-1,-1), intensity = 0.8 ))
#rtx.lights.append( PointLight(point = (0,0,0)))

rtx.scene.append( Sphere(V3(1.5,3,-10), 1, glass)  )
rtx.scene.append( Sphere(V3(-1.5,3,-10), 1, gota)  )

rtx.scene.append( Sphere(V3(3,0,-10), 1, oro)  )
rtx.scene.append( Sphere(V3(-3,0,-10), 1, esmeralda)  )

rtx.scene.append( Sphere(V3(1.5,-3,-10),1, diamond)  )
rtx.scene.append( Sphere(V3(-1.5,-3,-10), 1, ruby)  ) 

''' rtx.scene.append(Sphere(V3(0,0,-10),3,glass))
'''

rtx.glRender()

rtx.glFinish("outputs/output.bmp")
