import os
from dotenv import load_dotenv
from typing import Optional, Tuple
import tmdbsimple as tmdb

# Load environment variables
load_dotenv()

tmdb.API_KEY = os.getenv("TMDB_API_KEY", '')

search = tmdb.Search()

def _get_tmdb_data(t: str, is_movie: bool = False) -> Optional[dict]:
    # For Movie
    if is_movie:
        response = search.movie(query=t, language="ja-JP")
        for result in response['results']:
            if (result['original_title'] == t) or (result['title'] == t):
                return result
    # For TV Show
    response = search.tv(query=t, language="ja-JP")
    for result in response['results']:
        if (result['original_name'] == t) or (result['name'] == t):
            return result
    return None

def get_tmdb_matched_show(title_chunks: list[str], is_movie: bool = False) -> Tuple[Optional[str], Optional[dict]]:
    # Group of chunks
    for ti in range(len(title_chunks)):
        t = ' '.join(title_chunks[:ti + 1])
        tmdb_data = _get_tmdb_data(t, is_movie)
        if tmdb_data:
            return t, tmdb_data
    # Single title
    for t in title_chunks:
        tmdb_data = _get_tmdb_data(t, is_movie)
        if tmdb_data:
            return t, tmdb_data
    return None, None