# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para spruto.tv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config

def test_video_exists( page_url ):
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[sprutotv.py] get_video_url(page_url='%s')" % page_url)
    video_urls = []
    # Descarga la página del vídeo
    data = scrapertools.cache_page(page_url)
    print page_url
    # Busca el vídeo de dos formas distintas
    patronvideos  = '\.setup\(\{[\n]*[ ]*file\: "([^"]+)",[\n]*[ ]*image\:'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    
    for media_url in matches:
        video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [sprutotv]",media_url])
        
    for video_url in video_urls:
        logger.info("[sprutotv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []

    patronvideos  = '(www.spruto.tv/iframe_embed.php\?video_id=[0-9]+)'
    logger.info("[sprutotv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[spruto.tv]"
        url = "http://"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'sprutotv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    

    return devuelve
