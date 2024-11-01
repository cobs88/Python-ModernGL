import glm

class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1)):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        # light intensity
        self.Ia = 1 * self.color # ambient 
        self.Id = 0 * self.color # diffuse 
        self.Is = 0 * self.color # specular