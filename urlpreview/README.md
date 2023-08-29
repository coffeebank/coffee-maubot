# urlpreview

A bot that responds to links with a link preview embed, using Matrix API to fetch meta tags

![preview.jpg](preview.jpg)

## [Download >](releases)

- [Join our Matrix room >](../../../#readme)

<br>


## Config

- `max_links` - Change how many links you'd like to process per message. 1-3 is recommended.
- `max_image_embed` - Change the maximum image width displayed in the embed. 300 is recommended.
- `no_results_react` - Adds a reaction emoji to the message to show that no results were returned. Put `''` to disable.

### Matrix Synapse URL Previews API

This is optional, but highly recommended for a better experience.

- `appid` - Your bot's access token. This is needed to make the request to the Matrix Synapse URL Preview API.
- `homeserver` - Your homeserver (matrix-client.matrix.org by default, don't add https in front)
- ~~`min_image_width` - Change the minimum image width before the bot sends an image. 500 is recommended to avoid favicons.~~


## Usage

Sending any link in chat will have the bot reply to your message with the link's embed details.

The bot will first mark the chat as read, to indicate that it has initiated properly.

If there are multiple links in the message, the bot will fetch up to `max_links` (3) links using aiohttp. If it fails, it will skip embedding that link.

If the link returns a 404, the bot will return an emoji `no_results_react` (💨) on your message, to show that no results were returned.


## Notes

- This bot comes with two parsers: `htmlparser` and `synapse`. By default, both are enabled.
- You can control which ones to enable/disable or prioritize using `EXT_ENABLED` (last in array takes priority).

### htmlparser

- `htmlparser` works out-of-the-box by directly fetching the HTML page and parsing using `htmlparser` (built-in).
- This may leak your server's IP, and is recommended for bots hosted in a VPS/server environment.
- Some sites protected by Cloudflare/similar services may not return results.

### synapse

- `synapse` depends on [Synapse URL Previews](https://matrix-org.github.io/synapse/latest/setup/installation.html?highlight=url%20previews#url-previews) from the [matrix.org homeserver](https://matrix.org/legal/terms-and-conditions/).
- `synapse` requires you to specify an `appid` and `homeserver` that runs Synapse and supports URL Previews.

<br />

- Due to the length of some embeds, line-breaks are stripped from any `og:description` tags.
- Image width is hardcoded at `max_image_embed` px wide. There may be an option in the future to install a dependency that'll parse image height.
