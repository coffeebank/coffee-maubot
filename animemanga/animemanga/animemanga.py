from mautrix.util.config import BaseProxyConfig, ConfigUpdateHelper
from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import List, Type, Optional

from .cmfmatrixpy import SendableEmbed, SendableMenuCollapsible, maubot_parse_embed_images
from .coffeeani_maubot import *
from .coffeeani_utils import *

import logging
logger = logging.getLogger(__name__)

class Config(BaseProxyConfig):
    def do_update(self, helper: ConfigUpdateHelper) -> None:
        helper.copy("results")
        helper.copy("max_description_length")
        helper.copy("deepl_api")

class AnimeMangaBot(Plugin):
    async def start(self) -> None:
        await super().start()
        self.config.load_and_update()

    @classmethod
    def get_config_class(cls) -> Type[BaseProxyConfig]:
        return Config

    @command.new("anime", help="Search for anime, animations, and donghua")
    @command.argument("title", pass_raw=True)
    async def animemanga_anime(self, evt: MessageEvent, title: str) -> None:
        await evt.mark_read()
        number_of_results = self.config.get("results", 0)
        await self.client.set_typing(evt.room_id, timeout=0)
        embeds = await maubot_anilist_embeds(evt, "ANIME", title)
        if embeds:
            if number_of_results > 0:
                embeds = embeds[:number_of_results]
            embeds_after_mxc = [await maubot_parse_embed_images(self, em.get('embed', None)) for em in embeds]
            sendables = [SendableEmbed.to_sendable(eam) for eam in embeds_after_mxc]
            if number_of_results > 0:
                sendables = sendables[:number_of_results]
            return await evt.respond(SendableMenuCollapsible.to_sendable(sendables), allow_html=True)
        no_results = SendableEmbed.to_sendable(maubot_embed_source(None))
        return await evt.respond(no_results, allow_html=True)

    @command.new("manga", aliases=["manhwa", "manhua", "lightnovel"], help="Search for manga, manhwa, manhua, and light novels. Searches Anilist, MangaDex, and Batoto.")
    @command.argument("title", pass_raw=True)
    async def animemanga_manga(self, evt: MessageEvent, title: str) -> None:
        await evt.mark_read()
        number_of_results = self.config.get("results", 0)
        await self.client.set_typing(evt.room_id, timeout=0)
        # anilist
        embeds = await maubot_anilist_embeds(evt, "MANGA", title)
        if embeds:
            if number_of_results > 0:
                embeds = embeds[:number_of_results]
            embeds_after_mxc = [await maubot_parse_embed_images(self, em.get('embed', None)) for em in embeds]
            sendables = [SendableEmbed.to_sendable(eam) for eam in embeds_after_mxc]
            if number_of_results > 0:
                sendables = sendables[:number_of_results]
            return await evt.respond(SendableMenuCollapsible.to_sendable(sendables), allow_html=True)
        # mangadex
        embeds = await maubot_mangadex_embeds(title)
        if embeds:
            if number_of_results > 0:
                embeds = embeds[:number_of_results]
            embeds_after_mxc = [await maubot_parse_embed_images(self, em.get('embed', None)) for em in embeds]
            sendables = [SendableEmbed.to_sendable(eam) for eam in embeds_after_mxc]
            if number_of_results > 0:
                sendables = sendables[:number_of_results]
            return await evt.respond(SendableMenuCollapsible.to_sendable(sendables), allow_html=True)
        # batoto
        embeds = await maubot_batoto_embeds(title)
        if embeds:
            if number_of_results > 0:
                embeds = embeds[:number_of_results]
            embeds_after_mxc = [await maubot_parse_embed_images(self, em.get('embed', None)) for em in embeds]
            sendables = [SendableEmbed.to_sendable(eam) for eam in embeds_after_mxc]
            if number_of_results > 0:
                sendables = sendables[:number_of_results]
            return await evt.respond(SendableMenuCollapsible.to_sendable(sendables), allow_html=True)
        # no results
        no_results = SendableEmbed.to_sendable(maubot_embed_source(None))
        return await evt.respond(no_results, allow_html=True)

    @command.new("bangumi", aliases=["番组", "番組", "番组计划", "番組計劃"], help="Search for donghua, manhua, and anime/manga/manhwa")
    @command.argument("type")
    @command.argument("title", pass_raw=True)
    async def bangumi(self, evt: MessageEvent, type: str, title: str) -> None:
        await evt.mark_read()
        number_of_results = self.config.get("results", 0)
        await self.client.set_typing(evt.room_id, timeout=0)
        bangumi_type = {
            "anime": "anime",
            "donghua": "anime",
            "动画": "anime",
            "動畫": "anime",
            "アニメ": "anime",
            "あにめ": "anime",
            "manga": "manga",
            "manhua": "manga",
            "漫画": "manga",
            "漫畫": "manga",
            "manhwa": "manga",
            "만화": "manga",
        }
        embeds = await maubot_bangumi_embeds(bangumi_type.get(type, "anime"), title)
        if embeds:
            if number_of_results > 0:
                embeds = embeds[:number_of_results]
            embeds_after_mxc = [await maubot_parse_embed_images(self, em.get('embed', None)) for em in embeds]
            sendables = [SendableEmbed.to_sendable(eam) for eam in embeds_after_mxc]
            if number_of_results > 0:
                sendables = sendables[:number_of_results]
            return await evt.respond(SendableMenuCollapsible.to_sendable(sendables), allow_html=True)
        no_results = SendableEmbed.to_sendable(maubot_embed_source(None))
        return await evt.respond(no_results, allow_html=True)
