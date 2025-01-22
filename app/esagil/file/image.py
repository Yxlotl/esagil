import numpy as np
from PIL import Image

from app.esagil.file.util import sqrt_companding_table

input_image = Image.open("../../../data/pj68/raw/ImageSet/JNCE_2024362_68C00012_V01-raw.png")

width, height = input_image.size
scan_height = height / 128

for i in range(int(scan_height / 3)):
    output_image = Image.new("RGB", (width, 128))
    for y in range(128):
        for x in range(width):
            b = input_image.getpixel((x, y + 128*(3*i + 0)))
            g = input_image.getpixel((x, y + 128*(3*i + 1)))
            r = input_image.getpixel((x, y + 128*(3*i + 2)))
            output_image.putpixel((x, y), (int(r),int(g),int(b)))
            #output_image.putpixel((x, y + 128*i), (round(255*sqrt_companding_table[r]/2879), round(255*sqrt_companding_table[g]/2879), round(255*sqrt_companding_table[b]/2879)))
    output_image.save("../../../data/pj68/frames/frame{0}.png".format(i))