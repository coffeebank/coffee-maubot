# timein

Get the time in specific cities. Check timezones.

**`[p]timein New York`**

![preview.jpg](preview.jpg)

## [Download >](releases)

- [Join our Matrix room >](../../../#readme)

<br>


## Requirements

### Python 3.9+

Dependences are optional, but highly recommended. See Fallback Search in Notes section below.

`pip install pytz fuzzywuzzy`

### Python <=3.8

**Dependencies are required. Run:**

`pip install pytz fuzzywuzzy`


## Commands

- `timein`
  - Get the time in a city/timezone

Find valid cities and timezone strings at [https://coffeebank.github.io/timezone-picker/](https://coffeebank.github.io/timezone-picker/)


## Notes

- Dependencies: `pytz`, `fuzzywuzzy`
  - 🔺 `!timein new yo`
    - These dependencies allow the bot to search with the city name, typos, and in lowercase
- Fallback Search (Python 3.9+ only)
  - 🔹 `!timein America/New_York`
    - In Fallback Search mode, you must specify the exact timezone string for the bot to work
