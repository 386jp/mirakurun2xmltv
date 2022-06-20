from fastapi import APIRouter
from fastapi.responses import Response
from fastapi_utils.tasks import repeat_every
import xml.etree.ElementTree as ET
from app.controllers.epgparser import runparse as epgparser

router = APIRouter()

@router.on_event("startup")
@repeat_every(seconds=60 * 60 * 12) # 12 hour
def _parse_epg() -> None:
    epgparser()

@router.get("/")
def get_cleaned_xmltv():
    tree = ET.parse("./epg_new.xml")
    root = tree.getroot()
    data = ET.tostring(root, encoding='utf8', method='xml')

    return Response(content=data, media_type="application/xml")