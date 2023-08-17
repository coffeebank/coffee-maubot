from maubot import Plugin, MessageEvent
from maubot.handlers import command
from typing import Optional
from datetime import datetime

IMPROVED_SEARCH = False
try:
    import pytz
    from fuzzywuzzy import fuzz, process
    IMPROVED_SEARCH = True
except ImportError:
    from zoneinfo import ZoneInfo # Python 3.9+

def fuzzy_timezone_search(tz: str):
    if IMPROVED_SEARCH is True:
        fuzzy_results = process.extract(tz.replace(" ", "_"), pytz.common_timezones, limit=500, scorer=fuzz.partial_ratio)
        matches = [x for x in fuzzy_results if x[1] > 98] 
        return matches
    return None

async def format_results(tz):
    if len(tz) == 1:
        return tz
    else:
        return None

class TimeinBot(Plugin):
    @command.new("timein", help="Get the time in specific cities. Check timezones.")
    @command.argument("city_or_timezone", pass_raw=True)
    async def timein(self, evt: MessageEvent, city_or_timezone: str) -> None:
        if IMPROVED_SEARCH is True:
            tz_results = fuzzy_timezone_search(city_or_timezone)
            tz_resp = await format_results(tz_results)
            if tz_resp:
                time = datetime.now(pytz.timezone(tz_resp[0][0]))
                fmt = "**%H:%M** *(%I:%M %p)*\n**%A, %d %B %Y**\n*%Z (UTC %z)"
                await evt.respond("> "+time.strftime(fmt)+f", {tz_resp[0][0]}*")
            else:
                await evt.respond("No timezone found. Find a list of cities/timezones here: https://coffeebank.github.io/timezone-picker/")
        elif IMPROVED_SEARCH is False:
            try:
                time = datetime.now(ZoneInfo(city_or_timezone))
                fmt = "**%H:%M** *(%I:%M %p)*\n**%A, %d %B %Y**\n*%Z (UTC %z)"
                await evt.respond("> "+time.strftime(fmt)+f", {city_or_timezone}*")
            except:
                await evt.respond("No timezone found. Find a list of timezones here: https://coffeebank.github.io/timezone-picker/")
