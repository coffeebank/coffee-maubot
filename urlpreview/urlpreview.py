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

        await evt.mark_read()
        msgs = ""
        images = []
        count = 0
        for _, url_str in matches:
          if count >= MAX_LINKS:
            break

          url_params = urllib.parse.urlencode({"i": url_str, "appid": appid})
          embed_content =  "https://{}/_matrix/media/r0/preview_url?url={}".format(HOMESERVER, url_str)
          resp = await self.http.get(embed_content, headers={"Authorization":"Bearer {}".format(appid)})

          # Guard clause
          if resp.status != 200:
            continue
          cont = json.loads(await resp.read())

          # Set empty if no og:description
          if cont.get('og:description', None) == None:
            embed_desc = ""
          else:
            embed_desc = str(cont.get('og:description', '')).replace('\r', ' ').replace('\n', ' ')

          # If there is an og:title use this
          if cont.get('og:title', False) is not False:
            msgs += "> "+str(cont.get('og:site-title', ''))+"\n> ### ["+str(cont.get('og:title', ''))+"]("+str(url_str)+")\n> "+str(embed_desc)
          # If there is not an og:title, but there is an image, use this
          elif cont.get('og:title', True) and cont['og:image']:
            msgs += "> "+str(cont.get('og:site-title', ''))+"\n> "+str(embed_desc)
          
          if cont.get('og:image', None):
            if cont.get('og:image:width', None) and cont.get('og:image:width') > MIN_IMAGE_WIDTH:
              images.append(cont)

          msgs += "\n\n" # Add line breaks
          count += 1 # Implement MAX_LINKS

        if count <= 0:
          await evt.react("💨")
          return
        await evt.reply(str(msgs), allow_html=True)

        # Send images after text
        for img in images:
          await self.client.send_file(
            evt.room_id,
            url=img.get('og:image', None),
            info=BaseFileInfo(mimetype=img.get('og:image:type', None)),
            file_name=str(url_str),
            file_type=MessageType.IMAGE
          )
