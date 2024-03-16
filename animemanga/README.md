# animemanga

An anime manga bot for Matrix.

Search anime, manga (manhwa/manhua), and light novels from Anilist. See series info, status, and episodes/chapters.

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
- Series status (Not yet released, Releasing, Finished)
- Series preview embed images
- Media sub-types (Oneshot, Novel, ONA, etc.)


## Commands

- `anime`
  - Searches for anime using Anilist
- `manga`, aliases=`["manhwa", "manhua", "lightnovel", "漫画", "漫画", "만화"]`
  - Searches for manga/manhwa/manhua and light novels using Anilist


## Config

- `results` - The number of results the bot should return
- `max_description_length` - The length of the description body


## Notes

- All manga/manhwa/manhua and light novel searches are categorized under "manga" by Anilist. Searches may return unexpected results.
  - A paginate feature has not yet been added. For now, you can adjust the number of `results` returned in the config.
- This bot is tested on Element and Cinny.

## License

- This project contains code from [coffeeani by coffee-cogs](https://github.com/coffeebank/coffeeani-dpy) (AGPL-3.0 License) and [anisearch by Jintaku and Wyn](https://github.com/Jintaku/Jintaku-Cogs-V3/tree/master/anisearch) (AGPL-3.0 License)
