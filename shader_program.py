class ShaderProgram:
    def __init__(self, context):
        self.context = context
        self.programs = {}
        self.programs['default'] = self.get_program('default')

    def get_program(self, shader_program_name):
        with open(f'shaders/{shader_program_name}.vert') as file:
            vertex_shader = file.read()

        with open(f'shaders/{shader_program_name}.frag') as file:
            fragment_shader = file.read()

        program = self.context.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)
        return program
    
    def destroy(self):
        [program.release() for program in self.programs.values()]