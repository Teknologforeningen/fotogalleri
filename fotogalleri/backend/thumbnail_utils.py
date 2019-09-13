from PIL import Image
import os


def generate_thumbnails(img_path, minsizes=[], maxsizes=[]):
    """
    Resizes given image to specified sizes, either define the length of 
    the shorter side (minsizes) or longer side (maxsizes). Generates a thumbnail
    for each size in both lists. If the generated thumbnail would be as big as or
    bigger than the original image, returns the original image instead.

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
        # Calculate the max size from min size, since the
        # thumbnail function only scales to max size
        w, h = img.size
        sizes.append(s * (w/h) if w > h else s * (h/w))

    thumbnails = []
    for s in sizes:
        w, h = img.size
        temp = img.copy()
        if w > s and h > s:
            # Thumbnail will retain its aspect ratio, but be scaled down to fit
            # inside a s x s square.
            temp.thumbnail((s, s))
        thumbnails.append(temp)
    return thumbnails


def save_img_to_path(image, filename, img_path):
    """
    Converts PIL Image to jpg and saves it to img_path.
    This function will overwrite an existing image with the same filename
    """
    if not os.path.exists(img_path):
        os.makedirs(img_path)
    w, h = image.size
    # Remove possible file extension from name
    name, _ = os.path.splitext(filename)
    name += "{w}x{h}".format(w=w, h=h)

    # Some image formats (PNG) are in RGBA, which jpg doesn't support
    rgb_image = image.convert('RGB')
    rgb_image.save(img_path + name + ".jpg", format="JPEG")
