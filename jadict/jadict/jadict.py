from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import List, Type, Optional

from .cmfmatrixpy import Embed, SendableEmbed, SendableMenuCollapsible
from .jadict_utils import *

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("results")

class JadictBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config


    # Utility Commands

    def jishoResultsEmbeds(self, jishoResult):
        number_of_results = self.config["results"]
        sendEmbeds = []
        for idx, jisho_results in enumerate(jishoResult):
            em = Embed(
                title=jisho_results.get('title', '-'),
                url=jisho_results.get('url', None),
                description=jisho_results.get('description')
            )
            for sense in jisho_results.get('senses'):
                em.add_field(
                    name=sense.get('name'),
                    value=sense.get('value')
                )
            em.set_footer(
                text="Results from Jisho API"
            )
            sendEmbeds.append(SendableEmbed.to_sendable(em))
        sendable = SendableMenuCollapsible.to_sendable(sendEmbeds[:number_of_results])
        return sendable



    # Bot Commands

    @command.new("jadict", aliases=["jisho"], help="Search Japanese dictionary. By default, searches using Japanese and Romaji. When searching in English, please use  \"quotes\"")
    @command.argument("text", pass_raw=True)
    async def jadict_jadict(self, evt: MessageEvent, text: str) -> None:
        await evt.mark_read()
        await self.client.set_typing(evt.room_id, timeout=0)
        jishoJson = await fetchJisho(text)

        if jishoJson not in [False, None]:
            jisho_results = make_results(jishoJson)
            sendEmbeds = self.jishoResultsEmbeds(jisho_results)
            await evt.respond(sendEmbeds, allow_html=True)
        else:
            return await evt.respond("No results found....")
