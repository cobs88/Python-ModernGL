import pygame
import moderngl

class Texture:
    def __init__(self, context):
        self.context = context
        self.textures = {}
        self.textures[0] = self.get_texture(path='textures/dirt.png')
        self.textures['map'] = self.get_texture(path='textures/map.png')

    def get_texture(self, path):
        texture = pygame.image.load(path).convert()
        texture = pygame.transform.flip(texture, flip_x=False, flip_y=True)
        texture = self.context.texture(size=texture.get_size(), components=3, data=pygame.image.tostring(texture, 'RGB'))

        texture.filter = (moderngl.LINEAR_MIPMAP_LINEAR, moderngl.LINEAR)
        texture.build_mipmaps()

        texture.anisotropy = 32.0
        return texture
    
    def destroy(self):
        [tex.release() for tex in self.textures.values()]