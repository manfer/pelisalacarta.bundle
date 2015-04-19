# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cuevana
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "pelisadicto"
__category__ = "F"
__type__ = "generic"
__title__ = "Pelisadicto"
__language__ = "ES"

DEBUG = config.get_setting("debug")
BASE_URL = "http://pelisadicto.com"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelisadicto.py] mainlist")

    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Portada",
            action = "agregadas",
            url = BASE_URL
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Por Género",
            action = "porGenero",
            url = BASE_URL
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Buscar",
            action = "buscar",
            url = BASE_URL
        )
    )
    
    return itemlist

def search(item,texto):
    logger.info("[pelisadicto.py] search")
    itemlist = []

    texto = texto.replace( " ", "+" )
    try:
        item.url = urlparse.urljoin( BASE_URL, "/buscar/%s" )
        item.url = item.url % texto
        itemlist.extend(agregadas(item))

        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def porGenero(item):
    itemlist = []

    data = scrapertools.cache_page(item.url)

    patron = '<li class="nav-header">Por género</li>.*?</ul>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    patron = '<li><a href="([^"]+)" title=".*?">(.*?)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(matches[0])

    for url, genero in matches:
        itemlist.append(
            Item(
                channel = __channel__,
                action = "agregadas",
                title = genero,
                url = urlparse.urljoin( BASE_URL, url )
            )
        )

    return itemlist

def agregadas(item):
    logger.info("[pelisadicto.py] agregadas")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)
    # Extrae las entradas
    patron  = '<li class="col-xs-6 col-sm-2.*?">.*?'
    patron += '<a href="(.*?)".*?src="(.*?)".*?alt="(.*?)".*?calidad">(.*?)<.*?</li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for url, thumbnail, title, calidad in matches:
        url = urlparse.urljoin( "http://pelisadicto.com/", url )
        thumbnail = urlparse.urljoin( "http://pelisadicto.com/", thumbnail )
        title = unicode( title, "utf-8" )
        itemlist.append(
            Item(
                channel = __channel__,
                action = "findvideos",
                title = title,
                fulltitle = title,
                url = url,
                thumbnail = thumbnail,
                plot = "",
                show = title,
                viewmode = "movie_with_plot"
            )
        )
    patron  = '<li class="active">.*?</li><li><span><a href="(.*?)"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)>0:
        url = urlparse.urljoin( item.url, matches[0] )
        itemlist.append(
            Item(
                channel = __channel__,
                action = "agregadas",
                title = u"Página siguiente >>",
                url = url
            )
        )

    return itemlist

def findvideos(item):
    logger.info("[pelisadicto.py] findvideos")
    itemlist = []

    data = re.sub(r"\n|\s{2}","",scrapertools.cache_page(item.url))

    patron = "<!-- SINOPSIS --> "
    patron += "<h2>[^<]+</h2> "
    patron += "<p>([^<]+)</p>"
    matches = re.compile(patron,re.DOTALL).findall(data)
    plot = matches[0]

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    patron = '<tr>.*?'
    patron += '<td><img src="(.*?)".*?<td>(.*?)</td>.*?<td>(.*?)</td>.*?<a href="(.*?)".*?</tr>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedidioma, scrapedcalidad, scrapedserver, scrapedurl in matches:
        idioma =""
        if "/img/1.png" in scrapedidioma: idioma="Castellano"
        if "/img/2.png" in scrapedidioma: idioma="Latino"
        if "/img/3.png" in scrapedidioma: idioma="Subtitulado"
        title = item.title + " ["+scrapedcalidad+"][" + idioma + "][" + scrapedserver + "]"
        itemlist.append( Item(channel=__channel__, action="play", title=title, fulltitle=title , url=scrapedurl , thumbnail="" , plot=plot , show = item.show) )
    return itemlist	

def play(item):
    logger.info("[pelisadicto.py] play")
    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
