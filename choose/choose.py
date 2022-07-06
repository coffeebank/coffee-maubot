from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import Optional
import random

class ChooseBot(Plugin):
    @command.new("choose", help="Have the bot choose for you")
    @command.argument("chooseText", pass_raw=True)
    async def echo_handler(self, evt: MessageEvent, chooseText: str) -> None:
        chooseArray = chooseText.split("|")
        chooseReply = random.choice(chooseArray)
        await evt.respond(f"> #### {chooseReply} \n> *choose by [{evt.sender}](https://matrix.to/#/{evt.sender})*")
