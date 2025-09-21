# animemanga

An anime manga bot for Matrix.

Search anime, manga (manhwa/manhua), and light novels. See series info, status, and episodes/chapters.

Supports Anilist, MangaDex, Bangumi, and Batoto.

**`[p]manga Give My Regards to Black Jack`**

![preview.jpg](https://coffeebank.github.io/coffee-maubot/assets/animemanga-preview.jpg)

<div className="hidden">

## [Download >](https://coffeebank.github.io/coffee-maubot/animemanga)

- [Join our Matrix room >](https://coffeebank.github.io/matrix)

</div>

<br />

## Features

- Synopsis/summary with official sources, streaming sites, and links
- English language titles with Native language and Romaji/Romanization support
- Series status (Finished, Releasing, Not yet released)
- Series preview embed images
- Media sub-types (Oneshot, Novel, ONA, etc.)


## Commands

- `!anime <title: str>`
  - Search for anime, animations, and donghua
- `!manga <title: str>`
  - aliases=`["manhwa", "manhua", "lightnovel"]`
  - Search for manga, manhwa, manhua, and light novels. Searches Anilist, MangaDex, and Batoto.
- `!anilist <type: str> <title: str>`
  - `type:`
    - `anime`, aliases=`["donghua", "动画", "動畫", "アニメ", "あにめ"]`
    - `manga`, aliases=`["manhua", "漫画", "漫畫", "manhwa", "만화", "lightnovel", "小说", "小說", "小説"]`
  - Search Anilist. Type is "anime" or "manga". Light novel searches are categorized as "manga".
- `!mangadex <title: str>`
  - Search MangaDex
- `!bangumi <type: str> <title: str>`
  - `type:`
    - `anime`, aliases=`["donghua", "动画", "動畫", "アニメ", "あにめ"]`
    - `manga`, aliases=`["manhua", "漫画", "漫畫", "manhwa", "만화", "lightnovel", "小说", "小說", "小説"]`
  - Search Bangumi. Type is "anime" or "manga". Light novel searches are categorized as "manga". Note: Results may be in non-English languages.
- `!batoto <title: str>`
  - Search Batoto


## Config

- `results` - The number of results the bot should return
- `max_description_length` - The length of the description body (not currently used)
- `deepl_api` - [DeepL Translate Free API key](https://www.deepl.com/pro-api) (not currently used)


## Notes

- All manga/manhwa/manhua and light novel searches are categorized under "manga" by Anilist and Bangumi. Searches may return unexpected results.
- `results` - 2 recommended, set 0 to show all results. Higher counts take longer as the bot has to upload/fetch Matrix mxc for each image. A paginate feature has been added in v0.2.0.
- This bot is tested on [Cinny](https://cinny.in).

## License

- This project contains code from [coffeeani by coffee-cogs](https://github.com/coffeebank/coffeeani-dpy) (AGPL-3.0 License) and [anisearch by Jintaku and Wyn](https://github.com/Jintaku/Jintaku-Cogs-V3/tree/master/anisearch) (AGPL-3.0 License)
