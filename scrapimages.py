#!/usr/bin/env python
import requests
import os
import re
import json
import xmltodict
from bs4 import BeautifulSoup
import urllib.request
from config import TUMBLR_BLOGS


def scrap_tumblr(blog, num, start):
    url = f"https://{blog}.tumblr.com/api/read?type=photo&num={num}&start={start}"
    response = requests.get(url)
    xml_cleaned = re.sub("[^\x20-\x7f]+", "", response.content.decode("utf-8"))
    data = xmltodict.parse(xml_cleaned)
    with open(f"media/{blog}.json", "w") as json_file:
        json.dump(data, json_file, indent=4, sort_keys=True)
    posts = data["tumblr"]["posts"]["post"]

    def get_url_from_post(post):
        try:
            soupe = BeautifulSoup(post["regular-body"], "html.parser")
            return soupe.find("img")["src"]
        except:
            return None
        # return soupe

    for post in posts:
        try:
            # if post has photoset, walk into photoset for each photo
            photoset = post["photoset"]["photo"]
            for photo in photoset:
                url = get_url_from_post(photo)
                if url:
                    filename = url.split("/")[-1]
                    download_image("media", filename, url)
        except:
            # select the largest resolution
            # usually in the first element
            url = get_url_from_post(post)
            # print(url)
            if url:
                filename = url.split("/")[-1]
                download_image("media", filename, url)


def download_image(path, name, url):
    file_path = os.path.join(path, name)
    print(f"downloading {file_path}")
    if not os.path.isfile(file_path):
        try:
            urllib.request.urlretrieve(url, file_path)
        except Exception as e:
            print("Failed: ", e)


for blog in TUMBLR_BLOGS:
    print(f"Scrapping {blog}")
    scrap_tumblr(blog, 20, 1)

# download_image(
#     "media",
#     "jojo.jpeg",
#     "https://64.media.tumblr.com/55de0d667fa0a26de027d0b69ac8e5e7/4eef33b906bed264-68/s640x960/3f7e17c5bcae6570faa6b439bb3b7a28747ec3b4.jpg",
# )
