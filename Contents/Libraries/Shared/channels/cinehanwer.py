# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para cinehanwer
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

DEBUG = config.get_setting("debug")

__category__ = "A"
__type__ = "generic"
__title__ = "cinehanwer"
__channel__ = "cinehanwer"
__language__ = "ES"
__creationdate__ = "20140615"

def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.channels.cinehanwer mainlist")

    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            action = "peliculas",
            title = "Estrenos",
            url = "http://cinehanwer.com/estrenos/"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "peliculas",
            title = "Novedades",
            url = "http://cinehanwer.com"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "peliculas",
            title = "Más Vistas",
            url = "http://cinehanwer.com/inc/php/masvistas.php"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "peliculas",
            title = "Más Votadas",
            url = "http://cinehanwer.com/inc/php/masvotadas.php"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "alfabetico",
            title = "Por Orden Alfabético",
            url = "http://cinehanwer.com/estrenos/"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "calidades",
            title = "Por Calidad",
            url = "http://cinehanwer.com/estrenos/"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "generos",
            title = "Por Género",
            url = "http://cinehanwer.com/estrenos/"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "search",
            title = "Buscar...",
            url = "http://cinehanwer.com/estrenos/"
        )
    )
      
    return itemlist
    
def alfabetico(item):
    logger.info("pelisalacarta.channels.cinehanwer calidades")

    itemlist = []
    alfabeto = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','09']

    for letra in alfabeto:
        itemlist.append(
            Item(
                channel = __channel__,
                action = "peliculas",
                title = letra.upper(),
                url = "http://cinehanwer.com/letra/" + letra + ".html"
            )
        )

    return itemlist

def calidades(item):
    logger.info("pelisalacarta.channels.cinehanwer calidades")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div class="titc[^>]+>Buscar por C(.*?)</ul>')
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    patron  = '<li><a title="[^"]+" href="([^"]+)"><strong>([^<]+)</strong></a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append(
            Item(
                channel = __channel__,
                action = "peliculas",
                title = title,
                url = url
            )
        )

    return itemlist

def generos(item):
    logger.info("pelisalacarta.channels.cinehanwer generos")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div class="titc[^>]+>Buscar por G(.*?)</ul>')
    logger.info("data="+data)

    # Extrae las entradas (carpetas)
    patron  = '<li><a href="([^"]+)"[^>]+>([^<]+)</a></li>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,scrapedtitle in matches:
        title = scrapedtitle.strip()
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        itemlist.append(
            Item(
                channel = __channel__,
                action = "peliculas",
                title = title,
                url = url
            )
        )

    return itemlist

def search(item, texto):
    logger.info("pelisalacarta.channels.cinehanwer search")
    itemlist = []

    texto = texto.replace( " ", "+" )
    try:
        item.url = "http://cinehanwer.com/buscar/?q=%s"
        item.url = item.url % texto
        itemlist.extend( peliculas(item) )

        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def peliculas(item):
    logger.info("pelisalacarta.channels.cinehanwer peliculas")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    logger.info("data="+data)

    itemlist = []

    # Extrae las entradas
    '''
    <a href="/pelicula/3708/tarzan.html" title="Tarzan" >
    <img style="margin-top:0;" src="/files/uploads/3708.jpg" alt="" />
    <cite><center>Tarzan<br/><br><br><span class="txcnhd cowh dino" style=" color: #fff; ">
    <strong>Genero:</strong> Animacion<br>
    <strong>A&ntilde;o:</strong> 2014<br>
    <strong>Calidad:</strong> BR-Screener<br>
    <strong>Idiomas :</strong>  Espa&ntilde;ol
    '''
    patron = '<a href="([^"]+)" title="([^"]+)"[^<]+'
    patron += '<img style="[^"]+" src="([^"]+)"[^<]+'
    patron += '<cite>(.*?)</cite>'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for scrapedurl,scrapedtitle,scrapedthumbnail,scrapedplot in matches:
        title = scrapedtitle.strip()
        title = scrapertools.htmlclean(title)
        title = unicode( title, "Latin1" )
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        plot = scrapertools.htmlclean(scrapedplot)
        url = urlparse.urljoin(item.url,scrapedurl)
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append(
            Item(
                channel=__channel__,
                action="findvideos",
                title=title,
                url=url,
                thumbnail=thumbnail,
                plot=plot,
                fulltitle=title,
                viewmode="movie"
            )
        )

    #</b></span></a></li[^<]+<li><a href="?page=2">
    next_page = scrapertools.find_single_match(data,'</b></span></a></li[^<]+<li><a href="([^"]+)">')
    if next_page != "":
        itemlist.append(
            Item(
                channel = __channel__,
                action = "peliculas",
                title = u"Página siguiente >>",
                url = urlparse.urljoin( item.url, next_page ),
                folder = True
            )
        )

    return itemlist

def findvideos(item):
    logger.info("pelisalacarta.channels.cinehanwer findvideos")

    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)

    # Extrae las entradas (carpetas)  
    patron  = '<tr[^<]+'
    patron += '<td[^<]+<div[^<]+'
    patron += '<img[^<]+'
    patron += '<a href="([^"]+)"[^<]+</a></td[^<]+'
    patron += '<td[^<]+<img src="([^"]+)"</td[^<]+'
    patron += '<td[^<]+<img[^>]+>([^<]+)</td[^<]+'
    patron += '<td[^>]+>([^<]+)</td[^<]+'
    patron += '<td[^<]+</td[^<]+'
    patron += '<td[^<]+'
    patron += '<a title="Reportar este enlace"'
    matches = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    
    for scrapedurl,serverthumb,idioma,calidad in matches:
        idioma = idioma.strip()
        calidad = calidad.strip()
        nombre_servidor = serverthumb.split("/")[-1]

        title = "Ver en "+nombre_servidor+" ("+idioma+") (Calidad "+calidad+")"
        url = scrapedurl
        thumbnail = ""
        plot = ""
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")
        itemlist.append( Item(channel=__channel__, action="play" , title=title , url=url, thumbnail=thumbnail, plot=plot, folder=False))

    return itemlist

def play(item):
    logger.info("pelisalacarta.channels.cinehanwer play url="+item.url)

    itemlist = servertools.find_video_items(data=item.url)

    for videoitem in itemlist:
        videoitem.title = item.title
        videoitem.fulltitle = item.fulltitle
        videoitem.thumbnail = item.thumbnail
        videoitem.channel = __channel__

    return itemlist
