# timein

Get the time in specific cities. Check timezones.

**`[p]timein New York`**

![preview.jpg](https://coffeebank.github.io/coffee-maubot/assets/timein-preview.jpg)

<div className="hidden">

## [Download >](https://coffeebank.github.io/coffee-maubot/timein)

- [Join our Matrix room >](https://coffeebank.github.io/matrix)

</div>

<br />


## Requirements

Dependences are optional, but highly recommended.

`pip install pytz fuzzywuzzy`


## Commands

- `timein`
  - Get the time in a city/timezone

Find valid cities and timezone strings at [https://coffeebank.github.io/timezone-picker/](https://coffeebank.github.io/timezone-picker/)


## Usage with Dependencies

- 🔺 `!timein new yo`
  - These dependencies allow the bot to search with the city name, typos, and in lowercase


## Usage (Default)

- 🔹 `!timein America/New_York`
  - In Default mode, you must specify the exact timezone string for the bot to work


## Notes

- `timein` works best with Python 3.9+

<details>
{( <summary><h3>For Python &lt;=3.8 Users</h3></summary> )}

> ⚠️ Please note that [Maubot recommends Python 3.10+](https://docs.mau.fi/maubot/usage/setup/index.html).

**`timein` requires dependencies to function on Python &lt;=3.8.**

**Run:**

`pip install pytz fuzzywuzzy`

</details>
