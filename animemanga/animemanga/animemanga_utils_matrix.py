import asyncio
import aiohttp
import datetime
import json
import re

from .animemanga_utils_anilist import *

def embed_new_tag(contents, tag="p", markdown=True):
    body = contents
    if markdown == True:
        body = embed_markdown(str(contents))
    return f"<{tag}>{body}</{tag}>"

def embed_new_field(name="", value="", inline=None):
    if name:
        return f"<p><b>{str(name)}:</b> {embed_markdown(str(value))}</p>"
    else:
        return embed_new_tag(embed_markdown(value))

def embed_markdown(contents):
    def _markdown_replace_links(match):
        string_part = match.group(1)
        url_part = match.group(2)
        return f'<a href="{url_part}">{string_part}</a>'
    results = contents
    # links
    pattern_links = r'\[([^]]+)\]\((http[^)]+)\)'
    results = re.sub(pattern_links, _markdown_replace_links, results)
    return results.replace("<p>", "").replace("</p>", "")

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

async def matrix_anilist_embeds(self, format: str, title: str, number_of_results: int, max_description_length: int):
    cmd = "MANGA"
    if format in ["anime", "Anime", "ANIME"]:
        cmd = "ANIME"

    embed_data, data = await search_anime_manga(cmd, title, isDiscord=False)

    if len(embed_data) <= 0:
        return await evt.respond("No results found")

    embed_data_limit = embed_data[:number_of_results]
    embeds = ""

    for am in embed_data_limit:
        embed = []
        embed.append(f'<h3><a href="{am["link"]}">{am["title"]}</a></h3>')
        
        if am["description"]:
            embed.append(embed_new_tag(matrix_description_parser(am["description"], max_description_length)))
        if am["info"]:
            embed.append(embed_new_field(name=str(am["info_status"]), value=matrix_description_parser(am["info"]), inline=True))
        if am["studios"]:
            embed.append(embed_new_field(name="Studios", value=am["studios"], inline=True))
        if am["external_links"]:
            embed.append(embed_new_field(name="Links", value=am["external_links"], inline=True))
        if am["names"]:
            embed.append(embed_new_field(name="Names", value=matrix_description_parser(', '.join(am["names"])), inline=True))
        if am["image"]:
            embed.append(f'<img src="{(await matrix_get_image(self, am["image"]))}" width="300" />')

        if cmd == "ANIME":
            embed.append(embed_new_tag(" ・ ".join(filter(None, [am["info_format"], am["time_left"], "Powered by Anilist"])), tag="h6"))
        else:
            embed.append(embed_new_tag(" ・ ".join(filter(None, [am["info_format"], "Powered by Anilist"])), tag="h6"))

        embeds += embed_new_tag("".join(embed), tag="blockquote", markdown=False)
    return embeds

async def matrix_get_image(self, image_url: str):
    resp = await self.http.get(image_url)
    if resp.status != 200:
        return None
    og_image = await resp.read()
    mxc = await self.client.upload_media(og_image, mime_type='image/jpg', filename="image.jpg")
    return mxc
