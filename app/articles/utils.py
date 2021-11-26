from bs4 import BeautifulSoup
import requests
from PIL import Image
import secrets
import os
from flask import current_app


def get_article_html(url):
    source = requests.get(url).text
    soup = BeautifulSoup(source, "lxml")
    title = find_article_title(soup)
    image = find_article_image(soup)
    return title, image


def find_article_title(soup):
    title = soup.find("title")
    return title.text if title else None


def find_article_image(soup):
    images = soup.find_all("img")
    images_urls = []
    for image in images:
        image_src = image.get("src")
        if (
            image_src
            and image_src.startswith("http" or "www")
            and ("jpg" in image_src or "png" in image_src)
        ):
            images_urls.append(image_src)

    if not images_urls:
        return None

    if len(images_urls) > 1:
        url = images_urls[1]
    else:
        url = images_urls[0]
    random_hex = secrets.token_hex(8)
    f_ext = ".jpg" if "jpg" in url else ".png"
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(
        current_app.root_path, "static/images/articles", picture_fn
    )
    try:
        img = Image.open(requests.get(url, stream=True).raw)
        img.save(picture_path)
    except:
        return None

    return picture_fn
