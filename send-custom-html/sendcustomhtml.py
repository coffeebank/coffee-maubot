from maubot import Plugin, MessageEvent
from maubot.handlers import command

class SendCustomHtmlBot(Plugin):
    @command.new("sendcustomhtml", help="Have the bot send a message as custom HTML.")
    @command.argument("html", pass_raw=True)
    async def sendcustomhtml(self, evt: MessageEvent, html: str) -> None:
        await evt.reply(html, allow_html=True)
