# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para sinluces
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
#------------------------------------------------------------
import urlparse,urllib2,urllib,re
import os,sys

from core import logger
from core import config
from core import scrapertools
from core import jsontools
from core.item import Item
from servers import servertools

__channel__ = "sinluces"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "Sinluces"
__language__ = "ES"

DEBUG = config.get_setting("debug")

host = "http://www.sinluces.com/"


def isGeneric():
    return True

def mainlist(item):
    logger.info("pelisalacarta.sinluces mainlist")
    itemlist = []
    title ="Estrenos"
    itemlist.append( Item(channel=__channel__, title=title      , action="peliculas", url="http://sinluces.com/page/1/", fanart="http://s17.postimg.org/rnup1a333/sinlestfan.jpg", thumbnail="http://s23.postimg.org/p1a2tyejv/sinlestthu.jpg"))
    '''
    title ="HD"
    itemlist.append( Item(channel=__channel__, title=title      , action="peliculas", url="http://www.sinluces.com/search/label/HD", fanart="http://s11.postimg.org/6736sxxr7/sinlhdfan.jpg", thumbnail="http://s12.postimg.org/d5w5ojuql/sinlhdth.jpg"))
    '''
    title ="Buscar"
    itemlist.append( Item(channel=__channel__, title=title      , action="search", url="", fanart="http://s22.postimg.org/3tz2v05ap/sinlbufan.jpg", thumbnail="http://s30.postimg.org/jhmn0u4jl/sinlbusthub.jpg"))
    
    

    
    
    
    return itemlist
def search(item,texto):
    logger.info("pelisalacarta.sinluces search")
    texto = texto.replace(" ","+")
    
    item.url = "http://sinluces.com/?s=%s" % (texto)
    try:
        return buscador(item)
    # Se captura la excepciÛn, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

def buscador(item):
    logger.info("pelisalacarta.sinluces buscador")
    itemlist = []
    
    
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron  = '<div class="movie"><div class="imagen"><img src="([^"]+)" '
    patron += 'alt="(.*?)".*?'
    patron += '<a href="([^"]+)".*?'
    patron += '<span class="icon-grade"></span>([^<]+)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 and  not "Error 404" in data:
        itemlist.append( Item(channel=__channel__, title="No hay resultados...", thumbnail ="http://s6.postimg.org/55zljwr4h/sinnoisethumb.png", fanart ="http://s6.postimg.org/avfu47xap/sinnoisefan.jpg",folder=False) )


    for scrapedthumbnail, scrapedtitle, scrapedurl, scrapedrate in matches:
        scrapedtitle = scrapedtitle + scrapedrate
        
        itemlist.append( Item(channel=__channel__, action="fanart", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail ,  viewmode="movie", extra=scrapedtitle, fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg", folder=True) )

    return itemlist
def peliculas(item,paginacion=True):
    logger.info("pelisalacarta.sinluces peliculas")
    itemlist = []
   
    
   
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron  = '<div class="movie"><div class="imagen"><img src="([^"]+)" '
    patron += 'alt="(.*?)".*?'
    patron += '<a href="([^"]+)".*?'
    patron += '<span class="icon-grade"></span>([^<]+)</div>'
    
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches)==0 and  not "Error 404" in data:
        itemlist.append( Item(channel=__channel__, title="No hay resultados...", thumbnail ="http://s6.postimg.org/55zljwr4h/sinnoisethumb.png", fanart ="http://s6.postimg.org/avfu47xap/sinnoisefan.jpg",folder=False) )
    
    
    for scrapedthumbnail, scrapedtitle, scrapedurl, scrapedrate in matches:
        scrapedtitle = scrapedtitle + scrapedrate
        
        itemlist.append( Item(channel=__channel__, action="fanart", title=scrapedtitle , url=scrapedurl , thumbnail=scrapedthumbnail ,  viewmode="movie",  fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg") )
        
        #paginacio
    

    # Extrae el paginador
    ## Paginación
    if  "Error 404" in data:
        itemlist.append( Item(channel=__channel__, title="No hay mas paginas...", thumbnail ="http://s6.postimg.org/55zljwr4h/sinnoisethumb.png", fanart ="http://s6.postimg.org/avfu47xap/sinnoisefan.jpg",folder=False) )
    else:
        current_page_number = int(scrapertools.get_match(item.url,'page/(\d+)'))
        item.url = re.sub(r"page/\d+","page/{0}",item.url)
            
        next_page_number = current_page_number +1
        next_page = item.url.format(next_page_number)
                    
        title= "Pagina siguiente>>"
        if  not "Error 404" in data:
            itemlist.append( Item(channel=__channel__, title=title, url=next_page, fanart="http://s30.postimg.org/4gugdsygx/sinlucesfan.jpg", thumbnail="http://s16.postimg.org/lvzzttkol/pelisvkflecha.png", action="peliculas", folder=True) )

    return itemlist

def fanart(item):
    logger.info("pelisalacarta.peliculasdk fanart")
    itemlist = []
    url = item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    title= scrapertools.get_match(data,'<title>Ver(.*?)pelic')
    title= re.sub(r"3D|SBS|-|","",title)
    title= title.replace('Ver','')
    title= title.replace('Online','')
    title= title.replace('Gratis','')
    title= title.replace(' ','%20')
    url="http://api.themoviedb.org/3/search/movie?api_key=57983e31fb435df4df77afb854740ea9&query=" + title + "&language=es&include_adult=false"
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patron = '"page":1.*?"backdrop_path":"(.*?)".*?,"id":(.*?),'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if len(matches)==0:
       extra=item.thumbnail
       show= item.thumbnail
       category= item.thumbnail
       itemlist.append( Item(channel=__channel__, title=item.title, url=item.url, action="findvideos", thumbnail=item.thumbnail, fanart=item.thumbnail ,extra=extra, show=show, category= category,folder=True) )
    else:
        for fan, id in matches:
            fanart="https://image.tmdb.org/t/p/original" + fan
            item.extra= fanart
    #fanart_2 y arts
                
            url ="http://assets.fanart.tv/v3/movies/"+id+"?api_key=6fa42b0ef3b5f3aab6a7edaa78675ac2"
            data = scrapertools.cachePage(url)
            data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
            patron = '"hdmovielogo":.*?"url": "([^"]+)"'
            matches = re.compile(patron,re.DOTALL).findall(data)
            if '"moviedisc"' in data:
                disc = scrapertools.get_match(data,'"moviedisc":.*?"url": "([^"]+)"')
            if '"movieposter"' in data:
                poster = scrapertools.get_match(data,'"movieposter":.*?"url": "([^"]+)"')
            if '"moviethumb"' in data:
                thumb = scrapertools.get_match(data,'"moviethumb":.*?"url": "([^"]+)"')
            if '"moviebanner"' in data:
                 banner= scrapertools.get_match(data,'"moviebanner":.*?"url": "([^"]+)"')
            
            if len(matches)==0:
               extra=  item.thumbnail
               show = item.extra
               category = item.extra

               itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=item.thumbnail, fanart=item.extra,  extra=extra, show=show, category= category, folder=True) )
        for logo in matches:
            if '"hdmovieclearart"' in data:
                clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                if '"moviebackground"' in data:
                    fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                    extra=clear
                    show= fanart_2
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                         category= clear
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show, category= category, folder=True) )
                else:
                    extra= clear
                    show=item.extra
                    if '"moviedisc"' in data:
                        category = disc
                    else:
                        category = clear
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show, category= category, folder=True) )

            if '"moviebackground"' in data:
                 fanart_2=scrapertools.get_match(data,'"moviebackground":.*?"url": "([^"]+)"')
                 if '"hdmovieclearart"' in data:
                     clear=scrapertools.get_match(data,'"hdmovieclearart":.*?"url": "([^"]+)"')
                     extra=clear
                     show= fanart_2
                     if '"moviedisc"' in data:
                         category= disc
                     else:
                          category= clear
                
                 else:
                       extra=logo
                       show= fanart_2
                       if '"moviedisc"' in data:
                            category= disc
                       else:
                            category= logo
                       itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra, extra=extra,show=show, category= category,  folder=True) )
    
            if not '"hdmovieclearart"' in data and not '"moviebackground"' in data:
                    extra= logo
                    show=  item.extra
                    if '"moviedisc"' in data:
                        category= disc
                    else:
                        category= item.extra
                    itemlist.append( Item(channel=__channel__, title = item.title , action="findvideos", url=item.url, server="torrent", thumbnail=logo, fanart=item.extra,category= category, extra=extra,show=show ,  folder=True) )

    title ="Info"
    if len(item.extra)==0:
       fanart=item.thumbnail
    else:
       fanart = item.extra
       plot= item.extra
    if '"movieposter"' in data:
        thumbnail= poster
    elif '"moviethumb"' in data:
          thumbnail = thumb
    
    else:
        thumbnail = item.thumbnail

    itemlist.append( Item(channel=__channel__, action="info" , title=title , url=item.url, thumbnail=thumbnail,  fanart=fanart, extra = extra, show = show,folder=False ))




    return itemlist






def findvideos(item):
    logger.info("pelisalacarta.sinluces findvideos")
    itemlist = []
    
    # Descarga la pagina
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    
        
       
    #extra enlaces
    
    
    patron= '<div class="play-c">(.*?)<div class="datos">'
    
    matches = re.compile(patron,re.DOTALL).findall(data)

    if not "hqq" in data:
        itemlist.append( Item(channel=__channel__, title="Sin servidores para Pelisalacarta...", thumbnail ="http://s6.postimg.org/55zljwr4h/sinnoisethumb.png", fanart ="http://s6.postimg.org/avfu47xap/sinnoisefan.jpg",folder=False) )
   
    for bloque_enlaces_idiomas in matches:
        patronenlaces= '<div id="play-(.*?)".*?src="([^"]+)"'
        matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(bloque_enlaces_idiomas)
        patronidiomas= '<a href="#play-(.*?)">([^<]+)'
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(bloque_enlaces_idiomas)
        for numero, scrapedurl in matchesenlaces:
            url=scrapedurl
            for numero2, idiomas in matchesidiomas:
                if numero == numero2:
                   title = idiomas
                   idiomas= re.sub(r"[0-9]","",idiomas)
                   listavideos = servertools.findvideos(url)
                   for video in listavideos:
                    
                       videotitle = scrapertools.unescape(video[0])+"-"+idiomas
                       url = video[1]
                       server = video[2]
                       title_first="Ver en--"
                       title= title_first + videotitle

                       itemlist.append( Item(channel=__channel__, action="play", server=server, title=title , url=url , thumbnail=item.extra , fulltitle = item.title , fanart = item.show, folder=False) )


        #otro patronenlaces
        patronenlaces= '<div id="play-(.*?)".*?src=\'([^\']+)\''
        matchesenlaces = re.compile(patronenlaces,re.DOTALL).findall(bloque_enlaces_idiomas)
        patronidiomas= '<a href="#play-(.*?)">([^<]+)'
        matchesidiomas = re.compile(patronidiomas,re.DOTALL).findall(bloque_enlaces_idiomas)
        for numero, url in matchesenlaces:
            pepe=url
            for numero2, idiomas in matchesidiomas:
                if numero == numero2:
                   title = idiomas
                   idiomas= re.sub(r"[0-9]","",idiomas)
                   listavideos = servertools.findvideos(pepe)
                   for video in listavideos:
                       
                       videotitle = scrapertools.unescape(video[0])+"-"+idiomas
                       url = video[1]
                       server = video[2]
                       title_first="Ver en--"
                       title= title_first + videotitle
                           
                       itemlist.append( Item(channel=__channel__, action="play", server=server, title=title , url=url , thumbnail=item.extra , fulltitle = item.title , fanart = item.show, folder=False) )
    

        patron = '<em>opción \d+, ([^<]+)</em>.*?'
        # Datos que contienen los enlaces para sacarlos con servertools.findvideos
        patron+= '<div class="contenedor_tab">(.*?)<div style="clear:both;">'
        matches = re.compile(patron,re.DOTALL).findall(data)
    
        for idioma, datosEnlaces in matches:
        
            listavideos = servertools.findvideos(datosEnlaces)
        
        
            for video in listavideos:
                videotitle = scrapertools.unescape(video[0])+"-"+idioma
                url = video[1]
                server = video[2]
                title_first="Ver en--"
                title= title_first + videotitle
                itemlist.append( Item(channel=__channel__, action="play", server=server, title=title , url=url , thumbnail=item.extra , fulltitle = item.title , fanart = item.show, folder=False) )



            
        
            



    return itemlist

def info(item):
    logger.info("pelisalacarta.sinluces trailer")
    url=item.url
    data = scrapertools.cachePage(url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    title= scrapertools.get_match(data,'<title>Ver(.*?)pelic')
    title = title.replace("Ver","")
    plot = scrapertools.get_match(data,'<h2>Sinopsis.*?<p>([^<]+).*?</p>')
   
    plot = plot.replace("</span>","")
    plot = plot.replace("</i>","")
    plot = plot.replace("&#8220","")
    plot = plot.replace("<b>","")
    plot = plot.replace("</b>","")
    plot = plot.replace(" &#8203;&#8203;","")
    plot = plot.replace("&#8230","")
    plot = plot.replace("</div> </div> <div class='clear'>","")
    plot = plot.replace("</div><div><span><i class='icon icon-ok'>","")
    foto = item.show
    photo= item.extra

    ventana2 = TextBox1(title=title, plot=plot, thumbnail=photo, fanart=foto)
    ventana2.doModal()

def test():
    return True



