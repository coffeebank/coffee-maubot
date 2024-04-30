import re

def to_html_markdown_links(contents):
    def _markdown_replace_links(match):
        string_part = match.group(1)
        url_part = match.group(2)
        return f'<a href="{url_part}">{string_part}</a>'
    results = contents
    # links
    pattern_links = r'\[([^]]+)\]\((http[^)]+)\)'
    results = re.sub(pattern_links, _markdown_replace_links, results)
    return results.replace("<p>", "").replace("</p>", "")
