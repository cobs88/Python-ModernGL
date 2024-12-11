from vbo import VBO
from shader_program import ShaderProgram

class VAO:
    def __init__(self, context):
        self.context = context
        self.vbo = VBO(context)
        self.program = ShaderProgram(context)
        self.vaos = {}

        self.vaos['plane'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['plane']
        )

        self.vaos['cube'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['cube']
        )

        self.vaos['map'] = self.get_vao(
            program = self.program.programs['default'],
            vbo = self.vbo.vbos['map']
        )

    def get_vao(self, program, vbo):
        vao = self.context.vertex_array(program, [(vbo.vbo, vbo.format, *vbo.attribs)])
        return vao
        
    def destroy(self):
        self.vbo.destroy()
        self.program.destroy()