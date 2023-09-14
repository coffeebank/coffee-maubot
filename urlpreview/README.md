# urlpreview

A bot that responds to links with a link preview embed, using Matrix API to fetch meta tags

![preview.jpg](preview.jpg)

## [Download >](releases)

- [Join our Matrix room >](../../../#readme)

<br>


## Config

- `ext_enabled` - Change which data sources to use for meta tags (last in array takes priority)
- `max_links` - Change how many links you'd like to process per message. 1-3 is recommended.
- `max_image_embed` - Change the maximum image width displayed in the embed. 300 is recommended.
- `no_results_react` - Adds a reaction emoji to the message to show that no results were returned. Put `''` to disable.
- `url_blacklist` - Disable urlpreview for an IP range or a Regex entry
- `user_blacklist` - Disable urlpreview for a user

| htmlparser | json | synapse |
| --- | --- | --- |
| N/A | - `json_max_char` - Set a maximum character limit for outputted JSON, to prevent long files from blocking chat. Default 2000. | - `appid` - Your bot's access token. This is needed to make the request to the Matrix Synapse URL Preview API.<br />- `homeserver` - Your homeserver (matrix-client.matrix.org by default, don't add https in front)

<br />

## Usage

Sending any link in chat will have the bot reply to your message with the link's embed details.

The bot will first mark the chat as read, to indicate that it has initiated properly.

If there are multiple links in the message, the bot will fetch up to `max_links` (3) links using aiohttp. If it fails, it will skip embedding that link.

If the link returns a 404, the bot will return an emoji `no_results_react` (💨) on your message, to show that no results were returned.

<br />

## Notes

- This bot comes with three parsers: `htmlparser`, `json`, and `synapse`. By default, all are enabled.
- You can control which ones to enable/disable or prioritize using `ext_enabled` (last in array takes priority).
- Due to the length of some embeds, line-breaks are stripped from any `og:description` tags.
- Image width relies on `og:image:width` provided by websites, and falls back to `max_image_embed` px wide. There may be an option in the future to install a dependency that'll parse image height.

<br />

### htmlparser

- `htmlparser` works out-of-the-box by directly fetching the HTML page and parsing using `htmlparser` (built-in).
- `htmlparser` may leak your server's IP, and is recommended for bots hosted in a VPS/server environment.
- Some sites protected by Cloudflare/similar services may not return results.

### json

- `json` works out-of-the-box by directly fetching pages with `application/json` mime_type and parsing using `json` (built-in).
- `json` may leak your server's IP, and is recommended for bots hosted in a VPS/server environment.
- By default, JSON results are truncated to `json_max_char` (2000) characters in chat.

### synapse

- `synapse` depends on the [Matrix Synapse URL Previews API](https://matrix-org.github.io/synapse/latest/setup/installation.html?highlight=url%20previews#url-previews).
- `synapse` requires you to specify an `appid` and `homeserver` that runs Synapse and supports URL Previews.
- Synapse URL Previews works best with the default [matrix.org homeserver](https://matrix.org/legal/terms-and-conditions/).
  - Some homeservers return 404s at an increased rate. You can check your homeserver's acceptance [on Hoppscotch *(update URL with your homeserver, and BOT_ACCESS_TOKEN in Headers)*](https://hopp.sh/r/wpEdCHsQ8YHM)
- `min_image_width` - Change the minimum image width before the bot sends an image. 475 is recommended to avoid favicons.  - Not implemented yet, to be restored soon

### Upgrade Guide

If you're updating from older urlpreview versions, delete the whole `ext_enabled: [...]` line and click "Save" to activate new parsers.

To get new Config entries, in your Maubot Manager's Instances, please click "Save" (even with no changes) to force-update the default Config values. This will restore missing Config values and defaults. You can also delete some or all of your Config entries and click "Save" to restore defaults.

<br />

### Known Bugs

- YouTube doesn't put line breaks in their `og:description`, which may lead to improperly parsed links in your Matrix client.
