from html.parser import HTMLParser
import json
from typing import List, Type
import urllib.parse

from .urlpreview_utils import *

async def fetch_htmlparser(
    self,
    url_str: str,
    *args
):
    try:
        resp = await self.http.get(url_str)
    except Exception as err:
        self.log.exception(f"[urlpreview] [ext_htmlparser] Error: {str(err)} - {str(urlparse(url_str).netloc)}")

    # Guard clause
    if resp.status != 200:
        self.log.exception(f"[urlpreview] [ext_htmlparser] Error: {str(urlparse(url_str).netloc)} returned status {str(resp.status)}")
        return None

    # Images
    if resp.content_type in IMAGE_TYPES:
        return {
            "title": None,
            "description": None,
            "image": url_str,
            "content_type": resp.content_type,
        }

    # HTML
    parser = ExtractMetaTags()
    cont = await resp.text()
    parser.feed(cont)
    parser.og["content_type"] = await check_image_content_type(self, parser.og["image"])
    self.log.debug("fetch_htmlparser "+str(parser.og))
    return parser.og

def fetch_meta_content(attrs, attr_to_find):
    # <meta property="" content="" />
    for attr, value in attrs:
        if attr in ["property", "name"] and value == attr_to_find:
            for attr_2, value_2 in attrs:
                if attr_2 == "content":
                    return str(value_2)
    return None

class ExtractMetaTags(HTMLParser):
    og = {
        "title": None,
        "description": None,
        "image": None,
        "content_type": None,
    }

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            title = fetch_meta_content(attrs, "og:title")
            if title is None:
                title = fetch_meta_content(attrs, "og:site-title")
            if title is not None:
                self.og["title"] = title

            description = fetch_meta_content(attrs, "og:description")
            if description is None:
                description = fetch_meta_content(attrs, "description")
            if description is not None:
                self.og["description"] = description

            image = fetch_meta_content(attrs, "twitter:image")
            if image is None:
                image = fetch_meta_content(attrs, "og:image")
            if image is not None:
                self.og["image"] = image
