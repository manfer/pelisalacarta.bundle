# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para turbovideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import jsunpack

def test_video_exists( page_url ):
    logger.info("[turbovideos.py] test_video_exists(page_url='%s')" % page_url)
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[turbovideos.py] url="+page_url)
    if not "embed" in page_url:
      page_url = page_url.replace("http://turbovideos.net/","http://turbovideos.net/embed-") + ".html"
    data = scrapertools.cache_page( page_url )
    media_url = scrapertools.get_match(data,'sources: \[\{file:"([^"]+)"')
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [turbovideos]",media_url])

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos  = 'http://turbovideos.net/([a-z0-9]+)'
    logger.info("[realvid.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[realvid]"
        url = "http://turbovideos.net/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'turbovideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)
            
    return devuelve

def test():

    video_urls = get_video_url("http://turbovideos.net/chd1akgq83ov")

    return len(video_urls)>0