import mautrix.api
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
        count = 0
        for _, url_str in matches:
          if count >= MAX_LINKS:
            break

          appid = self.config["appid"]
          url_params = urllib.parse.urlencode({"i": url_str, "appid": appid})
          embed_content =  "https://matrix.org/_matrix/media/r0/preview_url?url={}".format(url_str)
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
          
          if cont.get('og:image', False) is not False:
            try:
              mauApi = mautrix.api.HTTPAPI('https://matrix.org')
              # download_type='thumbnail' doesn't work because it requires width/height params, but they don't do anything?
              embed_img = str(mauApi.get_download_url(cont.get('og:image', False)))
              # embed_img = str(mauApi.get_download_url(cont.get('og:image', False), download_type='thumbnail')) + "?width=50&height=50"
            except Exception as e:
              print(e)
              embed_img = url_str
            finally:
              msgs += "\n> ### ![[Click to view image >]({})](".format(url_str) + str(embed_img) + ")\n\n"
          
          # implement MAX_LINKS
          count += 1

        if count <= 0:
          await evt.react("💨")
          return
        await evt.reply(str(msgs), allow_html=True)
