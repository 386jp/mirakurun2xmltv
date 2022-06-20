import re
from kanjize import kanji2int
from typing import Optional, Tuple

episode_regex = [
    [r'【[0-9]{0,5}】', r'(?<=【)[0-9]{0,5}(?=】)'],
    [r'\([0-9]{0,5}\)', r'(?<=\()[0-9]{0,5}(?=\))'],
    [r'#[0-9]{0,5}', r'(?<=#)[0-9]{0,5}'],
    [r'第[0-9]{0,5}話', r'(?<=第)[0-9]{0,5}(?=話)'],
    [r'第[0-9]{0,5}回', r'(?<=第)[0-9]{0,5}(?=回)'],
    [r'第[0-9]{0,5}節', r'(?<=第)[0-9]{0,5}(?=節)'],
    [r'第[一二三四五六七八九十壱弐参拾百千万萬億兆〇]{0,5}話', r'(?<=第)[一二三四五六七八九十壱弐参拾百千万萬億兆〇]{0,5}(?=話)'],
]

def get_episode_number_from_title(title: str) -> Tuple[Optional[int], list[str]]:
    for query, cleanup_query in episode_regex:
        match = re.search(query, title)
        if match:
            clean_match = re.search(cleanup_query, title)
            if clean_match:
                try:
                    episode_id = int(clean_match.group())
                except:
                    episode_id = kanji2int(clean_match.group())
                finally:
                    return episode_id, [title[0:match.span()[0]], title[match.span()[1]:]]
    return None, [title]