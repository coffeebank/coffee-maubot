import mautrix.api
from mautrix.types import RoomID, ImageInfo, MessageType
from mautrix.types.event.message import BaseFileInfo, Format, TextMessageEventContent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command

from html.parser import HTMLParser
import json
from typing import List, Type
import urllib.parse


class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("max_links")
        helper.copy("max_image_embed")
        helper.copy("no_results_react")

def fetch_meta_content(attrs, attr_to_find):
    # <meta property="" content="" />
    for attr, value in attrs:
        if attr in ["property", "name"] and value == attr_to_find:
            for attr_2, value_2 in attrs:
                if attr_2 == "content":
                    return str(value_2)
    return None

async def matrix_get_image(self, image_url: str, mime_type: str="image/jpeg", filename: str="image.jpg"):
    resp = await self.http.get(image_url)
    if resp.status != 200:
        return None
    og_image = await resp.read()
    mxc = await self.client.upload_media(og_image, mime_type=mime_type, filename=filename)
    return mxc

class ExtractMetaTags(HTMLParser):
    og = {
        "title": None,
        "description": None,
        "image": None,
    }

    def __init__(self):
        HTMLParser.__init__(self)

    def handle_starttag(self, tag, attrs):
        if tag == "meta":
            title = fetch_meta_content(attrs, "og:title")
            if title is None:
                title = fetch_meta_content(attrs, "title")
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

class UrlpreviewBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    # RFC 3986 excluding: (), []
    @command.passive("(https:\/\/[A-Za-z0-9\-._~:\/?#@!$&'*+,;=%]+)", multiple=True)
    async def handler(self, evt: MessageEvent, matches: List[str]) -> None:
        MAX_LINKS = self.config["max_links"]
        MAX_IMAGE_EMBED = self.config["max_image_embed"]
        NO_RESULTS_REACT = self.config["no_results_react"]

        await evt.mark_read()
        msgs = ""
        count = 0
        for _, url_str in matches:
            if count >= MAX_LINKS:
                break
            if count >= MAX_LINKS:
                break

            resp = await self.http.get(url_str)

            # Guard clause
            if resp.status != 200:
                continue
            parser = ExtractMetaTags()
            parser.og = {
                "title": None,
                "description": None,
                "image": None
            }

            # Images
            image_types = ["image/gif", "image/jpg", "image/jpeg", "image/png", "image/webp"]
            if resp.content_type in image_types:
                image_mxc = await matrix_get_image(self, url_str, mime_type=resp.content_type, filename=resp.content_type.replace('/', '.').replace('jpeg', 'jpg'))
                image = f'<a href="{url_str}"><img src="{image_mxc}" alt="{resp.content_type}" /></a>'
                msgs += f"<blockquote>{image}</blockquote>"
                count += 1 # Implement MAX_LINKS
                continue

            # HTML
            cont = await resp.text()
            parser.feed(cont)

            title = parser.og["title"]
            if title:
                title = f'<h3><a href="{url_str}">{title}</a></h3>'

            description = parser.og["description"]
            if description:
                description = '<p>'+str(description).replace('\r', ' ').replace('\n', ' ')+'</p>'

            image = parser.og["image"]
            if image:
                image_mxc = await matrix_get_image(self, image)
                image = f'<a href="{image}"><img src="{image_mxc}" width="{MAX_IMAGE_EMBED}" alt="Banner image" /></a>'

            embed_contents = "".join(filter(None, [title, description, image]))
            if embed_contents:
                msgs += f"<blockquote>{embed_contents}</blockquote>"
                count += 1 # Implement MAX_LINKS

        if count <= 0:
            if NO_RESULTS_REACT:
                try:
                    await evt.react(NO_RESULTS_REACT)
                except: # Silently ignore if react doesn't work
                    pass
            return
        await evt.reply(str(msgs), allow_html=True)
