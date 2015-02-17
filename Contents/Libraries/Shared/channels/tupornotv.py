# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para tupornotv
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os
import sys
from servers import servertools
#from platformcode.xbmc import xbmctools
from core import config
from core.item import Item
from core import logger
#from pelisalacarta import buscador

from core import scrapertools

__channel__ = "tupornotv"
__category__ = "F"
__type__ = "generic"
__title__ = "tuporno.tv"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[tupornotv.py] mainlist")
    
    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Categorías",
            action = "categorias",
            url = "http://tuporno.tv/categorias/",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Nube de Tags",
            action = "categorias",
            url = "http://tuporno.tv/tags/",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Top Videos (más votados)",
            action = "masVotados",
            url = "http://tuporno.tv/topVideos/",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Populares (más vistos)",
            action = "masVistos",
            url = "http://tuporno.tv/",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Videos Recientes",
            action = "novedades",
            url = "http://tuporno.tv/videosRecientes/",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Pendientes de Votación",
            action = "novedades",
            url = "http://tuporno.tv/pendientes"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Buscar",
            action = "search"
        )
    )

    return itemlist

def novedades(item):
    logger.info("[tupornotv.py] novedades")
    url = item.url
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)
    
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    # seccion novedades
    '''
    <table border="0" cellpadding="0" cellspacing="0" ><tr><td align="center" width="100%" valign="top" height="160px">
    <a href="/videos/cogiendo-en-el-bosque"><img src="imagenes/videos//c/o/cogiendo-en-el-bosque_imagen2.jpg" alt="Cogiendo en el bosque" border="0" align="top" /></a>
    <h2><a href="/videos/cogiendo-en-el-bosque">Cogiendo en el bosque</a></h2>
    '''

    # capturar listado de vídeos completo
    patronvideos  = '<div class="grid_12 listado_videos">(.*?)</div>\s+<div class="grid_4 lateral'
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)

    # extraer cada uno de los vídeos del listado
    patronvideos  = '<div class="relative">(.*?<div class="duracion">\d+:\d+</div>)\s+</div>'
    matches = re.compile(patronvideos,re.DOTALL).findall(matches[0])

    itemlist = []
    for match in matches:
        # Titulo
        try:
            scrapedtitle = re.compile('title="(.+?)"').findall(match)[0]
            scrapedtitle = unicode( scrapedtitle, "Latin1" )
        except:
            scrapedtitle = ''
        try:
            scrapedurl = re.compile('href="(.+?)"').findall(match)[0]
            scrapedurl = urlparse.urljoin(url,scrapedurl)
        except:
            continue
        try:
            scrapedthumbnail = re.compile('src="(.+?)"').findall(match)[0]
            scrapedthumbnail = urlparse.urljoin(url,scrapedthumbnail)
        except:
            scrapedthumbnail = ''
        scrapedplot = ""
        try:
            duracion = re.compile('<div class="duracion">(.+?)<').findall(match)[0]
        except:
            try:
                duracion = re.compile('\((.+?)\)<br').findall(match[3])[0]
            except:
                duracion = ""
             
        #logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"], duracion=["+duracion+"]")
        # Añade al listado de XBMC
        #trozos = scrapedurl.split("/")
        #id = trozos[len(trozos)-1]
        #videos = "http://149.12.64.129/videoscodiH264/"+id[0:1]+"/"+id[1:2]+"/"+id+".flv"
        itemlist.append(
            Item(
                channel = __channel__,
                action="play",
                title = scrapedtitle + " [" + duracion + "]",
                url = scrapedurl,
                thumbnail = scrapedthumbnail,
                plot = scrapedplot,
                server = "Directo",
                folder = False
            )
        )

    # ------------------------------------------------------
    # Extrae el paginador
    # ------------------------------------------------------
    #<a href="/topVideos/todas/mes/2/" class="enlace_si">Siguiente </a>
    patronsiguiente = '<a href="([^"]+)" class="enlace_si">Siguiente </a>'
    siguiente = re.compile(patronsiguiente,re.DOTALL).findall(data)
    if len(siguiente) > 0:
        scrapedurl = urlparse.urljoin( url, siguiente[0] )
        itemlist.append(
            Item(
                channel = __channel__,
                action = "novedades",
                title = u"Página siguiente >>",
                url = scrapedurl,
                folder = True
            )
        )

    return itemlist

def masVistos(item):
    logger.info("[tupornotv.py] masVistos")
    
    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Hoy",
            action = "novedades",
            url = "http://tuporno.tv/hoy",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Recientes",
            action = "novedades",
            url = "http://tuporno.tv/recientes",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Semana",
            action = "novedades",
            url = "http://tuporno.tv/semana",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Mes",
            action = "novedades",
            url = "http://tuporno.tv/mes",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Año",
            action = "novedades",
            url = "http://tuporno.tv/ano",
            folder = True
        )
    )

    return itemlist

def categorias(item):
    logger.info("[tupornotv.py] categorias")
    
    
    url=item.url
    # ------------------------------------------------------
    # Descarga la página
    # ------------------------------------------------------
    data = scrapertools.cachePage(url)
    #logger.info(data)
    # ------------------------------------------------------
    # Extrae las entradas
    # ------------------------------------------------------
    # seccion categorias
    # Patron de las entradas
    if url == "http://tuporno.tv/categorias/":
        patronvideos = '<div class="cat">'
        patronvideos += '<a href="([^"]+)">'      # URL
        patronvideos += '<div>([^<]+)</div>'      # TITULO
    else:
        patronvideos  = '<a href="(.tags[^"]+)"'     # URL
        patronvideos += ' class="[^"]+">([^<]+)</a>' # TITULO
    
    matches = re.compile(patronvideos,re.DOTALL).findall(data)
    #if DEBUG: scrapertools.printMatches(matches)
    
    itemlist = []
    for match in matches:
        if match[1] in ["SexShop","Videochat","Videoclub","Webcams","Tuporno","Video","Amigoxxx","Relatos"]:
            continue
        # Titulo
        scrapedtitle = unicode( match[1], "Latin1" )
        scrapedurl = urlparse.urljoin(url,match[0])
        scrapedthumbnail = ""
        scrapedplot = ""
        logger.info("title=["+scrapedtitle+"], url=["+scrapedurl+"], thumbnail=["+scrapedthumbnail+"]")
    
        # Añade al listado de XBMC
        itemlist.append(
            Item(
                channel = __channel__,
                action = "novedades",
                title = scrapedtitle.capitalize(),
                url = scrapedurl,
                thumbnail = scrapedthumbnail,
                plot = scrapedplot,
                folder = True
            )
        )
    return itemlist

def masVotados(item):
    logger.info("[tupornotv.py] masVotados")
    
    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Hoy",
            action = "novedades",
            url = "http://tuporno.tv/topVideos/todas/hoy",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Recientes",
            action = "novedades",
            url = "http://tuporno.tv/topVideos/todas/recientes",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Semana",
            action = "novedades",
            url = "http://tuporno.tv/topVideos/todas/semana",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Mes",
            action = "novedades",
            url = "http://tuporno.tv/topVideos/todas/mes",
            folder = True
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            title = "Año",
            action = "novedades",
            url = "http://tuporno.tv/topVideos/todas/ano",
            folder = True
        )
    )

    return itemlist

def search(item,texto):
    logger.info("[tupornotv.py] search")
    itemlist = []

    texto = texto.replace( " ", "+" )
    try:
        # Series
        item.url = "http://tuporno.tv/buscador/?str=%s"
        item.url = item.url % texto
        itemlist.extend(novedades(item))

        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def play(item):
    logger.info("[tupornotv.py] play")
    itemlist = []
    
    # Lee la pagina del video
    data = scrapertools.cachePage(item.url)
    codVideo = scrapertools.get_match(data,'body id="([^"]+)"')
    logger.info("codVideo="+codVideo)
    
    # Lee la pagina con el codigo
    # http://tuporno.tv/flvurl.php?codVideo=188098&v=MAC%2011,5,502,146
    url = "http://tuporno.tv/flvurl.php?codVideo="+codVideo+"&v=MAC%2011,5,502,146"
    data = scrapertools.cachePage(url)
    logger.info("data="+data)
    kpt = scrapertools.get_match(data,"kpt\=(.+?)\&")
    logger.info("kpt="+kpt)
    
    # Decodifica
    import base64
    url = base64.decodestring(kpt)
    logger.info("url="+url)

    itemlist.append(
        Item(
            channel = __channel__,
            action = "play",
            title = item.title,
            url = url,
            thumbnail = item.thumbnail,
            plot = item.plot,
            server = "Directo",
            folder = False
        )
    )

    return itemlist

# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_items = mainlist(Item())
    videos_items = novedades(mainlist_items[0])
    
    for video_item in videos_items:
        mirrors = play(video_item)
        if len(mirrors)>0:
            return True

    print "No hay ningún vídeo en la sección de novedades"
    return False
