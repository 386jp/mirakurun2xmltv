import os
import time
import logging
import asyncio
import datetime
from typing import Optional
from dotenv import load_dotenv
from urllib.request import urlopen
import xml.etree.ElementTree as ET
from app.controllers.xmltv2tmdb import get_program_data_cleaned

# Load environment variables
load_dotenv()

# Logger
logger = logging.getLogger('uvicorn')

async def modify_program_title(program: ET.Element, title: str, subtitle: str):
    program.find('title').text = title
    epg_subtitle = ET.SubElement(program, "sub-title")
    epg_subtitle.text = subtitle

async def modify_program_epid(program: ET.Element, episode_id: Optional[int]):
    if episode_id:
        epg_epid = ET.SubElement(program, "episode-num")
        epg_epid.set('system', "SxxExx")
        epg_epid.text = "S00E" + str(episode_id)
    else:
        epg_air_date = program.attrib["start"]
        if epg_air_date:
            epg_epid = ET.SubElement(program, "episode-num")
            epg_epid.set('system', "original-air-date")
            epg_epid.text = str(datetime.datetime.strptime(epg_air_date, "%Y%m%d%H%M%S +0000").strftime("%Y-%m-%d %H:%M:%S"))

async def modify_program_thumb(program: ET.Element, show_data: Optional[dict]):
    if show_data:
        thumb_src = show_data.get('poster_path')
        if thumb_src:
            epg_thumb = ET.SubElement(program, "icon")
            epg_thumb.set('src', "https://image.tmdb.org/t/p/original" + thumb_src)

async def modify_program_tags(program: ET.Element, tags):
    for tag in tags:
        epg_category = ET.SubElement(program, "category")
        epg_category.text = tag
    if "再放送" in tags:
        epg_category = ET.SubElement(program, "previously-shown")

async def modify_program_info(program: ET.Element):
    cleaned_program_info = get_program_data_cleaned(program)
    logger.info(cleaned_program_info)

    modify_title = asyncio.create_task(modify_program_title(program, cleaned_program_info['title'], cleaned_program_info['sub_title']))
    modify_epid = asyncio.create_task(modify_program_epid(program, cleaned_program_info['episode_id']))
    modify_thumb = asyncio.create_task(modify_program_thumb(program, cleaned_program_info['tmdb_show_data']))
    modify_tags = asyncio.create_task(modify_program_tags(program, cleaned_program_info['tags']))

    await modify_title
    await modify_epid
    await modify_thumb
    await modify_tags

def runparse():

    logger.info("EPGParse: running EPG parse")
    epg_path = os.getenv('EPG_PATH', "./epg.xml")

    if "http" in epg_path:
        with urlopen(epg_path) as f:
            tree = ET.parse(f)
            root = tree.getroot()
    else:
        tree = ET.parse(epg_path)
        root = tree.getroot()

    programs = root.findall('programme')

    async def mainConcurrent():
        tasks = [
            asyncio.create_task(modify_program_info(program))
            for program in programs
        ]
        await asyncio.wait(tasks)

    start = time.time()
    asyncio.run(mainConcurrent())
    elapsed_time = time.time() - start
    logger.info("EPGParse: elapsed_time:{0}".format(elapsed_time) + "[sec]")
    logger.info("EPGParse: average_time_spend:{0}".format(elapsed_time / len(programs)) + "[sec/program]")
    logger.info("EPGParse: total_programs:{0}".format(len(programs)) + "[programs]")

    tree.write('./epg_new.xml', encoding='UTF-8')