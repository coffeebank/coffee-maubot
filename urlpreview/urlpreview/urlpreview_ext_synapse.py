import mautrix.api
from mautrix.types import RoomID, ImageInfo, MessageType
from mautrix.types.event.message import BaseFileInfo, Format, TextMessageEventContent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command

import json
from typing import List, Type
import urllib.parse
from urllib.parse import urlparse

from .urlpreview_utils import check_image_content_type, check_line_breaks

async def fetch_synapse(self, url_str, appid, homeserver, html_custom_headers, **kwargs):
    # No API key
    if appid in ["BOT_ACCESS_TOKEN", None]:
        return None
    if not homeserver:
        return None
    if not url_str:
        return None

    url_encoded = urllib.parse.quote(str(url_str), safe="")
    embed_content = f"https://{homeserver}/_matrix/media/r0/preview_url?url={url_encoded}"
    try:
        resp = await self.http.get(embed_content, headers={"Authorization": "Bearer {}".format(appid)})
    except Exception as err:
        self.log.exception(f"[urlpreview] [ext_synapse] Error: {str(err)} - {str(urlparse(url_str).netloc)}")
        return None

    # Guard clause
    if resp.status != 200:
        self.log.exception(f"[urlpreview] [ext_synapse] Error: resp.status {str(resp.status)} - {str(urlparse(url_str).netloc)} - {str(resp)}")
        return None

    cont = json.loads(await resp.read())
    final_og = {
        "title": synapse_format_title(cont),
        "description": check_line_breaks(synapse_format_description(cont)),
        "image": synapse_format_image(cont),
        "image_mxc": synapse_format_image(cont),
        "content_type": (await synapse_format_content_type(self, cont, html_custom_headers)),
        "image_width": cont.get('og:image:width', None),
    }
    self.log.debug(f"[urlpreview] [ext_synapse] fetch_synapse {str(final_og)}")
    return final_og

def synapse_format_title(cont):
    if cont.get('og:title', None):
        return cont.get('og:title', None)
    if cont.get('og:site-title', None):
        return cont.get('og:site-title', None)
    if cont.get('og:site_name', None):
        return cont.get('og:site_name', None)
    if cont.get('title', None):
        return cont.get('title', None)
    return None

def synapse_format_description(cont):
    if cont.get('og:description', None):
        return cont.get('og:description', None)
    if cont.get('description', None):
        return cont.get('description', None)
    return None

def synapse_format_image(cont):
    if cont.get('twitter:image', None):
        return cont.get('twitter:image', None)
    if cont.get('og:image', None):
        return cont.get('og:image', None)
    return None

async def synapse_format_content_type(self, cont, html_custom_headers=None):
    if cont.get('og:image:type', None):
        return cont.get('og:image:type', None)
    content_type = await check_image_content_type(self, synapse_format_image(cont), html_custom_headers=html_custom_headers)
    return content_type
