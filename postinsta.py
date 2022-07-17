#!/usr/bin/env python

from instabot import Bot
from config import USERNAME, PASS, IG_TAGS
from utils import convert_img_insta


def main():
    bot = Bot()
    photo = "quote.png"
    new_img = "/tmp/new_img.jpeg"
    convert_img_insta(photo).save(new_img)
    caption = f""".
.
.
.
Follow @d_d_ead.py for more. Turn on the post notification.
{IG_TAGS}"""
    bot.login(username=USERNAME, password=PASS)
    bot.upload_photo(new_img, caption=caption)


main()
