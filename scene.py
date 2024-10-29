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

    def add_light(self, light):
        self.lights.append(light)

    def load(self):
        app = self.app

        self.add_light(Light(position=glm.vec3(5, 2, 0), color=(0, 1, 0)))
        self.add_light(Light(position=glm.vec3(-5, 2, 0), color=(1, 0, 0)))

        self.add_object(Cube(app, position=(-3, 0, 0)))
        self.add_object(Cube(app))

    def render(self):
        for object in self.objects:
            object.render()