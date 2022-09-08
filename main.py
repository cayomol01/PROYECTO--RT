from gl import Raytracer, V3
from figures import *
from lights import *


width = 1024
height = 1024

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3))
stone = Material(diffuse = (0.4, 0.4, 0.4))
grass = Material(diffuse = (0.3, 1, 0.3))

snow = Material(diffuse = (1,1,1))
button = Material(diffuse = (0.2,0.2,0.2))



rtx = Raytracer(width, height)

rtx.lights.append( AmbientLight( ))
rtx.lights.append( DirectionalLight(direction = (0,0,-1) ))


''' rtx.scene.append( Sphere(V3(0,0,-10), 2, brick)  )
rtx.scene.append( Sphere(V3(-4,-2,-15), 1.5, stone)  )
rtx.scene.append( Sphere(V3(2,2,-8), 0.2, grass)  )
 '''


rtx.scene.append(Sphere(V3(0,-2,-10), 2.5, snow))
rtx.scene.append(Sphere(V3(0,1,-10), 2, snow))
rtx.scene.append(Sphere(V3(0,3.5,-10), 1.5, snow))
rtx.scene.append(Sphere(V3(0,-1.5,-7.5), 0.50, button))
rtx.scene.append(Sphere(V3(0,0,-8), 0.25, button))
rtx.scene.append(Sphere(V3(0,1.5,-8), 0.25, button))
rtx.glRender()

rtx.glFinish("outputs/output.bmp")