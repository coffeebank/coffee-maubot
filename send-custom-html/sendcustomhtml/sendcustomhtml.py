from maubot import Plugin, MessageEvent
from maubot.handlers import command
from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from typing import Type
import asyncio
import json

from .cmfmatrixpy import Embed, SendableEmbed, SendableMenuCollapsible, maubot_parse_embed_images

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

    @command.new("sendcustomembed", help="Have the bot send an embed, formatted in Discord Embed JSON.")
    @command.argument("json_text", pass_raw=True)
    async def sendcustomembed(self, evt: MessageEvent, json_text: str) -> None:
        whitelist = self.config["whitelist"]
        if (evt.sender not in whitelist):
            return
        embed_json = json.loads(str(json_text))
        embed_obj = Embed.from_dict(embed_json)
        embed_obj_mxc = await maubot_parse_embed_images(self, embed_obj)
        sendable = SendableEmbed.to_sendable(embed_obj_mxc)
        await evt.respond(sendable, allow_html=True)

    @command.new("sendcustommenucollapsible", help="Have the bot send a collapsible menu.")
    @command.argument("pages", pass_raw=True)
    async def sendcustommenucollapsible(self, evt: MessageEvent, pages: str) -> None:
        whitelist = self.config["whitelist"]
        if (evt.sender not in whitelist):
            return
        pages_arr = json.loads(str(pages))
        sendable = SendableMenuCollapsible.to_sendable(pages_arr)
        await evt.respond(str(sendable), allow_html=True)
