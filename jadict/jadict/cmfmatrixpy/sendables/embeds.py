from typing import Any, Dict, List, Mapping, Optional

from ..embeds import Embed
from ..formatter import to_html_markdown_links

class SendableEmbed:
    """Embed formatter for Matrix"""

    def to_sendable(embed: Embed):
        """Converts this embed object into a sendable object, in formatted HTML text."""
        embed_json = embed.to_dict()
        sendables = [
            SendableEmbed.format_embed_author(embed_json),
            SendableEmbed.format_embed_title(embed_json),
            SendableEmbed.format_embed_thumbnail(embed_json),
            SendableEmbed.format_embed_description(embed_json),
            SendableEmbed.format_embed_fields(embed_json),
            SendableEmbed.format_embed_image(embed_json),
            SendableEmbed.format_embed_footer(embed_json)
        ]
        return f"""<blockquote>{"".join(filter(None, sendables))}</blockquote>"""

    def format_embed_title(embed: Mapping[str, Any], title_only=False):
        if embed.get('title') and title_only is False and embed.get('url'):
            return SendableEmbed.format_embed_url(embed, body=SendableEmbed.format_embed_title(embed, title_only=True))
        elif embed.get('title'):
            return f"""<h3>{embed.get('title')}</h3>"""
        else:
            return None

    def format_embed_url(embed: Mapping[str, Any], url: str=None, body=None):
        if url and body:
            return f"""<a href="{url}">{body}</a>"""
        elif url and not body:
            return f"""<a href="{url}">{url}</a>"""
        elif embed.get('url') and body:
            return f"""<a href="{embed.get('url')}">{body}</a>"""
        elif embed.get('url'):
            return f"""<a href="{embed.get('url')}">{embed.get('url')}</a>"""
        else:
            return None

    def format_embed_description(embed: Mapping[str, Any]):
        if embed.get('description'):
            return f"""<p>{to_html_markdown_links(embed.get('description', ''))}</p>"""
        else:
            return None

    def format_embed_colour(embed: Mapping[str, Any]):
        return None

    def format_embed_fields(embed: Mapping[str, Any]):
        sendables = []
        for field in embed.get('fields', []):
            if field.get('inline', True):
                sendables.append(f"""<blockquote><b>{field.get('name', '')}:</b> {to_html_markdown_links(field.get('value', ''))}</blockquote>""")
            else:
                sendables.append(f"""<blockquote><b>{field.get('name', '')}</b><br />{to_html_markdown_links(field.get('value', ''))}</blockquote>""")
        return ''.join(sendables)

    def format_embed_timestamp(embed: Mapping[str, Any]):
        return None

    def format_embed_author(embed: Mapping[str, Any], author_only=False):
        author = embed.get('author', {})
        if author_only is False and author.get('url') and author.get('name'):
            return f"""<sup>{SendableEmbed.format_embed_url(embed, url=author.get('url'), body=author.get('name', ''))}</sup>"""
        elif author_only is False and author.get('url'):
            return f"""<sup>{SendableEmbed.format_embed_url(embed, url=author.get('url'), body=author.get('url', ''))}</sup>"""
        elif author.get('name'):
            return f"""<sup>{name}</sup>"""
        return None

    def format_embed_thumbnail(embed: Mapping[str, Any], width: int=100):
        thumbnail = embed.get('thumbnail', {})
        if thumbnail.get('url') and thumbnail.get('width'):
            return f"""<img src="{thumbnail.get('url')}" width="{str(thumbnail.get('width'))}" />"""
        elif thumbnail.get('url'):
            return f"""<img src="{thumbnail.get('url')}" width="{str(width)}" />"""
        return None

    def format_embed_footer(embed: Mapping[str, Any]):
        footer = embed.get('footer', {})
        if footer.get('text'):
            return f"""<br /><b><sub>{footer.get('text', '')}</sub></b>"""
        return None

    def format_embed_image(embed: Mapping[str, Any], width: int=300):
        image = embed.get('image', {})
        if image.get('url') and image.get('width'):
            return f"""<img src="{image.get('url')}" width="{str(image.get('width'))}" />"""
        elif image.get('url'):
            return f"""<img src="{image.get('url')}" width="{str(width)}" />"""
        return None

    def format_embed_provider(embed: Mapping[str, Any]):
        return None

    def format_embed_video(embed: Mapping[str, Any]):
        return None
