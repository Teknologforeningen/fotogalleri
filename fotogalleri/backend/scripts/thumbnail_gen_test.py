from thumbnail_utils import generate_thumbnails, save_img_to_path

thumbnails = generate_thumbnails("scripts/test_img.png", minsizes=[
                                 20, 30], maxsizes=[5, 10])
print(thumbnails)
for thumbnail in thumbnails:
    save_img_to_path(thumbnail, "test", "scripts/test_thumbnails/")
