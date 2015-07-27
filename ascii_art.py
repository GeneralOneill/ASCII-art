import os.path
import random
import string
import urllib
from bisect import bisect
from PIL import Image
from termcolor import colored

CHAR_MAPPING = {60: " ",
                120: ".,-",
                160: "\\~c=!/|_iv",
                190: "gt[+]/(7jez2VfYL)T",
                200: "m*Q4ZGbNDdK5PXY",
                230: "8WAMK",
                255: "#%$"
                }
GREY_SCALE = False
RESIZE_WIDTH = 500.0
SCALE_OFFSET = 0.5

def downloadAndSave(img_url):
    filename = ''.join(random.choice(string.ascii_uppercase + string.digits)
                       for _ in range(7))
    while os.path.exists(filename):
        filename = ''.join(random.choice(string.ascii_uppercase + string.digits)
                           for _ in range(7))
    urllib.urlretrieve (img_url, "%s.jpg" % filename)
    return "%s.jpg" % filename

def acquireAndScale(filename):
    if not os.path.isfile(filename):
        return None
    im = Image.open(filename)
    scale_factor = RESIZE_WIDTH / im.size[0]
    im = im.resize((int(im.size[0] * scale_factor),
                    int(im.size[1] * scale_factor * SCALE_OFFSET)),
                    Image.BILINEAR)
    return im

def printGreyScaleImage(im):
    final_str = ""
    print im.size
    grey_levels = CHAR_MAPPING.keys()
    grey_levels.sort()
    for y in range(0,im.size[1]):
        for x in range(0,im.size[0]):
            pixel = im.getpixel((x,y))
            grey = (pixel[0] + pixel[1] + pixel[2]) / 3
            lum = grey # 255 - grey if terminal background is white
            possibles = CHAR_MAPPING[grey_levels[bisect(grey_levels,lum)]]
            if GREY_SCALE:
                grey_bash = 232 + (256 - 232) * lum/255
            else:
                grey_bash = 255
            final_str=final_str+'\033[38;5;' + str(grey_bash) +'m' + possibles[random.randint(0,len(possibles)-1)]
        final_str=final_str+"\n"+" \033[38;5;255m"
    print final_str

image_url = raw_input("Enter image url:")
image = acquireAndScale(downloadAndSave(image_url))
if image is not None:
    printGreyScaleImage(image)
else:
    print "Image not found"
