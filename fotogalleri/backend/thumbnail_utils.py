from PIL import Image
import glob
import os
import base64
from io import BytesIO


def generate_thumbnails(img_path, minsizes=[], maxsizes=[]):
    """
    Resizes given image to specified sizes, either define the length of 
    the shorter side (minsizes) or longer side (maxsizes). Generates a thumbnail
    for each element in either list. No thumbnail will be generated if the generated
    thumbnail would be bigger than the original image.

    Returns a list of PIL Image objects.

    :param img_path: path to source image
    :param minsizes: list of integers (sizes) for "short side" resizing
    :param maxsizes: list of integers (sizes) for "long side" resizing
    """
    if not minsizes and not maxsizes:
        raise ValueError(
            "This function needs at least one minsize or maxsize for thumbnail")
    img = Image.open(infile)

    sizes = maxsizes
    for s in minsizes:
        # Calculate the max size from min size
        w, h = img.size
        sizes.append(s * (w/h) if w > h else s * (h/w))

    thumbnails = []
    for s in sizes:
        # Only generate thumbnail if it would be smaller than the original image
        if needs_thumbnail(img, s):
            thumbnails.append(img.copy().thumbnail((s, s)))
    return thumbnails


def pil_to_base64(image):
    """
    :param image: PIL Image object
    returns: base64 string
    """
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue())


def needs_thumbnail(image, maxsize):
    w, h = image.size
    return w > maxsize and h > maxsize
