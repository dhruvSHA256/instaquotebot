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

caption = "I should study instead but I am literally dead and have no motivation \n\n #academia #achilles #ancientrome #aristotle #bookquotes #books #classicliterature #classics #darkacademiaaesthetic #dostoyevsky #englishliterature #existential #followforfollowback #hopelessromantic #ilubutdoI #lifephilosophy #lifequotes #likeforlikes #literature #mythology #nihilist #philosophical #philosophy #philosophyquotes #plato #poetry #positivityquotes #quotedaily #quotesaboutlife #quotesdaily #quotesindonesia #quotesoftheday #quotestoday #quotetoliveby #romanticism #sad #shakespeare #socrates #stoicism #successquotes #thisisallbullshit #virgil #virgin #wisdom #writersofinstagram"


bot.upload_photo(
    new_img,
    caption=caption,
)
