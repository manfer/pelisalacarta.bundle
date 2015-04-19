# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Conector para meuvideos
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os

from core import scrapertools
from core import logger
from core import config
from core import jsunpack
import string
import time

def test_video_exists( page_url ):
    logger.info("[meuvideos] test_video_exists(page_url='%s')" % page_url)
    data = SaltarPubli(page_url)
    patron ='<div id="over_player_msg">([^"]+)<span id='
    logger.info(data)
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches) >0:
      Estado = matches[0].replace("<br>", "<br/>") 
      patron = "jah\('(.*?)'\,"
      matches = re.compile(patron,re.DOTALL).findall(data)
      data = scrapertools.downloadpage(matches[0])
      Estado = Estado + " "+ scrapertools.get_match(data,"html\('(.*?)'\)")
      logger.info(Estado)
      return False, Estado
 
    return True,""

def get_video_url( page_url , premium = False , user="" , password="", video_password="" ):
    logger.info("[meuvideos.py] url="+page_url)
    data = SaltarPubli(page_url)
    data = scrapertools.get_match(data,"return p}(.*?)'\)\)\)")
    patron ='\(\'(.*?)\'\,([0-9]+)\,([0-9]+)\,\'(.*?)\'\.'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for p, a, c, k in matches:
      c=int(c)
      a = int(a)
      while(c>0):
        c=c-1
        if k.split("|")[c]:
          patron = ur'\b'+int2base(c,a)+ur'\b'
          p = re.sub(patron, k.split("|")[c], p, re.UNICODE)    
      patron='setup\({file:"([^"]+)",'
      matches = re.compile(patron,re.DOTALL).findall(p)
      media_url=matches[0]

    
    video_urls = []
    video_urls.append( [ scrapertools.get_filename_from_url(media_url)[-4:]+" [meuvideos]",media_url])

    return video_urls
    
def SaltarPubli(page_url):
    data = scrapertools.cache_page( page_url )
    patron = '<Form method="POST">.{1}<input type="hidden" name="op" value="([^"]*)">.{1}<input type="hidden" name="usr_login" value="([^"]*)">.{1}<input type="hidden" name="id" value="([^"]*)">.{1}<input type="hidden" name="fname" value="([^"]*)">.{1}<input type="hidden" name="referer" value="([^"]*)">.{1}<input type="hidden" name="hash" value="([^"]*)">'
    matches = re.compile(patron,re.DOTALL).findall(data)
    time.sleep(3)
    media_url=""
    for op, usr_login, id, fname, referer, hash in matches:
      post=urllib.urlencode({"op":op,"usr_login":usr_login,"id":id,"fname":fname, "referer":referer,"hash":hash,"imhuman":"Proceed to video"})
      url = page_url
      data = scrapertools.cache_page(url,post=post)
    return data
    
def int2base(integer, base):
        if not integer: return '0'
        sign = 1 if integer > 0 else -1
        alphanum = string.digits + string.ascii_lowercase
        nums = alphanum[:base]
        res = ''
        integer *= sign
        while integer:
                integer, mod = divmod(integer, base)
                res += nums[mod]
        return ('' if sign == 1 else '-') + res[::-1]

# Encuentra vídeos del servidor en el texto pasado
def find_videos(data):
    # Añade manualmente algunos erróneos para evitarlos
    encontrados = set()
    devuelve = []

    patronvideos  = 'http://meuvideos.com/([a-z0-9A-Z]+)'
    logger.info("[meuvideos.py] find_videos #"+patronvideos+"#")
    matches = re.compile(patronvideos,re.DOTALL).findall(data)

    for match in matches:
        titulo = "[meuvideos]"
        url = "http://meuvideos.com/"+match
        if url not in encontrados:
            logger.info("  url="+url)
            devuelve.append( [ titulo , url , 'meuvideos' ] )
            encontrados.add(url)
        else:
            logger.info("  url duplicada="+url)

    return devuelve

def test():

    video_urls = get_video_url("http://meuvideos.com/yn1rwiz0rnux")

    return len(video_urls)>0