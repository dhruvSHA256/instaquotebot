#!/usr/bin/env python

from instabot import Bot
import math
from PIL import Image
from config import USERNAME, PASS

bot = Bot()
bot.login(username=USERNAME, password=PASS)


photo = "quote.png"
new_img = "/tmp/new_img.jpeg"


def convert_img_insta(photo, new_img):
    # ratio = 4:5 = .80; width/height = .80; width = .80 * height
    img = Image.open(photo)
    img_width = img.size[0]
    img_height = img.size[1]
    maxsize = (math.ceil(0.80 * img_height), img_height)
    img = img.resize(maxsize, Image.Resampling.NEAREST)
    img = img.convert("RGB")
    img.save(new_img)


convert_img_insta(photo, new_img)

caption = "\n\n.... #academia #ancientrome #aristotle #bookquotes #classicliterature #classics #darkacademiaaesthetic #existential #hopelessromantic #lifequotes #literature #nihilist #philosophy #poetry #quotesdaily #romanticism #sad #shakespeare #socrates #stoicism"

bot.upload_photo(
    new_img,
    caption=caption,
)
