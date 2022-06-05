#!/usr/bin/env python

from instabot import Bot
import os
import math
from PIL import Image

USERNAME = os.environ["IGUSERNAME"]
PASS = os.environ["IGPASS"]

# print(USERNAME)
# print(PASS)

bot = Bot()
bot.login(username=USERNAME, password=PASS)


photo = "quote.png"
new_img = "/tmp/new_img.jpeg"

img = Image.open(photo)
img_width = img.size[0]
img_height = img.size[1]
# ratio = 4:5 = .80; width/height = .80; width = .80 * height
maxsize = (math.ceil(0.80 * img_height), img_height)
img = img.resize(maxsize, Image.Resampling.NEAREST)
img = img.convert("RGB")
img.save(new_img)

quote = "I should study instead"
bot.upload_photo(
    new_img,
    caption=quote,
)
