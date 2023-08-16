from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import List, Type, Optional

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
            senses = []
            for sense in jisho_results["senses"]:
                senses.append(f"**{sense['name']}**: {sense['value']}")
            result = [
                f"### [{jisho_results['title']}]({jisho_results['url']})",
                f"{jisho_results['description']}",
                "\u2002\n".join(senses),
            ]
            sendEmbeds.append("\u2002\n".join(result))
        return sendEmbeds[:number_of_results]



    # Bot Commands

    @command.new("jadict", aliases=["jisho"], help="Search Japanese dictionary. By default, searches using Japanese and Romaji. When searching in English, please use  \"quotes\"")
    @command.argument("text", pass_raw=True)
    async def jadict_jadict(self, evt: MessageEvent, text: str) -> None:
        jishoJson = await fetchJisho(text)

        if jishoJson not in [False, None]:
            jisho_results = make_results(jishoJson)
            sendEmbeds = self.jishoResultsEmbeds(jisho_results)
            sendEmbeds.append("###### Results from [Jisho API and others](https://jisho.org/about)")
            await evt.respond("\n".join(sendEmbeds))
        else:
            return await evt.respond("No results found....")
