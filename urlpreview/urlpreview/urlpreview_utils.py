import ipaddress
import re
import socket
import urllib.parse
import os
import subprocess
from datetime import datetime as dt
import hashlib
from urllib.parse import urlparse

IMAGE_TYPES = ["image/gif", "image/jpg", "image/jpeg", "image/png", "image/webp"]

def check_all_none_except(data, keys_to_except):
    for key, value in data.items():
        if key not in keys_to_except and value is not None:
            return False
    return True

async def check_image_content_type(self, image_url, html_custom_headers=None):
    if not image_url:
        return None
    try:
        resp = await self.http.get(str(image_url), headers=html_custom_headers)
    except Exception as err:
        self.log.exception(f"[urlpreview] [utils] check_image_content_type Error: {err} - {str(image_url)}")
        return None
    if resp.status != 200:
        return None
    if resp.content_type in IMAGE_TYPES:
        return resp.content_type
    return None

def check_line_breaks(text: str):
    if text is None:
        return None
    return text.replace('\n', '<br />')

def format_title(title, url_str: str="", custom_styles: str="",use_divtag_instead_of_htag: bool=False):
    if not title:
        return None
    tag = 'div' if use_divtag_instead_of_htag else 'h3'
    if url_str:
        return f'<{tag} style="{custom_styles}"><a href="{url_str}">{str(title)}</a></{tag}>'
    else:
        return f'<{tag} style="{custom_styles}" >{str(title)}</{tag}>'

def format_description(description, preserve_line_breaks: bool=False, custom_styles: str="", indent_description: bool=False, use_divtag_instead_of_ptag: bool=False):
    if not description:
        return None
    prefix = '&#8250;&nbsp;&nbsp;&nbsp;&nbsp;' if indent_description else ''
    tag = 'div' if use_divtag_instead_of_ptag else 'p'
    if preserve_line_breaks is False:
        return f'<{tag} style="{custom_styles}">{prefix}'+str(description).replace('\r', ' ').replace('\n', ' ')+f'</{tag}>'
    else:
        return f'<{tag} style="{custom_styles}">{prefix}'+str(description)+f'</{tag}>'

def format_image(image_mxc, url_str: str='', content_type: str=None, max_image_embed: int=300, custom_styles: str=""):
    if not image_mxc:
        return None
    if not content_type:
        content_type = "Image"
    width = ''
    if max_image_embed > 0:
        width = f'width="{str(max_image_embed)}" '
    if url_str:
        return f'<a href="{url_str}"><img style="{custom_styles}" src="{image_mxc}" alt="{content_type}" {width}/></a>'
    else:
        return f'<img style="{custom_styles}" src="{image_mxc}" alt="{content_type}" {width}/>'
def format_video(video_mxc, url_str: str='', content_type: str=None):
    if not video_mxc:
        return None
    if not content_type:
        content_type = "Video"

    if url_str:
        return f'<a href="{url_str}"><video width="320" height="240" controls><source src="{video_mxc}" type="video/mp4"></video></a>'
    else:
        return f'<video width="320" height="240" controls><source src="{video_mxc}" type="video/mp4"></video>'

def format_image_width(image_width, max_image_embed: int=300):
    if image_width is None:
        return max_image_embed
    return min(int(image_width), max_image_embed)

async def process_image(self, image: str, html_custom_headers=None, content_type: str=None):
    if not image:
        return None
    image_url = urlparse(image)
    # URL is mxc
    if image_url.scheme == 'mxc':
        return image
    # URL is not mxc
    if not content_type:
        content_type = await check_image_content_type(self, image, html_custom_headers=html_custom_headers)
    if not content_type:
        content_type = 'image/jpeg'
    image_mxc = await matrix_get_image(
        self,
        image_url=image,
        html_custom_headers=html_custom_headers,
        mime_type=content_type,
        filename=content_type.replace('/', '.').replace('jpeg', 'jpg')
    )
    return image_mxc

async def matrix_get_image(self, image_url: str, html_custom_headers=None, mime_type: str="image/jpeg", filename: str="image.jpg"):
    if not image_url:
        return None
    try:
        resp = await self.http.get(image_url, headers=html_custom_headers)
    except Exception as err:
        self.log.exception(f"[urlpreview] [utils] Error matrix_get_image http.get: {str(err)}")
        return None
    if resp.status != 200:
        self.log.exception(f"[urlpreview] [utils] Error matrix_get_image resp.status: {str(resp.status)} - {str(urlparse(image_url).netloc)}")
        return None
    og_image = await resp.read()
    try:
        mxc = await self.client.upload_media(og_image, mime_type=mime_type, filename=filename)
    except Exception as err:
        self.log.exception(f"[urlpreview] [utils] Error matrix_get_image client.upload_media: {str(err)}")
        return None
    return mxc
async def process_video(self, video: str, html_custom_headers=None, content_type: str=None):
    if not video:
        return None
    video_url = urlparse(video)
    # URL is mxc
    if video_url.scheme == 'mxc':
        return video
    # URL is not mxc
    # yt-dlp puts out either mp4 or webm
    if not content_type:
        content_type = 'video/webm'
    image_mxc = await matrix_get_youtube_video(
        self,
        video_url=video,
        html_custom_headers=html_custom_headers,
        mime_type=content_type,
        filename=content_type.replace('/', '.').replace('jpeg', 'jpg')
    )
    return image_mxc
async def matrix_get_youtube_video(self, video_url: str, html_custom_headers=None, mime_type: str="video/webm", filename: str=""):
    if not filename:
        h = hashlib.md5(bytes(dt.now()))
        filename = str(dt.now() + h.hexdigest())
    if not video_url:
        return None
    try:
        result = subprocess.run(f'yt-dlp -p {self.YT_DLP_STORAGE_PATH} --no-part {video_url} -o "{filename}"')
    except Exception as err:
        self.log.exception(f"[urlpreview] [utils] Error matrix_get_youtube_video http.get: {str(err)}")
        return None

    og_video = None
    with open(filename, 'rb') as h:
        og_video = h.read()
    try:
        mxc = await self.client.upload_media(og_video, mime_type=mime_type, filename=filename)
    except Exception as err:
        self.log.exception(f"[urlpreview] [utils] Error matrix_get_youtube_video client.upload_media: {str(err)}")
        return None
    return mxc


def url_check_is_in_range(ip, unsafe_url, ranges):
    for r in ranges:
        # Range item is an IP
        try:
            if ipaddress.ip_address(ip) in ipaddress.ip_network(r, strict=False):
                return True
        # Range item is a regex
        except ValueError:
            if re.search(r, unsafe_url) is not None:
                return True
    return False

def url_get_ip_from_hostname(hostname):
    # IPv4
    try:
        return socket.gethostbyname(hostname)
    except socket.gaierror:
        pass
    # IPv6
    try:
        answers = socket.getaddrinfo(hostname, None, socket.AF_INET6)
        for answer in answers:
            if answer[1] == socket.SOCK_STREAM:
                return answer[4][0]
    except (socket.gaierror, IndexError):
        pass
    return None

def url_check_blacklist(url, blacklist):
    if "://" not in url:
        url = "http://" + url
    hostname = urlparse(url).hostname
    ip = url_get_ip_from_hostname(hostname)
    if not ip:
        return False
    is_blacklisted = url_check_is_in_range(ip, url, blacklist)
    if not is_blacklisted:
        return url
    return None

def user_check_blacklist(user, blacklist):
    if user in blacklist:
        return True
    return False
