# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para netutv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os
import base64

from core import scrapertools
from core import logger
from core import config
from core import unpackerjs,unpackerjs3

SCRAPER_URL = "http://hqq.tv/player/embed_player.php"

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[netutv.py] url="+page_url)

    headers = [['User-Agent','Mozilla/5.0 (iPad; U; CPU OS 3_2 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Version/4.0.4 Mobile/7B334b Safari/531.21.10']]

    ### at
    id_video = page_url.split("=")[1]
    url_1 = SCRAPER_URL+"?vid="+id_video+"&autoplay=no"

    data = scrapertools.cache_page( url_1 , headers=headers )

    match_b64_1 = 'base64,([^"]+)"'
    b64_1 = scrapertools.get_match(data, match_b64_1)
    utf8_1 = base64.decodestring(b64_1)

    match_b64_inv = "='([^']+)';"
    b64_inv = scrapertools.get_match(utf8_1, match_b64_inv)
    b64_2 = b64_inv[::-1]
    utf8_2 = base64.decodestring(b64_2).replace("%","\\").decode('unicode-escape')

    match_at = '<input name="at" id="text" value="([^"]+)">'
    at = scrapertools.get_match(utf8_2, match_at)

    ### m3u8
    url_2 = SCRAPER_URL+"?vid="+id_video+"&at="+at+"&autoplayed=yes&referer=on&http_referer=http%3A%2F%2Fnetu.tv%2Fwatch_video.php%3Fv%3D"+id_video+"&pass="

    data = scrapertools.cache_page(url_2, headers=headers )

    match_b = '"#([^"]+)"'
    b = scrapertools.get_match(data, match_b)

    ### tb
    j = 0
    s2 = ""
    while j < len(b):
        s2+= "\\u0"+b[j:(j+3)]
        j+= 3
    s2 = s2.decode('unicode-escape')

    media_url = s2.encode('ASCII', 'ignore')

    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [netu.tv]",media_url])

    for video_url in video_urls:
        logger.info("[netutv.py] %s - %s" % (video_url[0],video_url[1]))

    return video_urls

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    encontrados = set()
    devuelve = []
    print "### data1: "+data

    # http://netu.tv/player/embed_player.php?vid=82U4BRSOB4UU&autoplay=no
    patronvideos  = 'netu.tv/player/embed_player.php\?vid\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(patronvideos)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    # http://netu.tv/watch_video.php?v=96WDAAA71A8K
    patronvideos  = 'netu.tv/watch_video.php\?v\=([A-Z0-9]+)'
    logger.info("[netutv.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[netu.tv]"
        url = "http://netu.tv/watch_video.php?v="+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'netutv' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://netu.tv/watch_video.php?v=82U4BRSOB4UU")

    return len(video_urls)>0