import ipaddress
import re
import socket
import urllib.parse
from urllib.parse import urlparse

IMAGE_TYPES = ["image/gif", "image/jpg", "image/jpeg", "image/png", "image/webp"]

def check_all_none_except(data, keys_to_except):
    for key, value in data.items():
        if key not in keys_to_except and value is not None:
            return False
    return True

async def check_image_content_type(self, image_url):
    if not image_url:
        return None
    try:
        resp = await self.http.get(str(image_url))
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

def format_title(title, url_str: str=""):
    if not title:
        return None
    if url_str:
        return f'<h3><a href="{url_str}">{str(title)}</a></h3>'
    else:
        return f'<h3>{str(title)}</h3>'

def format_description(description, preserve_line_breaks: bool=False):
    if not description:
        return None
    if preserve_line_breaks is False:
        return f'<p>'+str(description).replace('\r', ' ').replace('\n', ' ')+'</p>'
    else:
        return f'<p>'+str(description)+'</p>'

def format_image(image_mxc, url_str: str='', content_type: str=None, max_image_embed: int=300):
    if not image_mxc:
        return None
    if not content_type:
        content_type = "Image"
    width = ''
    if max_image_embed > 0:
        width = f'width="{str(max_image_embed)}" '
    if url_str:
        return f'<a href="{url_str}"><img src="{image_mxc}" alt="{content_type}" {width}/></a>'
    else:
        return f'<img src="{image_mxc}" alt="{content_type}" {width}/>'

def format_image_width(image_width, max_image_embed: int=300):
    if image_width is None:
        return max_image_embed
    return min(int(image_width), max_image_embed)

async def process_image(self, image: str, content_type: str=None):
    if not image:
        return None
    image_url = urlparse(image)
    # URL is mxc
    if image_url.scheme == 'mxc':
        return image
    # URL is not mxc
    if not content_type:
        content_type = await check_image_content_type(self, image)
    if not content_type:
        content_type = 'image/jpeg'
    image_mxc = await matrix_get_image(
        self,
        image,
        mime_type=content_type,
        filename=content_type.replace('/', '.').replace('jpeg', 'jpg')
    )
    return image_mxc

async def matrix_get_image(self, image_url: str, mime_type: str="image/jpeg", filename: str="image.jpg"):
    if not image_url:
        return None
    try:
        resp = await self.http.get(image_url)
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
