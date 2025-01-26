from PIL import Image

from esagil.source.utilities.images import bugged_pixel
from esagil.source.utilities.project import get_resource

input_image = Image.open(get_resource('pj68/raw/ImageSet/JNCE_2024362_68C00012_V01-raw.png'))

width, height = input_image.size
output_image = Image.new('L', (width, height))

for y in range(height):
    for x in range(width):
        v = bugged_pixel(input_image, x, y, width, height)
        if v > 0:
            out = int(255)
        else:
            out = 0
        output_image.putpixel((x, y), out)
        #output_image.putpixel((x, y + 128*i), (round(255*SQRT_COMPANDING_TABLE[r]/2879), round(255*SQRT_COMPANDING_TABLE[g]/2879), round(255*SQRT_COMPANDING_TABLE[b]/2879)))

output_image.save(get_resource('pj68/frames/filter.png'))