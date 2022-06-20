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
