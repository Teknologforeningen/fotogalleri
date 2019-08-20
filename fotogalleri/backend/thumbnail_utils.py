from PIL import Image
import os


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
    img = Image.open(img_path)

    sizes = maxsizes
    for s in minsizes:
        # Calculate the max size from min size
        w, h = img.size
        sizes.append(s * (w/h) if w > h else s * (h/w))

    thumbnails = []
    for s in sizes:
        # Only generate thumbnail if it would be smaller than the original image
        w, h = img.size
        if w > s and h > s:
            temp = img.copy()
            temp.thumbnail((s, s))
            thumbnails.append(temp)
    return thumbnails


def save_to_path(image, name, img_path):
    """
    Converts PIL Image to jpg and saves it to img_path
    """
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    w, h = image.size
    name += "{w}x{h}".format(w=w, h=h)
    # Some image formats (PNG) are in RGBA, which jpeg doesn't support
    rgb_image = image.convert('RGB')
    rgb_image.save(img_path + name + ".jpg", format="JPEG")
