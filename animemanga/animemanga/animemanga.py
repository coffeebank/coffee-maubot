from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import List, Type, Optional

from .animemanga_utils_anilist import *
from .animemanga_utils_matrix import *

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("results")
        helper.copy("max_description_length")

class AnimeMangaBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.new("anime", help="Searches for anime using Anilist")
    @command.argument("title", pass_raw=True)
    async def animemanga_anime(self, evt: MessageEvent, title: str) -> None:
        number_of_results = self.config["results"]
        max_description_length = self.config["max_description_length"]
        to_send = await matrix_anilist_embeds(self, "ANIME", title, number_of_results, max_description_length)
        await evt.respond(to_send, allow_html=True)

    @command.new("manga", aliases=["manhwa", "manhua", "lightnovel", "漫画", "漫画", "만화"], help="Searches for manga/manhwa/manhua and light novels using Anilist")
    @command.argument("title", pass_raw=True)
    async def animemanga_manga(self, evt: MessageEvent, title: str) -> None:
        number_of_results = self.config["results"]
        max_description_length = self.config["max_description_length"]
        to_send = await matrix_anilist_embeds(self, "MANGA", title, number_of_results, max_description_length)
        await evt.respond(to_send, allow_html=True)
