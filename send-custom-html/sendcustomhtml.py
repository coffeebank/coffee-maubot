from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from typing import Type
import asyncio

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("whitelist")

class SendCustomHtmlBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.new("sendcustomhtml", help="Have the bot send a message as custom HTML.")
    @command.argument("html", pass_raw=True)
    async def sendcustomhtml(self, evt: MessageEvent, html: str) -> None:
        whitelist = self.config["whitelist"]
        if (evt.sender not in whitelist):
            return
        await evt.reply(html, allow_html=True)
