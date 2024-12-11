import numpy
import moderngl
from objparser import OBJParser

class VBO:
    def __init__(self, context):
        self.vbos = {}
        self.vbos['plane'] = PlaneVBO(context)
        self.vbos['cube'] = CubeVBO(context)
        self.vbos['map'] = MapVBO(context)

    def destroy(self):
        [vbo.destroy() for vbo in self.vbos.values()]

class BaseVBO:
    def __init__(self, context):
        self.context = context
        self.vbo = self.get_vbo()
        self.format: str = None
        self.attrib: list = None

    def get_vertex_data(self): ...

    def get_vbo(self):
        vertex_data = self.get_vertex_data()
        vbo = self.context.buffer(vertex_data)
        return vbo
    
    def destroy(self):
        self.vbo.release()

class PlaneVBO(BaseVBO):
    def __init__(self, context):
        super().__init__(context)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')
    
    def get_vertex_data(self):
        # Define vertices for a flat plane
        vertices = [(-1, 0, -1), (1, 0, -1), (1, 0, 1), (-1, 0, 1)]  # Plane on the XZ axis at y=0
        
        # Indices for the plane (two triangles to form a square)
        indices = [(0, 2, 1), (0, 3, 2)]

        # Get vertex position data
        vertex_data = self.get_data(vertices, indices)

        # Texture coordinates for the plane
        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]

        # Texture coordinate indices (same pattern as the vertex indices)
        tex_coord_indices = [(0, 2, 1), (0, 3, 2)]

        # Get texture coordinate data
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        # Normal vector for the plane (pointing upwards, in the positive Y direction)
        normals = [(0, 1, 0)] * 6  # 6 vertices total for 2 triangles

        normals = numpy.array(normals, dtype='f4').reshape(6, 3)

        # Combine normal data with vertex data
        vertex_data = numpy.hstack([normals, vertex_data])
        vertex_data = numpy.hstack([tex_coord_data, vertex_data])

        return vertex_data

class CubeVBO(BaseVBO):
    def __init__(self, context):
        super().__init__(context)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']

    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return numpy.array(data, dtype='f4')
    
    def get_vertex_data(self):
        vertices = [(-1, -1, 1), (1, -1, 1), (1, 1, 1), (-1, 1, 1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), (1, 1, -1)]
        
        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        
        vertex_data = self.get_data(vertices, indices)

        tex_coord_vertices = [(0, 0), (1, 0), (1, 1), (0, 1)]

        tex_coord_indices = [(0, 2, 3), (0, 1, 2),
                             (0, 2, 3), (0, 1, 2),
                             (0, 1, 2), (2, 3, 0),
                             (2, 3, 0), (2, 0, 1),
                             (0, 2, 3), (0, 1, 2),
                             (3, 1, 2), (3, 0, 1)]
        
        tex_coord_data = self.get_data(tex_coord_vertices, tex_coord_indices)

        normals = [(0, 0, 1) * 6,
                   (1, 0, 0) * 6,
                   (0, 0, -1) * 6,
                   (-1, 0, 0) * 6,
                   (0, 1, 0) * 6,
                   (0, -1, 0) * 6]
        
        normals = numpy.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = numpy.hstack([normals, vertex_data])
        vertex_data = numpy.hstack([tex_coord_data, vertex_data])


        return vertex_data
    

class MapVBO(BaseVBO):
    def __init__(self, app):
        super().__init__(app)
        self.format = '2f 3f 3f'
        self.attribs = ['in_texcoord_0', 'in_normal', 'in_position']
        
    def get_vertex_data(self):
        parser = OBJParser("objects/house.obj")

        vertex_data = parser.load()
        
        return vertex_data
