import glm
import pygame

FOV = 50
NEAR = 0.1
FAR = 100
SPEED = 0.01
SENSITIVITY = 0.05

class Camera:
    def __init__(self, app, position=(0, 1.5, -2), yaw=-90, pitch=0):
        self.app = app
        self.aspect_ratio = app.WIN_SIZE[0] / app.WIN_SIZE[1]
        self.position = glm.vec3(position)

        # camera coordinates
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        self.forward = glm.vec3(0, 0, -1)

        # camera orientation
        self.yaw = yaw
        self.pitch = pitch

        # makes the view matrix
        self.m_view = self.get_view_matrix()
        # makes the projection matrix
        self.m_proj = self.get_projection_matrix()

    def rotate(self):
        rel_x, rel_y = pygame.mouse.get_rel()
        self.yaw += rel_x * SENSITIVITY
        self.pitch -= rel_y * SENSITIVITY
        self.pitch = max(-89, min(89, self.pitch))

    def update_camera_vectors(self):
        yaw, pitch = glm.radians(self.yaw), glm.radians(self.pitch)

        self.forward.x = glm.cos(yaw) * glm.cos(pitch)
        self.forward.y = glm.sin(pitch)
        self.forward.z = glm.sin(yaw) * glm.cos(pitch)

        self.forward = glm.normalize(self.forward)
        self.right = glm.normalize(glm.cross(self.forward, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.forward))

    def update(self):
        self.move()
        self.rotate()
        self.update_camera_vectors()
        self.m_view = self.get_view_matrix()

    def move(self):
        velocity = SPEED * self.app.delta_time
        keys = pygame.key.get_pressed()

        # key checks to move the camera
        if keys[pygame.K_w]:
            self.position += self.forward * velocity # move forward
        if keys[pygame.K_s]:
            self.position -= self.forward * velocity # move backwards
        if keys[pygame.K_a]:
            self.position -= self.right * velocity # move left
        if keys[pygame.K_d]:
            self.position += self.right * velocity # move right
        if keys[pygame.K_q]:
            self.position -= self.up * velocity # move down
        if keys[pygame.K_e]:
            self.position += self.up * velocity # move up


    def get_view_matrix(self):
        # glm can create the view matrix using lookat
        return glm.lookAt(self.position, self.position + self.forward, self.up)

    def get_projection_matrix(self):
        # makes the projection matrix using perspective
        return glm.perspective(glm.radians(FOV), self.aspect_ratio, NEAR, FAR)