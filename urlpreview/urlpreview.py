import mautrix.api
from mautrix.types import RoomID, ImageInfo, MessageType
from mautrix.types.event.message import BaseFileInfo, Format, TextMessageEventContent
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
import json
from typing import List, Type
import urllib.parse

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("appid")
        helper.copy("homeserver")
        helper.copy("max_links")
        helper.copy("min_image_width")
        helper.copy("max_image_embed")

class UrlpreviewBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.passive("(https:\/\/[\S]+)", multiple=True)
    async def handler(self, evt: MessageEvent, matches: List[str]) -> None:
        appid = self.config["appid"]
        MAX_LINKS = self.config["max_links"]
        HOMESERVER = self.config["homeserver"]
        MIN_IMAGE_WIDTH = self.config["min_image_width"]
        MAX_IMAGE_EMBED = self.config["max_image_embed"]

        await evt.mark_read()
        msgs = ""
        count = 0
        for _, url_str in matches:
          if count >= MAX_LINKS:
            break

          url_params = urllib.parse.urlencode({"i": url_str, "appid": appid})
          embed_content = f"https://{HOMESERVER}/_matrix/media/r0/preview_url?url={url_str}"
          resp = await self.http.get(embed_content, headers={"Authorization":"Bearer {}".format(appid)})

          # Guard clause
          if resp.status != 200:
            continue
          cont = json.loads(await resp.read())

          # embed_site_title = ""
          # if cont.get("og:site-title", None):
          #   embed_site_title = "<em>"+cont.get("og:site-title", "")+"</em>"

          title = None
          if cont.get("og:title", None):
            title = f'<h3><a href="{url_str}">{cont.get("og:title", "")}</a></h3>'
          elif cont.get("og:site-title", None):
            title = f'<h3><a href="{url_str}">{cont.get("og:site-title", "")}</a></h3>'

          description = None
          if cont.get("og:description", None):
            description = '<p>'+str(cont.get('og:description', '')).replace('\r', ' ').replace('\n', ' ')+'</p>'

          image = None
          if cont.get("og:image", None):
            if (MIN_IMAGE_WIDTH <= 0) or (cont.get("og:image:width", None) and cont.get("og:image:width", 0) > MIN_IMAGE_WIDTH):
              mauApi = mautrix.api.HTTPAPI("https://"+HOMESERVER)
              image_url = str(mauApi.get_download_url(cont.get('og:image', None)))
              image = f'<a href="{image_url}"><img src="{cont.get("og:image", None)}" width="{MAX_IMAGE_EMBED}" alt="Banner image" /></a>'

          msgs += "<blockquote>"
          msgs += "".join(filter(None, [title, description, image]))
          msgs += "</blockquote>"
          count += 1 # Implement MAX_LINKS

        if count <= 0:
          await evt.react("💨")
          return
        await evt.reply(str(msgs), allow_html=True)
