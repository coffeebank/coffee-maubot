# animemanga

Search anime, manga (manhwa/manhua), and light novels from Anilist. See series info, status, and episodes/chapters.

**`[p]manga Give My Regards to Black Jack`**

<br>

- [Download >](releases)
- [Join our Matrix room >](../../../#readme)

![preview.jpg](preview.jpg)

<br>

## Features

- Synopsis/summary with official sources, streaming sites, and links
- English language titles with Native language and Romaji/Romanization support
- Series status (Not yet released, Releasing, Finished)
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
- Images are not yet supported.
  - Let me know in the Matrix chat if this feature is important to you!

## License

- This project contains code from [anisearch by Jintaku and Wyn](https://github.com/Jintaku/Jintaku-Cogs-V3/tree/master/anisearch) (AGPL-3.0 License)
