import numpy as np

class OBJParser:
    def __init__(self, filepath):
        self.filepath = filepath
        self.positions = []
        self.texcoords = []
        self.normals = []
        self.faces = []

    def load(self):
        with open(self.filepath, 'r') as file:
            for line in file:
                if line.startswith('v '):  # Vertex position
                    self.parse_vertex(line)
                elif line.startswith('vt '):  # Texture coordinate
                    self.parse_texcoord(line)
                elif line.startswith('vn '):  # Vertex normal
                    self.parse_normal(line)
                elif line.startswith('f '):  # Face (indices of vertex, texcoord, normal)
                    self.parse_face(line)
        return self.create_vertex_data()

    def parse_vertex(self, line):
        parts = line.strip().split()
        self.positions.append([float(parts[1]), float(parts[2]), float(parts[3])])

    def parse_texcoord(self, line):
        parts = line.strip().split()
        self.texcoords.append([float(parts[1]), float(parts[2])])

    def parse_normal(self, line):
        parts = line.strip().split()
        self.normals.append([float(parts[1]), float(parts[2]), float(parts[3])])

    def parse_face(self, line):
        parts = line.strip().split()[1:]
        face = []
        for part in parts:
            vals = part.split('/')
            position_index = int(vals[0]) - 1
            texcoord_index = int(vals[1]) - 1 if len(vals) > 1 and vals[1] != '' else None
            normal_index = int(vals[2]) - 1 if len(vals) > 2 else None
            face.append((position_index, texcoord_index, normal_index))
        self.faces.append(face)

    def create_vertex_data(self):
    # Pre-allocate the necessary NumPy arrays for positions, texcoords, and normals
        vertex_data = []
        for face in self.faces:
            for idx_tuple in face:
                # Extract position, texcoord, and normal
                position = np.array(self.positions[idx_tuple[0]])
                texcoord = np.array(self.texcoords[idx_tuple[1]]) if idx_tuple[1] is not None else np.array([0.0, 0.0])
                normal = np.array(self.normals[idx_tuple[2]]) if idx_tuple[2] is not None else np.array([0.0, 0.0, 0.0])

                # Concatenate using np.hstack
                vertex = np.hstack((texcoord, normal, position))
                vertex_data.append(vertex)

        # Convert the list of arrays into a single NumPy array
        return np.array(vertex_data, dtype='float32')
