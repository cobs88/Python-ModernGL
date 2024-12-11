import glm

class Light:
    def __init__(self, position=(3, 3, -3), color=(1, 1, 1), Ia = 0.05, Id = 0.5, Is = 1):
        self.position = glm.vec3(position)
        self.color = glm.vec3(color)

        # light intensity
        self.Ia = Ia * self.color # ambient 
        self.Id = Id * self.color # diffuse 
        self.Is = Is * self.color # specular