import pygame
import moderngl
import sys
from model import *
from camera import Camera
from light import Light
from mesh import Mesh

class GraphicsEngine: 
    def __init__(self, win_size=(800, 600)):
        pygame.init()

        self.WIN_SIZE = win_size

        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 4)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 6)
        pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)

        pygame.display.set_mode(self.WIN_SIZE, flags=pygame.OPENGL | pygame.DOUBLEBUF)

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)
        print("running...")

        self.context = moderngl.create_context() # creates an opengl context
        self.context.enable(flags=moderngl.DEPTH_TEST | moderngl.CULL_FACE) # enables depth testing and face culling

        # makes a clock to track time and delta time
        self.clock = pygame.time.Clock()
        self.time = 0
        self.delta_time = 0

        self.mesh = Mesh(self)
        self.light = Light()
        self.camera = Camera(self)
        self.scene = Cube(self)
        
    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                self.mesh.destroy()
                pygame.quit()
                sys.exit()

    def render(self):
        self.context.clear(color=(0.08, 0.16, 0.18)) # draws the background

        self.scene.render() # render the scene

        pygame.display.flip()
    
    def get_time(self):
        self.time = pygame.time.get_ticks() * 0.001

    def run(self):
        while True:
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)

if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()