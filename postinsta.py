#!/usr/bin/env python

from instabot import Bot
import math
from PIL import Image
from config import USERNAME, PASS, IG_TAGS
from utils import convert_img_insta

bot = Bot()
bot.login(username=USERNAME, password=PASS)


photo = "quote.png"
new_img = "/tmp/new_img.jpeg"

img = Image.open(photo)
img = convert_img_insta(img)
img.save(new_img)

caption = f"\n\n....{IG_TAGS}"

bot.upload_photo(
    new_img,
    caption=caption,
)
