from argparse import ArgumentParser
from ast import parse
from bz2 import compress
from PIL import Image
import os, os.path


# consult https://github.com/RyanAWalters/PowerOf2ImageResizer

threshold = 0.25

sizes = [2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384]  # po2 sizes
valid_images = [".jpg", ".png", ".gif", ".bmp", ".tif"]

def get_closest_po2_val(y):
    return min(sizes, key=lambda x: abs(x - y))

def adjust_within_threshold(res, new_res):
    if (res - new_res) > int(new_res * threshold):
        return sizes[sizes.index(new_res) + 1]
    return new_res

def po2(im):
    width, height = im.size
    closest_po2_width = get_closest_po2_val(width)
    closest_po2_height = get_closest_po2_val(height)

    new_width = adjust_within_threshold(width, closest_po2_width)
    new_height = adjust_within_threshold(height, closest_po2_height)

    return im.resize((new_width, new_height), resample=Image.BICUBIC)


def main():
    parser = ArgumentParser(description="Resize image resolutions to the power of two")
    parser.add_argument('img_dir', help='Folder with images')
    parser.add_argument('-o', '--outimg', dest='resized_img_dir', type=str, help='Folder to store resized image files')
    parser.add_argument('-tj', '--to-jpg', dest='to_jpg', type=bool, default=True, const = True, nargs='?', help='Convert images to JPEG (True, False). Default True')
    parser.add_argument('-q', '--quality', dest='jpg_quality', type=int, default=95, const=95, nargs='?', help='The JPEG image quality, on a scale from 0 (worst) to 95 (best). Default 95')
    parser.add_argument('-c', '--compression', dest='compression', type=int, default=5, const = 5, nargs='?', help='Compression level (0-9, 0 = no compression). Default 5')

    args = parser.parse_args()
    img_dir = args.img_dir
    resized_img_dir = args.resized_img_dir
    to_jpg = args.to_jpg
    jpg_quality = args.jpg_quality
    compression = args.compression

    if not os.path.exists(resized_img_dir):
        os.makedirs(resized_img_dir)

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
            if to_jpg:
                if not im.mode == 'RGB':
                    im = im.convert('RGB')
                po2(im).save(new_img_path + ".jpg", "JPEG", quality=jpg_quality)
            else:
                img_format = im.format.lower()
                po2(im).save(new_img_path + "." + img_format, img_format, compress_level=compression)
            print(f)
    except MemoryError:
        print("OOM")


main()
