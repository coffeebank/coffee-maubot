import asyncio
import aiohttp
import datetime
import json
import re

from .animemanga_utils_anilist import *

def embed_new_line(contents):
    return f"> {str(contents)}\n"

def embed_new_field(name="", value="", inline=None):
    if name:
        return f"> **{str(name)}:** {str(value)}\n"
    else:
        return embed_new_line(value)

def matrix_description_parser(description, max_description_length: int = 500):
    if description is None:
        return None
    description = clean_spoilers(description)
    description = clean_html(description)
    description = description.replace("\n", " ")
    if len(description) > max_description_length:
        return description[:max_description_length] + "..."
    else:
        return description

async def matrix_anilist_embeds(format: str, title: str, number_of_results: int, max_description_length: int):
    cmd = "MANGA"
    if format in ["anime", "Anime", "ANIME"]:
        cmd = "ANIME"

    embed_data, data = await search_anime_manga(cmd, title, isDiscord=False)

    if len(embed_data) <= 0:
        return await evt.respond("No results found")

    embed_data_limit = embed_data[:number_of_results]
    embeds = ""

    for am in embed_data_limit:
        embed = embed_new_line(f"### [{am['title']}]({am['link']})")
        embed += embed_new_line(matrix_description_parser(am["description"], max_description_length))

        if am["info"]:
            embed += embed_new_field(name=str(am["info_status"]), value=matrix_description_parser(am["info"]), inline=True)
        if am["studios"]:
            embed += embed_new_field(name="Studios", value=am["studios"], inline=True)
        if am["external_links"]:
            embed += embed_new_field(name="Links", value=am["external_links"], inline=True)
        if am["names"]:
            embed += embed_new_field(name="Names", value=matrix_description_parser(', '.join(am["names"])), inline=True)
        if cmd == "ANIME":
            embed += embed_new_field(value="###### "+" ・ ".join(filter(None, [am["info_format"], am["time_left"], "Powered by Anilist"])))
        else:
            embed += embed_new_field(value="###### "+" ・ ".join(filter(None, [am["info_format"], "Powered by Anilist"])))

        embed += "\n\n"
        embeds += embed
    return embeds
