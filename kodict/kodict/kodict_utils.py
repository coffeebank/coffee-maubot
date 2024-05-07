import urllib.parse
import kodict_core
from korean_romanizer.romanizer import Romanizer

from .cmfmatrixpy import Embed

## Utility Commands

def truncate(text: str, max: int, extension: str="…"):
    if len(text) > max:
        return text[:max-1]+extension
    else: return text

async def embed_krdict(krdict_results, attribution: list[str]=["Krdict (한국어기초사전)"]):
    sendEmbeds = []
    attribution = "Results from "+", ".join(attribution)
    try:
        total = str(min(int(krdict_results.total_results), 10))
    except:
        total = "..."
    for result_idx, krdict_result in enumerate(krdict_results.results):
        e = await embed_krdict_result(krdict_result, result_idx, str(total), attribution)
        sendEmbeds.append(e)
    return sendEmbeds

async def embed_krdict_result(krdict_result, result_idx: int, total: str, attribution: str):
    e = Embed(
        title=str(krdict_result.word),
        url=str(krdict_result.url),
        description=kodict_core.services.krdict.krdict_results_body(krdict_result),
        colour=None
    )
    for idx, kr_def in enumerate(krdict_result.definitions):
        krdict_definition = kodict_core.services.krdict.krdict_results_definition(kr_def, idx)
        e.add_field(
            name=krdict_definition.get("name"),
            value=krdict_definition.get("value")
        )
    e.set_footer(
        text=" ・ ".join(filter(None, [
            str(attribution),
            str(result_idx+1)+"/"+str(total)
        ])))
    return e

async def embed_deepl(text, deepl_results=None, description=None):
    safe_text = urllib.parse.quote(text, safe='')
    alt_links = [
      f"Wiktionary: [EN](https://en.wiktionary.org/w/index.php?fulltext=0&search={safe_text}), [KO](https://ko.wiktionary.org/w/index.php?fulltext=0&search={safe_text})",
      f"Google Translate: [EN](https://translate.google.com/?text={safe_text})"
    ]
    if len(" ・ ".join(alt_links)) > 1013:
        alt_links = [
            "Wiktionary: [EN](https://en.wiktionary.org), [KO](https://ko.wiktionary.org)",
            "Google Translate: [EN](https://translate.google.com)"
        ]
    if Romanizer(str(text)).romanize() != text:
        text_romanization = str(Romanizer(str(text)).romanize())
    else:
        text_romanization = None
    if Romanizer(str(deepl_results)).romanize() != deepl_results:
        deepl_results = "\n".join([deepl_results, truncate(str(Romanizer(str(deepl_results)).romanize()), 250)])
    desc = "\n".join(filter(None, [text_romanization, description]))
    e = Embed(title=truncate(str(text), 100), description=desc, colour=None)
    e.add_field(name="Translation", value=">>> "+truncate(str(deepl_results), 1019), inline=False)
    e.add_field(name="More Links", value=" ・ ".join(alt_links), inline=False)
    e.set_footer(text="Results from DeepL. No Krdict search results found.")
    return e

async def embed_fallback(text, description=None, footer=None):
    safe_text = urllib.parse.quote(text, safe='')
    e = Embed(title=truncate(str(text), 100), description=description, colour=None)
    e.add_field(name="Krdict (한국어기초사전)", value=f"https://krdict.korean.go.kr/eng/dicMarinerSearch/search?mainSearchWord={safe_text}")
    e.add_field(name="Wiktionary", value=f"https://en.wiktionary.org/w/index.php?fulltext=0&search={safe_text}")
    e.add_field(name="DeepL Translate", value=f"https://deepl.com/translator#ko/en/{safe_text}")
    e.add_field(name="Google Translate", value=f"https://translate.google.com/?text={safe_text}")
    if footer:
        e.set_footer(text=footer)
    return e
