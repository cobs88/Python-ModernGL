import numpy
import glm
import pygame

class BaseModel:
    def __init__(self, app, vao_name, texture_id):
        self.app = app
        self.m_model = self.get_model_matrix()
        self.texture_id = texture_id
        self.vao = app.mesh.vao.vaos[vao_name]
        self.program = self.vao.program
        self.camera = self.app.camera

    def update(self): ...

    def get_model_matrix(self):
        m_model = glm.mat4()
        return m_model
    
    def render(self):
        self.update()
        self.vao.render()

class Cube(BaseModel):
    def __init__(self, app, vao_name='cube', texture_id=0):
        super().__init__(app, vao_name, texture_id)
        self.on_init()

    def update(self):
        self.texture.use()
        self.program['m_model'].write(self.m_model)
        self.program['m_view'].write(self.camera.m_view)
        self.program['camPos'].write(self.camera.position)

    def on_init(self):
        self.texture = self.app.mesh.texture.textures[self.texture_id]
        self.program['u_texture_0'] = 0
        self.texture.use()

        # light
        self.program['light.position'].write(self.app.light.position)
        self.program['light.Ia'].write(self.app.light.Ia)
        self.program['light.Id'].write(self.app.light.Id)
        self.program['light.Is'].write(self.app.light.Is)

        # textures
        self.program['u_texture_0'] = 0
        self.texture.use()

        # matrices
        self.program['m_proj'].write(self.app.camera.m_proj) # writes the projection matrix to the shader program
        self.program['m_view'].write(self.app.camera.m_view) # writes the view matrix to the shader program
        self.program['m_model'].write(self.m_model) # writes the model matrix to the shader program