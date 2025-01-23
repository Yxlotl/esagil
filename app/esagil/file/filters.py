import numpy as np
from PIL import Image

from app.esagil.file.util import sqrt_companding_table, clamp, bugged_pixel

input_image = Image.open("../../../data/pj68/raw/ImageSet/JNCE_2024362_68C00012_V01-raw.png")

width, height = input_image.size
output_image = Image.new("L", (width, height))

for y in range(height):
    for x in range(width):
        v = bugged_pixel(input_image, x, y, width, height)
        if v > 0:
            out = int(255)
        else:
            out = 0
        output_image.putpixel((x, y), out)
        #output_image.putpixel((x, y + 128*i), (round(255*sqrt_companding_table[r]/2879), round(255*sqrt_companding_table[g]/2879), round(255*sqrt_companding_table[b]/2879)))

output_image.save("../../../data/pj68/frames/filter.png")