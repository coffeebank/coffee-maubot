# kodict

A Korean dictionary Matrix bot for searching and translating Korean vocabulary.

Searches National Institute of Korean Language's Korean-English Learners' Dictionary (한국어기초사전).

![preview.jpg](https://coffeebank.github.io/coffee-maubot/assets/kodict-preview.jpg)

<div className="hidden">

## [Download >](https://coffeebank.github.io/coffee-maubot/kodict)

- [Join our Matrix room >](https://coffeebank.github.io/matrix)

</div>

<br />

## Features

- Search dictionary entries in Korean (Hangul, Hanja)
- Search dictionary entries in English
- Pronunciation in Hangul and Romanization
- Word origins in Hanja
- Parts of speech


## Setup

**Note: A [Korean-English Learners' Dictionary (한국어기초사전) API](https://krdict.korean.go.kr/openApi/openApiInfo) (free) is required.**

**Prerequisites are required:**
- Shut down your Maubot, then run:
  - `python -m pip install cssselect kodict-core korean-romanizer krdict.py@git+https://github.com/coffeebank/krdict.py lxml`
- Start your Maubot again, then install the .mbp from your Maubot Dashboard website, and add an instance
- In the Config, add your [Korean-English Learners' Dictionary (한국어기초사전) API](https://krdict.korean.go.kr/openApi/openApiInfo) key under `krdict_api`
- Click Save


## Config

- `krdict_api` - [Korean-English Learners' Dictionary (한국어기초사전) API](https://krdict.korean.go.kr/openApi/openApiInfo) (free)
- `deepl_api` - [DeepL API Free](https://www.deepl.com/pro-api)
- `results` - The number of results the bot should return


## Commands

- `kodict`, aliases=`["krdict"]`
  - Searches Korean dictionary

Uses material from National Institute of Korean Language's [Korean-English Learners' Dictionary (한국어기초사전)](https://krdict.korean.go.kr/eng/mainAction).


## Notes

- **This plugin require Python 3.9+** ([Maubot recommends Python 3.10+](https://docs.mau.fi/maubot/usage/setup/index.html))
- A [Korean-English Learners' Dictionary (한국어기초사전) API](https://krdict.korean.go.kr/openApi/openApiInfo) (free) is required.
  - `krdict.py`'s non-api URLs needs fixing. No ETA. The API methods still work.
- A custom `krdict.py` dependency is required.
  - The custom version replaces `requests` with `aiohttp, asyncio` for async support
