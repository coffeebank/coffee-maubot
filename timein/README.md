# timein

Get the time in specific cities. Check timezones.

**`[p]timein New York`**

![preview.jpg](preview.jpg)

## [Download >](releases)

- [Join our Matrix room >](../../../#readme)

<br>


## Requirements

### Python 3.9+

Dependences are optional. For Improved Search (see Notes below), run:

`pip install pytz fuzzywuzzy`

### Python 3.6-3.8

**Dependencies are required. Run:**

`pip install pytz fuzzywuzzy`


## Commands

- `timein`
  - Get the time in a city/timezone


## Notes

- Improved Search requires `pytz` and `fuzzywuzzy` dependencies
  - 🔺 `!timein new york`
    - Searches work even with only the city name, typos, and in lowercase
  - 🔹 `!timein America/New_York`
    - Without Improved Search, you must specify the exact timezone
- Timein requires Improved Search for Python <3.9
