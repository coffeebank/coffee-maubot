from ..embeds import Embed
from .fetch import maubot_fetch_image

async def maubot_parse_embed_images(self, embed: Embed):
    image = embed.image
    if image.url:
        mxc_image = await maubot_fetch_image(self, image.url)
        embed.set_image(url=mxc_image)
    thumbnail = embed.thumbnail
    if thumbnail.url:
        mxc_thumbnail = await maubot_fetch_image(self, thumbnail.url)
        embed.set_thumbnail(url=mxc_thumbnail)
    return embed
