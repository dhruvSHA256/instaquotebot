import math
from PIL import Image
import os
import json
import random


def convert_img_insta(img, format="RGB"):
    # ratio = 4:5 = .80; width/height = .80; width = .80 * height

    # if img is filename
    if isinstance(img, str):
        img = Image.open(img)

    img_width, img_height = img.size
    minsize = (math.ceil(0.80 * img_height), img_height)
    img = img.resize(minsize, Image.Resampling.NEAREST)
    img = img.convert(format)
    return img


def recommend_font_size(text):
    size = 55
    l = len(text)

    resize_heuristic = 0.9
    resize_actual = 0.985
    while l > 1:
        l = l * resize_heuristic
        size = size * resize_actual

    return int(size)


def wrap_text(text, w=30):
    new_text = ""
    new_sentence = ""
    for word in text.split(" "):
        delim = " " if new_sentence != "" else ""
        new_sentence = new_sentence + delim + word
        if len(new_sentence) > w:
            new_text += "\n" + new_sentence
            new_sentence = ""
    new_text += "\n" + new_sentence
    return new_text


def get_random_quote(quotefile, TAGS):
    with open(quotefile, "r+") as qfp:
        data = json.load(qfp)
        randomtag = random.choice(TAGS)
        randomidx = random.randint(0, len(data[randomtag]["children"]) - 1)
        quoteobj = data[randomtag]["children"][randomidx]
        while quoteobj["used"]:
            randomidx = random.randint(0, len(data[randomtag]["children"]) - 1)
            quoteobj = data[randomtag]["children"][randomidx]
        data[randomtag]["children"][randomidx]["used"] = True
        qfp.seek(0)
        qfp.write(json.dumps(data,sort_keys=True, indent=4))
        qfp.truncate()
        return quoteobj


def get_random_bg(bgdir):
    bg_options = os.listdir(bgdir)
    return os.path.join(bgdir, random.choice(bg_options))
