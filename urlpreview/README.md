# urlpreview

A bot that responds to links with a link preview embed, using Matrix API to fetch meta tags

- [Download >](releases)
- [Join our Matrix room >](../../../#readme)

![preview.jpg](preview.jpg)

<br>


## Config

- `appid` - Your bot's access token. This is needed to make the request to matrix.org's URL preview API.
- `homeserver` - Your homeserver (matrix-client.matrix.org by default, don't add https in front)
- `max_links` - Change how many links you'd like to process per message. 1-3 is recommended.
- `min_image_width` - Change the minimum image width before the bot sends an image. 500 is recommended to avoid favicons.
- `max_image_embed` - Change the maximum image width displayed in the embed. 300 is recommended.


## Usage

Sending any link in chat will have the bot reply to your message with the link's embed details.

The bot will first mark the chat as read, to indicate that it has initiated properly.

If there are multiple links in the message, the bot will send up to `max_links` (3) requests to `homeserver` (matrix.org)'s URL preview API. If it fails due to ratelimiting, it will skip embedding that link.

If the link returns a 404, the bot will return an 💨 emoji on your message, to show that no results were returned.


## Notes

- This bot uses [Synapse URL Previews](https://matrix-org.github.io/synapse/latest/setup/installation.html?highlight=url%20previews#url-previews) from the [matrix.org homeserver](https://matrix.org/legal/terms-and-conditions/).
  - To authenticate requests, it uses your bot's access token, to be provided in `appid` when you load this plugin.
- Due to the length of some embeds, line-breaks will be stripped from any `og:description` tags.
