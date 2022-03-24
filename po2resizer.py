from argparse import ArgumentParser
from PIL import Image
import os, os.path

from numpy import size

# consult https://github.com/RyanAWalters/PowerOf2ImageResizer

#threshold = 0.25

#sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192]  # po2 sizes
sizes = []

valid_images = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".pjpeg", ".png", ".gif", ".bmp", ".tif", ".tiff"]

def get_closest_po2_val(y):
    return min(sizes, key=lambda x: abs(x - y))

def adjust_within_threshold(res, new_res, threshold):
    if (res - new_res) > int(new_res * threshold):
        #cannot increase over the limit anymore..
        if new_res == sizes[-1]:
            return new_res
        return sizes[sizes.index(new_res) + 1] #increase the new resolution according to threshold
    return new_res

def po2(im, threshold):
    width, height = im.size
    closest_po2_width = get_closest_po2_val(width)
    closest_po2_height = get_closest_po2_val(height)

    new_width = adjust_within_threshold(width, closest_po2_width, threshold)
    new_height = adjust_within_threshold(height, closest_po2_height, threshold)

    return im.resize((new_width, new_height), resample=Image.LANCZOS)

def aspect_ratio_resize(im, threshold):
    width, height = im.size
    largest = max(width, height)
    closest_po2_largest = get_closest_po2_val(largest)
    res = adjust_within_threshold(largest, closest_po2_largest, threshold)
    return res

def parse_cmd():
    parser = ArgumentParser(description="Resize image resolutions to the power of two")
    parser.add_argument('img_dir', help='Folder with images')
    parser.add_argument('-o', '--outimg', dest='resized_img_dir', type=str, help='Folder to store resized image files')
    parser.add_argument('-j', '--to-jpg', dest='to_jpg', type=int, default=1, const=1, nargs='?', help='Convert images to JPEG (0 yes, 1 no). Default 1')
    parser.add_argument('-q', '--quality', dest='jpg_quality', type=int, default=95, const=95, nargs='?', help='The JPEG image quality, on a scale from 0 (worst) to 95 (best). Default 95')
    parser.add_argument('-c', '--compression', dest='compression', type=int, default=5, const =5, nargs='?', help='Compression level (0-9, 0 = no compression). Default 5')

    args = parser.parse_args()
    img_dir = args.img_dir
    resized_img_dir = args.resized_img_dir
    to_jpg = args.to_jpg
    jpg_quality = args.jpg_quality
    compression = args.compression

def resizer(img_dir, resized_img_dir, threshold, max_res, to_jpg, jpg_quality, compression):
    if not os.path.exists(resized_img_dir):
        os.makedirs(resized_img_dir)

    global sizes
    x = 1
    while True:
        new_x = x*2
        if new_x > max_res:
            if (max_res - x) > int(x * threshold):
                sizes.append(new_x)
                break
            break
        sizes.append(new_x)
        x = new_x

    try:
        for f in os.listdir(img_dir):
            ext = os.path.splitext(f)[1]
            name = os.path.splitext(f)[0]
            if ext.lower() not in valid_images:
                continue
            img_path = os.path.join(img_dir,f)
            new_img_path = os.path.join(resized_img_dir, name)

            #print(img_path, new_img_path)
            im = Image.open(img_path)

            #resize to the maximum of max_res while keeping aspect ratio
            new_res = aspect_ratio_resize(im, threshold)
            im.thumbnail((new_res, new_res), Image.LANCZOS)

            if to_jpg == 1:
                if not im.mode == 'RGB':
                    im = im.convert('RGB')
                po2(im, threshold).save(new_img_path + ".jpg", "JPEG", quality=jpg_quality)
            else:
                img_format = im.format.lower()
                po2(im, threshold).save(new_img_path + "." + img_format, img_format, compress_level=compression)
            print(f)
            #img_format = im.format.lower()
            #im.save(new_img_path + "." + img_format, img_format, compress_level=compression)
    except MemoryError:
        print("OOM")

    sizes.clear()
    print("Run finished")
