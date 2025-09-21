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

- `anime`
  - Search for anime, animations, and donghua
  - Searches Anilist
- `manga`, aliases=`["manhwa", "manhua", "lightnovel"]`
  - Search for manga, manhwa, manhua, and light novels.
  - Searches Anilist, MangaDex, and Batoto.
- `bangumi`, aliases=`["番组", "番組", "番组计划", "番組計劃"]`
  - `anime` - Search for anime/donghua
  - `manga` - Search for manhua/manga/manhwa
  - Searches Bangumi


## Config

- `results` - The number of results the bot should return
- `max_description_length` - The length of the description body (not currently used)
- `deepl_api` - [DeepL Translate Free API key](https://www.deepl.com/pro-api) (not currently used)


## Notes

- All manga/manhwa/manhua and light novel searches are categorized under "manga" by Anilist and Bangumi. Searches may return unexpected results.
- `results` - 2 recommended, set 0 to show all results. Higher counts take longer as the bot has to upload/fetch Matrix mxc for each image. A paginate feature has been added in v0.2.0.
- This bot is tested on Element and Cinny.

## License

- This project contains code from [coffeeani by coffee-cogs](https://github.com/coffeebank/coffeeani-dpy) (AGPL-3.0 License) and [anisearch by Jintaku and Wyn](https://github.com/Jintaku/Jintaku-Cogs-V3/tree/master/anisearch) (AGPL-3.0 License)
