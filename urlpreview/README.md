# urlpreview

A bot that responds to links with a link preview embed, using Matrix API to fetch meta tags

- [Download >](releases)
- [Join our Matrix room >](../../../#readme)

![preview.jpg](preview.jpg)

<br>


## Config

`appid` - Your bot's access token. This is needed to make the request to matrix.org's URL preview API.


## Usage

Sending any link in chat will have the bot reply to your message with the link's embed details.

The bot will first mark the chat as read, to indicate that it has initiated properly.

If there are multiple links in the message, the bot will send up to 3 requests to matrix.org's URL preview API. If it fails due to ratelimiting, it will skip embedding that link.

If the link returns a 404, the bot will return an 💨 emoji on your message, to show that no results were returned.


## Notes

- This bot uses [Synapse URL Previews](https://matrix-org.github.io/synapse/latest/development/url_previews.html) from the [matrix.org homeserver](https://app.element.io).
  - To authenticate requests, it uses your bot's access token, to be provided in `appid` when you load this plugin.
- Due to the way quoting works and the length of some embeds, line-breaks will be stripped from any `og:description` tags.
