import re

def is_num(s: str) -> bool:
    return True if s.isdecimal() and s.isascii() else False

def get_title_separated(title: str) -> list[str]:
    title_chunks = re.split('[()【】《》（）［］<>「」\[\]~-☆▽▼●◆・※ :,!]', title)
    return title_chunks