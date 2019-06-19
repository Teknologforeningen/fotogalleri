from PIL import Image
import glob
import os
from tqdm import tqdm

# Width, height limit. Will limit to the "longer" side.
sizes = [(1920, 1920), (500, 500)]


def generate_thumbnails(dir_path, width, height):
    """
    Resizes an image to specified width and height, preserving aspect ratio.
    This means that the image will be constrained to either the width or height
    so that it is at most 'width' wide and 'height' high.

    This function will create thumnbail subdirectories in dir_path

    :param dir_path: path to directory with source images
    :param width: int, max width in pixels
    :param height: int, max height in pixels
    """
    for infile in tqdm(glob.glob(dir_path + "/*.jpg")):
        file, ext = os.path.splitext(infile)
        img = Image.open(infile)
        img.thumbnail((width, height))
        img_dir = f"thumbnails/{width}x{height}/"
        if not os.path.exists(img_dir):
            os.makedirs(img_dir)
        img.save(img_dir + file + ".thumbnail", "JPEG")
        img = square_crop(img)
        img.save(img_dir + file + ".crop", "JPEG")


def square_crop(img):
    w, h = img.size
    if w > h:
        top = 0
        bot = h
        left = w/2 - h/2
        right = w - left
    else:
        top = h/2 - w/2
        bot = h - top
        left = 0
        right = w
    return img.crop((left, top, right, bot))


for size in sizes:
    generate_thumbnails('.', *size)
