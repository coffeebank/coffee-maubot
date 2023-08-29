import mautrix.api
from mautrix.types import RoomID, ImageInfo, MessageType
from mautrix.types.event.message import BaseFileInfo, Format, TextMessageEventContent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command

import urllib.parse
from urllib.parse import urlparse

from .urlpreview_utils import *
from .urlpreview_ext_htmlparser import *
from .urlpreview_ext_synapse import *

EXT_ENABLED = ["synapse", "htmlparser"]
EXT_ARR = {
  "htmlparser": fetch_htmlparser,
  "synapse": fetch_synapse
}

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("appid")
        helper.copy("homeserver")
        helper.copy("max_links")
        helper.copy("min_image_width")
        helper.copy("max_image_embed")
        helper.copy("no_results_react")
        helper.copy("url_blacklist")
        helper.copy("user_blacklist")

async def fetch_all(self, url_str, appid: str='', homeserver: str='matrix-client.matrix.org'):
    final_og = {}
    for ext in EXT_ENABLED:
        try:
            fetch_ext = EXT_ARR.get(ext, None)
            og_resp = await fetch_ext(self, url_str, appid, homeserver)
            if og_resp:
                final_og.update({k:v for (k,v) in og_resp.items() if v})
        except Exception as err:
            self.log.exception(f"[urlpreview] [utils] Error fetch_all fetch_ext: {err}")
    return final_og

async def embed_url_preview(self, url_str, og, max_image_embed: int=300):
    # Check if None
    if not og:
        return None
    if all(v is None for v in og):
        return None

    image_mxc = await process_image(self, og.get('image', None), og.get('content_type', None))

    # Only contains image
    if check_all_none_except(og, ['image', 'content_type']):
        image_solo = format_image(image_mxc, url_str, og.get('content_type', None), max_image_embed=0) # Full size image
        if image_solo is not None:
            return f"<blockquote>{image_solo}</blockquote>"
        else:
            return None # Everything is empty

    # Regular message
    title = format_title(og.get('title', None), url_str)
    description = format_description(og.get('description', None))
    image = format_image(image_mxc, url_str, og.get('content_type', None), max_image_embed)
    message = "".join(filter(None, [title, description, image]))

    if message:
        return f"<blockquote>{message}</blockquote>"
    return None

class UrlPreviewBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    # RFC 3986 excluding: (), []
    @command.passive("(https:\/\/[A-Za-z0-9\-._~:\/?#@!$&'*+,;=%]+)", multiple=True)
    async def handler(self, evt: MessageEvent, matches: List[str]) -> None:
        # Check USER_BLACKLIST
        USER_BLACKLIST = self.config["user_blacklist"]
        if user_check_blacklist(evt.sender, USER_BLACKLIST):
            return

        appid = self.config["appid"]
        MAX_LINKS = self.config["max_links"]
        HOMESERVER = self.config["homeserver"]
        MIN_IMAGE_WIDTH = self.config["min_image_width"]
        MAX_IMAGE_EMBED = self.config["max_image_embed"]
        NO_RESULTS_REACT = self.config["no_results_react"]
        URL_BLACKLIST = self.config["url_blacklist"]
        await evt.mark_read()

        embeds = []
        count = 0
        for _, unsafe_url in matches:
            if count >= MAX_LINKS:
                break
            # Check URL_BLACKLIST
            url_str = url_check_blacklist(unsafe_url, URL_BLACKLIST)
            if url_str is None:
                self.log.exception(f"[urlpreview] WARNING: {evt.sender} tried to access blacklisted IP: {str(unsafe_url)}")
                continue

            og = await fetch_all(self, url_str, appid, HOMESERVER)
            embed = await embed_url_preview(self, url_str, og, MAX_IMAGE_EMBED)
            if embed is not None:
                embeds.append(embed)
                count += 1 # Implement MAX_LINKS

        if len(embeds) <= 0:
            if NO_RESULTS_REACT:
                try:
                    await evt.react(NO_RESULTS_REACT)
                except: # Silently ignore if react doesn't work
                    pass
            return
        to_send = "".join(embeds)
        return await evt.reply(to_send, allow_html=True)
