import numpy
import glm
import pygame

class BaseModel:
    def __init__(self, app, vao_name, texture_id, position=(0, 0, 0), rotation=(0, 0, 0), scale=(0, 0, 0)):
        self.app = app
        self.position = position
        self.rotation = glm.vec3([glm.radians(a) for a in rotation])
        self.scale = scale
        self.m_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        # translation
        m_model = glm.translate(m_model, self.position)

        # rotation
        m_model = glm.rotate(m_model, self.rotation.x, glm.vec3(1, 0, 0))
        m_model = glm.rotate(m_model, self.rotation.y, glm.vec3(0, 1, 0))
        m_model = glm.rotate(m_model, self.rotation.z, glm.vec3(0, 0, 1))

        # scaling
        m_model = glm.scale(m_model, self.scale)

        return m_model
    
    def render(self):
        self.update()
        self.vao.render()

class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', texture_id=0, position=(0, 0, 0), rotation=(0, 0, 0), scale=(1, 1, 1)):
        super().__init__(app, vao_name, texture_id, position, rotation, scale)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.camera.m_view)
        self.program['camPos'].write(self.camera.position)

        for i, light in enumerate(self.app.scene.lights):
            self.program[f'lights[{i}].position'].write(light.position)
            self.program[f'lights[{i}].Ia'].write(light.Ia)
            self.program[f'lights[{i}].Id'].write(light.Id)
            self.program[f'lights[{i}].Is'].write(light.Is)

        self.program['lightCount'].value = len(self.app.scene.lights)  # Update the light count

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_0'] = 0
        self.texture.use()



        # textures
        self.program['u_texture_0'] = 0
        self.texture.use()

        # matrices
        self.program['m_proj'].write(self.app.camera.m_proj) # writes the projection matrix to the shader program
        self.program['m_view'].write(self.app.camera.m_view) # writes the view matrix to the shader program
        self.program['m_model'].write(self.m_model) # writes the model matrix to the shader program