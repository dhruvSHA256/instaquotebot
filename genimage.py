#!/usr/bin/env python

from typing import overload
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
import os
import json
import math
import random
from config import TAGS,BGDIR,QUOTEFILE


def recommend_font_size(text):
    size = 50
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




with open(QUOTEFILE, "r+") as qfp:
    data = json.load(qfp)
    randomtag = random.choice(TAGS)
    randomidx = random.randint(0, len(data[randomtag]["children"]) - 1)
    quoteobj = data[randomtag]["children"][randomidx]
    while quoteobj["used"]:
        randomidx = random.randint(0, len(data[randomtag]["children"]) - 1)
        quoteobj = data[randomtag]["children"][randomidx]
    data[randomtag]["children"][randomidx]["used"] = True
    quote = quoteobj["text"]
    author = quoteobj["author"]
    qfp.seek(0)
    qfp.write(json.dumps(data))
    qfp.truncate()

text = quote

FONT = "fonts/JosefinSans-Bold.ttf"
FONT_SIZE = recommend_font_size(text)

bg_options = os.listdir(BGDIR)
background_img = os.path.join(BGDIR, random.choice(bg_options))

bgimg = Image.open(background_img)
bgimg = bgimg.convert("RGBA")
bgimg_width = bgimg.size[0]
bgimg_height = bgimg.size[1]
maxsize = (math.ceil(0.80 * bgimg_height), bgimg_height)
bgimg = bgimg.resize(maxsize, Image.Resampling.NEAREST)


IMAGE_WIDTH = bgimg.size[0]
IMAGE_HEIGHT = bgimg.size[1]
bgimg.convert("RGBA")

padding = int((IMAGE_WIDTH / 100) * 5)

overlay = Image.new("RGBA", (IMAGE_WIDTH, IMAGE_HEIGHT), (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay, "RGBA")
draw.rectangle(
    (
        (padding, padding),
        (
            IMAGE_WIDTH - padding,
            IMAGE_HEIGHT - padding,
        ),
    ),
    fill=(62, 59, 56, 170),
)
bgimg = Image.alpha_composite(bgimg, overlay)

img_w, img_h = bgimg.size
bg_w, bg_h = bgimg.size
offset = (int((bg_w - img_w) / 2), int((bg_h - img_h) / 2))

text = wrap_text(text)
img = Image.new(
    "RGBA",
    (IMAGE_WIDTH, IMAGE_HEIGHT),
    (0, 0, 0, 0),
)
img.paste(bgimg, offset)


text
font = ImageFont.truetype(FONT, FONT_SIZE)
draw = ImageDraw.Draw(img)
img_w, img_h = img.size
x = img_w / 2
y = img_h / 2
IF = ImageFont.truetype(FONT, FONT_SIZE)
COLOR = (255, 255, 255)
SPACING = 6
textsize = draw.multiline_textsize(text, font=IF, spacing=SPACING)
text_w, text_h = textsize
x -= text_w / 2
y -= text_h / 2
draw.multiline_text(
    align="center",
    xy=(x, y),
    text=text,
    fill=COLOR,
    font=font,
    spacing=SPACING,
)

authortextsize = draw.multiline_textsize(author, font=IF, spacing=SPACING)
authortext_w, authortext_h = authortextsize
authortextoffset = (
    int((IMAGE_WIDTH - authortext_w) / 2),
    IMAGE_HEIGHT - 4 * padding,
)

# IMAGE_HEIGHT - padding - authortext_h - 20,
draw.multiline_text(
    align="center",
    xy=authortextoffset,
    text=author,
    fill=COLOR,
    font=font,
    spacing=SPACING,
)
img.save("quote.png", "PNG")

# img = Image.open(photo)
# img_width = img.size[0]
# img_height = img.size[1]
# # ratio = 4:5 = .80; width/height = .80; width = .80 * height
# maxsize = (math.ceil(0.80 * img_height), img_height)
# img = img.resize(maxsize, Image.Resampling.NEAREST)
# img = img.convert("RGB")
# img.save(new_img)
