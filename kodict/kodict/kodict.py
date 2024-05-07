from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import List, Type, Optional

import kodict_core
from .cmfmatrixpy import SendableEmbed, SendableMenuCollapsible
from .kodict_utils import embed_krdict, embed_deepl, embed_fallback

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("krdict_api")
        helper.copy("deepl_api")
        helper.copy("results")

class KodictBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config


    # Utility Commands

    def noneStrings(entry):
        if entry == "":
            return None
        return entry

    async def kodictResultsEmbed(self, results, result_count: int=3):
        sendables = []
        for result in results:
            sendable_embed = SendableEmbed.to_sendable(result)
            sendables.append(sendable_embed)
        sendable_menu = SendableMenuCollapsible.to_sendable(sendables[:result_count])
        return sendable_menu


    # Bot Commands

    @command.new("kodict", aliases=["krdict"], help="Search Korean dictionary. Search National Institute of Korean Language's Korean-English Learners' Dictionary.")
    @command.argument("text", pass_raw=True)
    async def kodict_kodict(self, evt: MessageEvent, text: str) -> None:
        KRDICT_API = self.config["krdict_api"]
        if not KRDICT_API:
            KRDICT_API = None
        DEEPL_API = self.config["deepl_api"]
        if not DEEPL_API:
            DEEPL_API = None
        RESULTS = self.config["results"]
        await evt.mark_read()
        await self.client.set_typing(evt.room_id, timeout=0)

        results = await kodict_core.fetch_all(text, KRDICT_API, DEEPL_API)
        if results.get("krdict", None):
            attribution = ["Krdict (한국어기초사전)"]
            if results.get("deepl", None):
                attribution.append("DeepL")
            send_embeds = await embed_krdict(results.get("krdict"), attribution)
            sendables = await self.kodictResultsEmbed(send_embeds)
            return await evt.respond(sendables, allow_html=True)
        elif results.get("deepl", None):
            deepl_embed = await embed_deepl(text, results.get("deepl"), None)
            sendable = SendableEmbed.to_sendable(deepl_embed)
            return await evt.respond(sendable, allow_html=True)
        else:
            fallback_embed = await embed_fallback(text, None, "No results from Krdict API.")
            sendable = SendableEmbed.to_sendable(fallback_embed)
            return await evt.respond(sendable, allow_html=True)
