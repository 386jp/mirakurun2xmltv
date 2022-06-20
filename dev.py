#%%
import datetime
import xml.etree.ElementTree as ET
from app.controllers.xmltv2tmdb import get_program_data_cleaned

#%%
tree = ET.parse("dev-epg.xml")
root = tree.getroot()

programs = root.findall('programme')
#%%
get_program_data_cleaned(programs[0])
#%%
import re
import mojimoji
import xml.etree.ElementTree as ET

from app.controllers.jpepgtools.tags.title import get_tags_from_title
from app.controllers.jpepgtools.episode import get_episode_number_from_title
from app.controllers.jpepgtools.title_separator import get_title_separated, is_num
from app.controllers.tmdb.show_data import get_tmdb_matched_show

#%%
# タイトル取得
# title = str(program.find('title').text)
title = "金曜ロードショー「トイ・ストーリー４」★本編ノーカットで初放送★🈔🈑🈓"
title = "マネーのまなび【高リスク金融商品にご用心!】"

# タグ取得 (映画かどうか判定)
is_movie = False
# for c in program.findall('category'):
#     if str(c.text).startswith('映画'):
#         is_movie = True
is_movie = True

# 全角文字を半角文字に変換
title = mojimoji.zen_to_han(title, kana=False)

# タイトル前処理
title = title.replace('ミニ', ' ミニ')
title = title.replace('SP', ' SP')
title = title.replace('!', '! ')

# タイトルタグとタイトルを分離
tag, title_alt1 = get_tags_from_title(title)

# タイトルタグから映画かどうか判別
if '映画' in tag:
    is_movie = True

# タイトルからエピソード番号を抽出
episode_id, title_alt2 = get_episode_number_from_title(title_alt1)

# タイトルを区切り文字で分割
title_chunks = []
for t in title_alt2:
    title_chunks.extend(get_title_separated(t))
title_chunks = [chunk for chunk in title_chunks if chunk != '']
title_chunks = [chunk for chunk in title_chunks if not is_num(chunk)]

# TMDbによるデータ取得
cleaned_title, show_data = get_tmdb_matched_show(title_chunks, is_movie = is_movie)

# タイトルとサブタイトルの処理
if cleaned_title and show_data:
    cleaned_title_chunk_id = title_chunks.index(cleaned_title)
    main_title = " ".join(title_chunks[:cleaned_title_chunk_id+1])
    sub_title = " ".join(title_chunks[cleaned_title_chunk_id+1:])
    main_title = re.sub('[ 　]+', ' ', main_title)
    sub_title = re.sub('[ 　]+', ' ', sub_title)
else:
    if title_alt2[0]:
        if len(title_alt2) == 2:
            main_title = title_alt2[0]
            sub_title = title_alt2[1]
        else:
            if len(title_chunks) == 2:
                main_title = title_chunks[0]
                sub_title = title_chunks[1]
            else:
                main_title = title_alt2[0]
                sub_title = ""
    else:
        if title:
            main_title = title
        else:
            main_title = ''
        sub_title = ""

{
    'title': main_title,
    'sub_title': sub_title,
    'tags': tag,
    'episode_id': episode_id,
    'tmdb_show_data': show_data if show_data else {}
}
#%%
