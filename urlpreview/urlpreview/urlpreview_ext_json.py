import json
import urllib.parse
from urllib.parse import urlparse

from .urlpreview_utils import check_line_breaks

async def fetch_json(self, url_str, json_max_char=2000, html_custom_headers=None, **kwargs):
    if not url_str:
        return None
    if html_custom_headers:
        html_custom_headers["Content-Type"] = "application/json"
    else:
        html_custom_headers = {"Content-Type": "application/json"}

    try:
        resp = await self.http.get(
            url_str,
            headers=html_custom_headers,
            timeout=30
        )
    except Exception as err:
        self.log.exception(f"[urlpreview] [ext_json] Error: {str(err)} - {str(urlparse(url_str).netloc)}")
        return None

    # Guard clause
    if resp.status != 200:
        self.log.exception(f"[urlpreview] [ext_json] Error: Status {str(resp.status)} - {str(urlparse(url_str).netloc)} - {str(resp)}")
        return None
    try:
        json_raw = await resp.json(content_type=None) # Allow JSON sent as text/plain or other mime_types
    except Exception as err:
        self.log.debug(f"[urlpreview] [ext_json] Response is not json, ending fetch_json - {str(err)}")
        return None

    # JSON
    self.log.debug(f"[urlpreview] [ext_json] fetch_json {str(json_raw)[:600]} ...")
    json_str = json.dumps(json_raw, sort_keys=False, indent=2, separators=(',', ': '))
    
    return {
        "title": None,
        "description": f"<pre><code>{str(check_line_breaks(json_str))[:json_max_char]}</code></pre>",
        "image": None,
        "image_mxc": None,
        "content_type": None,
        "image_width": None,
    }
