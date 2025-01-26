from PIL import Image

from esagil.source.utilities.images import bugged_pixel, avg_pixel
from esagil.source.utilities.project import get_resource

input_image = Image.open(get_resource('pj68/raw/ImageSet/JNCE_2024362_68C00012_V01-raw.png'))

width, height = input_image.size
scan_height = height / 128

for i in range(int(scan_height / 3)):
    output_image = Image.new('RGB', (width, 128))
    for y in range(128):
        for x in range(width):
            #adding filtering here
            r, g, b = 0.0, 0.0, 0.0

            if bugged_pixel(input_image, x, y + 128*(3*i + 0), width, height) > 0:
                b = avg_pixel(input_image, x, y + 128*(3*i + 0), width, height)
            else:
                b = input_image.getpixel((x, y + 128*(3*i + 0)))
            if bugged_pixel(input_image, x, y + 128*(3*i + 1), width, height) > 0:
                g = avg_pixel(input_image, x, y + 128*(3*i + 1), width, height)
            else:
                g = input_image.getpixel((x, y + 128*(3*i + 1)))
            if bugged_pixel(input_image, x, y + 128*(3*i + 2), width, height) > 0:
                r = avg_pixel(input_image, x, y + 128*(3*i + 2), width, height)
            else:
                r = input_image.getpixel((x, y + 128*(3*i + 2)))
            output_image.putpixel((x, y), (int(r),int(g),int(b)))
            #output_image.putpixel((x, y + 128*i), (round(255*SQRT_COMPANDING_TABLE[r]/2879), round(255*SQRT_COMPANDING_TABLE[g]/2879), round(255*SQRT_COMPANDING_TABLE[b]/2879)))
    output_image.save(get_resource('pj68/frames/frame{0}.png'.format(i)))