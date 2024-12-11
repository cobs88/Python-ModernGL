from model import *
from light import Light

class Scene:
    def __init__(self, app):
        self.app = app
        self.objects = []
        self.lights = []
        self.load()

    def add_object(self, object):
        self.objects.append(object)

    # MAXIMUM OF 10 LIGHTS PER SCENE !!!
    def add_light(self, light):
        self.lights.append(light)

    def load(self):
        app = self.app

        #self.add_light(Light(position=glm.vec3(3, 3, 3), color=(1, 1, 1)))
        self.add_light(Light(position=glm.vec3(3, 3, 3), color=(1, 1, 1), Ia = 1, Id = 0, Is = 0))

        self.add_object(Map(app))

    def render(self):
        for object in self.objects:
            object.render()