from typing import Any, List, Optional

class SendableMenuCollapsible:
    """Menu formatter, Collapsible type"""

    def to_sendable(pages: List[str]):
        """Converts this object into a sendable object, in formatted HTML text."""
        sendable = ""
        for index, page in enumerate(pages):
            sendable += SendableMenuCollapsible.format_menu_collapsible_item(page, index=index)
        return sendable

    def format_menu_collapsible_item(body: str, index: int=None):
        if index == 0:
            return f"""<div>{body}</div>"""
        elif index:
            return f"""<hr /><details><summary>Page {str(index+1)}</summary><div>{body}</div></details>"""
        else:
            return f"""<details><div>{body}</div></details>"""
