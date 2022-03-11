from mautrix.api import HTTPAPI
from mautrix.types import RoomID, ImageInfo
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
import json
from typing import List, Type
import urllib.parse

MAX_LINKS = 3

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("appid")

class UrlpreviewBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.passive("(https:\/\/[\S]+)", multiple=True)
    async def handler(self, evt: MessageEvent, matches: List[str]) -> None:
        await evt.mark_read()
        msgs = ""
        for _, url_str in matches:
          if len(msgs) >= MAX_LINKS:
            msgs.append("...")
            break

          appid = self.config["appid"]
          url_params = urllib.parse.urlencode({"i": url_str, "appid": appid})
          embed_content =  "https://matrix-client.matrix.org/_matrix/media/r0/preview_url?url={}".format(url_str)
          resp = await self.http.get(embed_content, headers={"Authorization":"Bearer {}".format(appid)})
          if resp.status == 500:
            await evt.reply("Hmmmm")
            return None
          if resp.status != 200:
            self.log.warning(f"Error: {resp.status}")
            return None
          cont = json.loads(await resp.read())

          if cont.get('og:description', None) == None:
            embed_desc = ""
          else:
            embed_desc = cont.get('og:description', '')

          if cont.get('og:title', False):
            msgs += "> "+str(cont.get('og:site-title', ''))+"\n> ### ["+str(cont.get('og:title', ''))+"]("+str(url_str)+")\n> "+str(embed_desc)
          elif cont.get('og:title', True) and cont['og:image']:
            msgs += "> "+str(cont.get('og:site-title', ''))+"\n> "+str(embed_desc)
          
          if cont.get('og:image', False):
            try:
              embed_img = HTTPAPI.get_download_url(cont.get('og:image', ''))
            except TypeError:
              embed_img = url_str
            msgs += "\n> ### ![[Click to view image >]({})](".format(url_str) + str(embed_img)+")\n"

        if len(msgs) == 0:
            return
        await evt.reply(str(msgs), allow_html=True)
