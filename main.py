from gl import Raytracer, V3
from figures import *
from lights import *


width = 1024
height = 1024

# Materiales

brick = Material(diffuse = (0.8, 0.3, 0.3))
stone = Material(diffuse = (0.4, 0.4, 0.4))
grass = Material(diffuse = (0.3, 1, 0.3))

snow = Material(diffuse = (0.9,0.9,0.9))
button = Material(diffuse = (0.2,0.2,0.2))
mouth = Material(diffuse=(0.4,0.4,0.4))
nose = Material(diffuse = (1,0.63,0.20))

oeye = Material(diffuse=(1,1,1))
ieye = Material(diffuse=(0,0,0))



rtx = Raytracer(width, height)

rtx.lights.append( AmbientLight( ))
rtx.lights.append( DirectionalLight(direction = (0,0,-1) ))


''' rtx.scene.append( Sphere(V3(0,0,-10), 2, brick)  )
rtx.scene.append( Sphere(V3(-4,-2,-15), 1.5, stone)  )
rtx.scene.append( Sphere(V3(2,2,-8), 0.2, grass)  )
 '''

#snowballs
rtx.scene.append(Sphere(V3(0,-2,-10), 2.5, snow))
rtx.scene.append(Sphere(V3(0,1,-10), 2, snow))
rtx.scene.append(Sphere(V3(0,3.5,-10), 1.5, snow))

#buttons
rtx.scene.append(Sphere(V3(0,-1.5,-7.5), 0.40, button))
rtx.scene.append(Sphere(V3(0,0,-8), 0.30, button))
rtx.scene.append(Sphere(V3(0,1.5,-8), 0.30, button))

#mouth
rtx.scene.append(Sphere(V3(-0.5,2.9,-8.75), 0.125, mouth))
rtx.scene.append(Sphere(V3(0.5,2.9,-8.75), 0.125, mouth))
rtx.scene.append(Sphere(V3(0.20,2.8,-8.75), 0.125, mouth))
rtx.scene.append(Sphere(V3(-0.20,2.8,-8.75), 0.125, mouth))


#Nose
rtx.scene.append(Sphere(V3(0,3.5,-8.50), 0.20, nose))

#eyes
rtx.scene.append(Sphere(V3(-0.50, 3.75, -8.70), 0.20, oeye))
rtx.scene.append(Sphere(V3(-0.50, 3.75, -8.55), 0.125, ieye))

rtx.scene.append(Sphere(V3(0.50, 3.75, -8.70), 0.20, oeye))
rtx.scene.append(Sphere(V3(0.50, 3.75, -8.55), 0.125, ieye))


rtx.glRender()

rtx.glFinish("outputs/snowman.bmp")