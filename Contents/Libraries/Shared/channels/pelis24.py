# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para pelis24
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item

__channel__ = "pelis24"
__category__ = "F,S"
__type__ = "generic"
__title__ = "Pelis24"
__language__ = "ES"

DEBUG = config.get_setting("debug")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[pelis24.py] mainlist")

    itemlist = []
    itemlist.append( Item(channel=__channel__, title="Recientes"      , action="peliculas"    , url="http://pelis24.com/index.php?do=lastnews"))
    itemlist.append( Item(channel=__channel__, title="Por A-Z"        , action="pelisaz"      , url="http://pelis24.com"))
    itemlist.append( Item(channel=__channel__, title="Por Categorias" , action="categorias"   , url="http://pelis24.com"))
    itemlist.append( Item(channel=__channel__, title="Por Calidades"  , action="calidades"    , url="http://pelis24.com"))
    itemlist.append( Item(channel=__channel__, title="Por Idiomas"    , action="idiomas"      , url="http://pelis24.com"))
    itemlist.append( Item(channel=__channel__, title="Buscar"         , action="search"       , url="http://pelis24.com"))
    return itemlist


def search(item,texto):
    logger.info("[pelis24.py] search")
 
    return buscar(item,texto)
  
def buscar(item, texto=""):
    if item.extra:
      post = item.extra
      texto = item.extra.split("=")[len(item.extra.split("="))-1]
    else:
      post= "do=search&subaction=search&story="+texto
    
    #post = "do=search&subaction=search&search_start=4&full_search=0&result_from=31&story=" + texto
    data = scrapertools.cache_page(item.url, post=post)

    patron = '<div class="base shortstory">(.*?)<div class="bsep">&nbsp;</div>'
    resultados = re.compile(patron,re.DOTALL).findall(data)
    itemlist = []
    for resultado in resultados:
      url, title = scrapertools.find_single_match(resultado,'<h3 class="btl"><a href="([^"]+)">(.*?)</a></h3>')
      plot = scrapertools.find_single_match(resultado,'<div>&nbsp;</div>\r\n<div>(.*?)<br />')
      title = re.sub('<[^>]+>',"",title)
      plot = re.sub('<[^>]+>',"",plot)
      
      if "table" in resultado:
        itemlist.append(Item(title=title, channel=__channel__,action="episodios", url=url,plot=plot,folder=True))
      else:
        itemlist.append(Item(title=title, channel=__channel__,action="findvideos", url=url,plot=plot,folder=True))
    
    next_page = scrapertools.find_single_match(data,'<a name="nextlink" id="nextlink" onclick="javascript:list_submit\(([^"]+)\); return\(false\)" href="#"><span class="thide pnext">Siguiente</span></a>')
    logger.info(next_page)
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="buscar", title=">> Pagina siguiente" , url=item.url,extra="do=search&subaction=search&search_start="+next_page+"&full_search=0&result_from="+str(((int(next_page)-1)*10)+1)+"&story=" +texto , folder=True) )
    
   
    return itemlist

  
def pelisaz(item):
    logger.info("[pelis24.py] pelisaz")
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,'<div align="center" style=" width:95%; margin-left:10px;">(.*?)\n\n</div>')
    patron = '<a href="([^"]+)"[^>]+>([^"]+)</a>'
    resultados = re.compile(patron,re.DOTALL).findall(data)
    itemlist =[]
    for url, letra in resultados:
      itemlist.append(Item(title=letra, channel=__channel__,action="peliculas", url=item.url+url,folder=True))
    return itemlist


def episodios(item):
    logger.info("[pelis24.py] episodios")
    data = scrapertools.cache_page(item.url)
    thumbnail = scrapertools.find_single_match(data,'<div class="image-block">\n  <img src="([^"]+)"')
    data = scrapertools.find_single_match(data,'<table (?:[^>]*)? style="border: 1px solid black;">(.*?)<div>')
    logger.info(data)

    patron = '<tr(.*?)</tr>'
    resultados = re.compile(patron,re.DOTALL).findall(data)
    itemlist =[]
    for resultado in resultados:
      if "href" in resultado:
        patron ='<a href="([^"]+)"(?:.*?)(Capitulo.+)'
        url, title = scrapertools.find_single_match(resultado,patron)
        
        title = re.sub('<[^>]+>',"",title)
        title = title.replace("&nbsp;"," ")

        itemlist.append(Item(title=title, channel=__channel__,action="findvideos", url=url,plot=item.plot, thumbnail=thumbnail, folder=True))

    return itemlist
 
 
def peliculas(item):
    logger.info("[pelis24.py] peliculas")
    itemlist = []
    data = scrapertools.cache_page(item.url)
    data = scrapertools.find_single_match(data,"<div id='dle-content'>(.*?<div class=\"navigation\">.*?)</div[^<]+</div[^<]+</div>") 
    patron  = '<div class="movie_box">(.*?)<div class="postbottom">'
    matches = re.compile(patron,re.DOTALL).findall(data)

    for bloque in matches:
        title = scrapertools.find_single_match(bloque,"<h3>([^<]+)</h3>")
        url = scrapertools.find_single_match(bloque,'<a href="([^"]+)"><img class="homethumb"')
        thumbnail = scrapertools.find_single_match(bloque,'<img class="homethumb" src="([^"]+)\n')
        plot = scrapertools.find_single_match(bloque,'<span class="pop_desc">(.*?)</span>')
        
        if "serie" in url:
          itemlist.append( Item(channel=__channel__, action="episodios", title=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movie_with_plot", folder=True) )        

        else:
          itemlist.append( Item(channel=__channel__, action="findvideos", title=title , url=url , thumbnail=thumbnail , plot=plot , viewmode="movie_with_plot", folder=True) )

    # Extrae el paginador
    next_page = scrapertools.find_single_match(data,'<a href="([^"]+)"><span class="thide pnext">')
    if next_page!="":
        itemlist.append( Item(channel=__channel__, action="peliculas", title=">> Pagina siguiente" , url=next_page , folder=True) )

    return itemlist


def categorias(item):
    logger.info("[pelis24.py] categorias")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<b>CATEGORIAS</b>(.*?)</ul>')

    patron = '<a href="([^"]+)"><b>([^<]+)</b></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
                                          
    for scrapedurl,scrapedtitle in matches:
        import HTMLParser
        url =  HTMLParser.HTMLParser().unescape(urlparse.urljoin(item.url,scrapedurl).decode("utf8")).encode("utf8")
        title = scrapedtitle.strip()
        title = title[0].upper() +  title[1:].lower()
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , folder=True) )

    return itemlist
    
    
def calidades(item):
    logger.info("[pelis24.py] calidades")
    itemlist = []
    itemlist.append( Item(channel=__channel__, action="peliculas", title="HD 720p" , url="http://pelis24.com/hd/", thumbnail="http://pelis24.com/images/menu_03.png" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="peliculas", title="HQ 480p" , url="http://pelis24.com/peliculas480p/", thumbnail="http://pelis24.com/images/menu_04.png" , folder=True) )
    itemlist.append( Item(channel=__channel__, action="peliculas", title="3D" , url="http://pelis24.com/pelicula-3d/", thumbnail="http://pelis24.com/images/menu_05.png" , folder=True) )

    return itemlist
   
    
def idiomas(item):
    logger.info("[pelis24.py] idiomas")
    itemlist = []
    data = scrapertools.cachePage(item.url)
    data = scrapertools.find_single_match(data,'<b>IDIOMAS</b>(.*?)</ul>')

    patron = '<a href="([^"]+)"><b>([^<]+)</b></a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
                                          
    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        title = scrapedtitle.strip()
        title = title[0].upper() +  title[1:].lower()
        itemlist.append( Item(channel=__channel__, action="peliculas", title=title , url=url , folder=True) )

    return itemlist
    
    
# Verificacion automatica de canales: Esta funcion debe devolver "True" si esta ok el canal.
def test():
    from servers import servertools
    
    # mainlist
    mainlist_items = mainlist(Item())
    # Da por bueno el canal si alguno de los videos de "Novedades" devuelve mirrors
    novedades_items = peliculas(mainlist_items[0])
    bien = False
    for novedades_item in novedades_items:
        mirrors = servertools.find_video_items( item=novedades_item )
        if len(mirrors)>0:
            bien = True
            break

    return bien
