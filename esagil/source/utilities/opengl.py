import OpenGL.GL
import PIL.Image as Image
import numpy
from OpenGL.GL import *


def load_texture(filename):
    #Open the image and get the raw data to pass to the buffer
    img = Image.open(filename)
    img_raw = numpy.array(list(img.getdata()), numpy.uint8)
    #Generate a new texture id
    texture_id = glGenTextures(1)
    #Pass the pixels into a buffer
    glPixelStorei(GL_UNPACK_ALIGNMENT, 1)
    #Define the attributes of this buffer so that it can be rendered properly
    glTextureParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
    glTextureParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTextureParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
    glTextureParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTextureParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTextureParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    #Finally, create the texture
    glTexImage2D(GL_TEXTURE_2D, 0, GL_LUMINANCE, img.size[0], img.size[1], 0, GL_LUMINANCE, GL_UNSIGNED_BYTE, img_raw)
    return texture_id

def get_cube_verts(pos, len):
    len.x *= 0.5
    len.y *= 0.5
    len.z *= 0.5
    verts = (
        (pos.x + len.x, pos.y - len.y, pos.z - len.z),
        (pos.x + len.x, pos.y + len.y, pos.z - len.z),
        (pos.x - len.x, pos.y + len.y, pos.z - len.z),
        (pos.x - len.x, pos.y - len.y, pos.z - len.z),
        (pos.x + len.x, pos.y - len.y, pos.z + len.z),
        (pos.x + len.x, pos.y + len.y, pos.z + len.z),
        (pos.x - len.x, pos.y - len.y, pos.z + len.z),
        (pos.x - len.x, pos.y + len.y, pos.z + len.z)
    )
    return verts