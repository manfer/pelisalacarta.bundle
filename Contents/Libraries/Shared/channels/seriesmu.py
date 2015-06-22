# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para seriesmu
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
try:
    import xbmc
    import xbmcgui
except: pass

__channel__ = "seriesmu"
__category__ = "F,S,D"
__type__ = "generic"
__title__ = "SeriesMU"
__language__ = "ES"

DEBUG = config.get_setting("debug")
host = "http://series.mu/"
#Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:22.0) Gecko/20100101 Firefox/22.0
#DEFAULT_HEADERS = []
#DEFAULT_HEADERS.append( ["User-Agent","User-Agent=Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.6; es-ES; rv:1.9.2.12) Gecko/20101026 Firefox/3.6.12"] )



def isGeneric():
    return True

def login():
    url = "http://series.mu/login/"
    post = "user="+config.get_setting("seriesmuuser")+"&pass="+config.get_setting("seriesmupassword")
    data = scrapertools.cache_page(url,post=post)



def mainlist(item):
    logger.info("pelisalacarta.seriesmu mainlist")
    itemlist = []
    title ="Habilita tu cuenta en la configuración..."
    title = title.replace(title,bbcode_kodi2html("[COLOR greenyellow]"+title+"[/COLOR]"))
    if config.get_setting("seriesmuaccount")!="true":
        itemlist.append( Item( channel=__channel__ , title=title , action="openconfig" , url="" , fanart="http://s17.postimg.org/6d3kggvvj/smfanlog.jpg", thumbnail="http://s2.postimg.org/c678law6x/smloglog.jpg",  folder=False ) )
    else:
        login()
        title ="Mis Series"
        title = title.replace(title,bbcode_kodi2html("[COLOR aqua][B]"+title+"[/B][/COLOR]"))
        
        itemlist.append( Item(channel=__channel__, title=title      , action="mis_series", url="http://series.mu/catalogo/mis-series/1/", fanart="http://s27.postimg.org/agsoe4jir/smumsfan.jpg", thumbnail= "https://cdn4.iconfinder.com/data/icons/sabre/snow_sabre_black/512/folder_black_library.png"))
        title ="Series"
        title = title.replace(title,bbcode_kodi2html("[COLOR aqua][B]"+title+"[/B][/COLOR]"))
        
        itemlist.append( Item(channel=__channel__, title=title      , action="catalogo", url="http://series.mu/catalogo/series/1/", fanart="http://s12.postimg.org/eh5r2oefh/smsfan.jpg", thumbnail="https://lh3.googleusercontent.com/-eSiNj7X0wQU/AAAAAAAAAAI/AAAAAAAAAEM/iolph9ldX5w/photo.jpg"))
        title ="Peliculas"
        title = title.replace(title,bbcode_kodi2html("[COLOR aqua][B]"+title+"[/B][/COLOR]"))
        
        itemlist.append( Item(channel=__channel__, title=title     , action="catalogo", url="http://series.mu/catalogo/pelis/1/", fanart="http://s7.postimg.org/ybxhxdc0r/smpfan.jpg", thumbnail="http://cdn.flaticon.com/png/256/24949.png"))
       
        title ="Buscar..."
        title = title.replace(title,bbcode_kodi2html("[COLOR aqua][B]"+title+"[/B][/COLOR]"))
        
        itemlist.append( Item(channel=__channel__, title=title      , action="search", url="http://series.mu/search/", fanart="http://s7.postimg.org/9be35fm6z/smbfan.jpg", thumbnail="http://cdn.mysitemyway.com/etc-mysitemyway/icons/legacy-previews/icons/black-ink-grunge-stamps-textures-icons-people-things/060097-black-ink-grunge-stamp-textures-icon-people-things-eye6.png"))
    

    return itemlist

def openconfig(item):
    if "xbmc" in config.get_platform() or "boxee" in config.get_platform():
        config.open_settings( )
    return []
def bbcode_kodi2html(text):
    
    if config.get_platform().startswith("plex") or config.get_platform().startswith("mediaserver"):
        import re
        text = re.sub(r'\[COLOR\s([^\]]+)\]',
                      r'<span style="color: \1">',
                      text)
        text = text.replace('[/COLOR]','</span>')
        text = text.replace('[CR]','<br>')
        text = text.replace('[B]','<b>')
        text = text.replace('[/B]','</b>')
        text = text.replace('"color: yellow"','"color: gold"')
        text = text.replace('"color: white"','"color: auto"')
    
    return text


def search(item,texto):
    logger.info("pelisalacarta.seriesmu search")
    itemlist = []
    
    url = urlparse.urljoin(host, "/search/")
    post = 'post=yes' + '&q='+ texto[0:18]

    item.extra = post
    
    try:
        return buscador(item)
    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []



def buscador(item, ):
    itemlist = []
    logger.info("pelisalacarta.seriesmu buscador    ")
    # Descarga la página
    
    data = scrapertools.cache_page(item.url,post=item.extra)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    logger.info("data="+data)
    
    
    patron = '<a href="([^"]+)".*?'
    patron += 'src="([^"]+)".*?'
    patron += '<h2>(.*?)</h2>'
    
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches) == 0:
        itemlist.append( Item(channel=__channel__, title =bbcode_kodi2html("[COLOR skyblue][B]Sin resultados...[/B][/COLOR]"),fanart="http://s6.postimg.org/oy1rj72oh/pdknoisefan.jpg", thumbnail="http://s6.postimg.org/6kplh7brl/smnotallowed.png", folder=False ) )
    
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(host, scrapedurl)
        if "series" in scrapedurl:
            action= "episodios"
            
        if "peli" in scrapedurl:
                action="peliculas"
    
        itemlist.append( Item(channel=__channel__, title =scrapedtitle , url=scrapedurl, action=action, thumbnail= scrapedthumbnail, fanart="http://s21.postimg.org/gmwquc5hz/smfan2.jpg", show=scrapedtitle, folder=True) )

    return itemlist

def mis_series(item):
    logger.info("pelisalacarta.seriesmu mis_series")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    patron = '<div.*?class="col-md-2.*?media".*?>.*?'
    patron += '<a href="([^"]+)".*?'
    patron += 'src="([^"]+)".*?'
    patron += '<h2>(.*?)</h2>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        scrapedurl = urlparse.urljoin(host, scrapedurl)
        title = scrapedtitle.replace(scrapedtitle,bbcode_kodi2html("[COLOR sandybrown][B]"+scrapedtitle+"[/B][/COLOR]"))
        
        itemlist.append( Item(channel=__channel__, title =title , url=scrapedurl, action="episodios", thumbnail=scrapedthumbnail, fanart="http://s21.postimg.org/gmwquc5hz/smfan2.jpg", show=scrapedtitle,category = "mis_series", folder=True) )

    return itemlist

def catalogo(item):
    logger.info("pelisalacarta.seriesmu peliculas")
    itemlist = []
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    patronseries = 'Mis series</a></div>(.*?)</a></li></ul></div></div></div>'
    matchesseries = re.compile(patronseries,re.DOTALL).findall(data)
    
    for bloque_series in matchesseries:
        if (DEBUG): logger.info("bloque_series="+bloque_series)
        # Extrae las series
    
        patron = '<a href="([^"]+)".*?'
        patron += 'src="([^"]+)".*?'
        patron += '<h2>(.*?)</h2>.*?'
        patron += '<h3>([^<]+)</h3>'
    
    
        matches = re.compile(patron,re.DOTALL).findall(bloque_series)
        scrapertools.printMatches(matches)
    

        for scrapedurl, scrapedthumbnail, scrapedtitle, scrapedinfo in matches:
            scrapedinfo = scrapedinfo.replace(scrapedinfo,bbcode_kodi2html("[COLOR gold]"+scrapedinfo+"[/COLOR]"))
            title = scrapedtitle.replace(scrapedtitle,bbcode_kodi2html("[COLOR white]"+scrapedtitle+"[/COLOR]"))
            title = title +  " (" + scrapedinfo + ")"
            scrapedurl = urlparse.urljoin(host, scrapedurl)
            if "series" in scrapedurl:
                action= "episodios"
            
            if "peli" in scrapedurl:
                action="peliculas"
        
        
            itemlist.append( Item(channel=__channel__, title =title , url=scrapedurl, action=action, thumbnail=scrapedthumbnail, fanart="http://s21.postimg.org/gmwquc5hz/smfan2.jpg", show=scrapedtitle, folder=True) )
    ## Paginación
    try:
        next_page = scrapertools.get_match(data,'<a href="([^"]+)">Siguiente &rsaquo;</a></li></ul></div></div></div>')
        next_page = urlparse.urljoin(host, next_page)
        title= bbcode_kodi2html("[COLOR blue]>> Página siguiente[/COLOR]")
        itemlist.append( Item(channel=__channel__, title=title, url=next_page, action="catalogo" , fanart="http://s21.postimg.org/gmwquc5hz/smfan2.jpg", thumbnail="http://s21.postimg.org/pro3rcu6v/smarrow.jpg", folder=True) )
    except: pass
   

    return itemlist

def peliculas(item):
    logger.info("pelisalacarta.seriesmu temporadas")
    itemlist = []

    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)

    patron = '<div class="link-row">'
    patron += '<a href="([^"]+)".*?'
    patron += '<div class="host.*?([^<]+)"></div>.*?'
    patron += '<div class="lang audio">([^<]+)</div>.*?'
    patron += '<div class="quality">([^<]+)</div>'

    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)
    if len(matches) == 0:
        itemlist.append( Item(channel=__channel__, title =bbcode_kodi2html("[COLOR skyblue][B]No hay enlaces...[/B][/COLOR]"),fanart="http://s6.postimg.org/oy1rj72oh/pdknoisefan.jpg", thumbnail="http://s6.postimg.org/6kplh7brl/smnotallowed.png", folder=False ) )

    for scrapedurl, scrapedhost, scrapedaudio, scrapedcalidad in matches:
        scrapedhost= scrapedhost.replace("net","")
        scrapedhost= scrapedhost.replace("eu","")
        scrapedhost= scrapedhost.replace("sx","")
        puntuacion = scrapertools.get_match(data,'<li><div class="num" id="val-score">(.*?)</div>')
        puntuacion = puntuacion.replace(puntuacion,bbcode_kodi2html("[COLOR yellow]"+puntuacion+"[/COLOR]"))
        puntuacion_title = "Puntuación :"
        puntuacion_title = puntuacion_title.replace(puntuacion_title,bbcode_kodi2html("[COLOR pink]"+puntuacion_title+"[/COLOR]"))
        puntuacion = puntuacion_title + " " + puntuacion + "[CR]"
        scrapedplot = scrapertools.get_match(data,'<h2>(.*?)<div class="card media-chapters">')
        plotformat = re.compile('<p>(.*?)</p>',re.DOTALL).findall(scrapedplot)
        scrapedplot = scrapedplot.replace(scrapedplot,bbcode_kodi2html("[COLOR white]"+scrapedplot+"[/COLOR]"))
        for plot in plotformat:
            scrapedplot = scrapedplot.replace(plot,bbcode_kodi2html("[COLOR skyblue][B]"+plot+"[/B][/COLOR]"))
            scrapedplot = scrapedplot.replace("</h2><p>","[CR]")
            scrapedplot = scrapedplot.replace("</p></div>","")
        scrapedplot = puntuacion + scrapedplot
        scrapedhost = scrapedhost.replace(scrapedhost,bbcode_kodi2html("[COLOR burlywood]"+scrapedhost+"[/COLOR]"))
        scrapedaudio = scrapedaudio.replace(scrapedaudio,bbcode_kodi2html("[COLOR white]"+scrapedaudio+"[/COLOR]"))
        scrapedcalidad = scrapedcalidad.replace(scrapedcalidad,bbcode_kodi2html("[COLOR olive]"+scrapedcalidad+"[/COLOR]"))
        fanart = scrapertools.get_match(data,'<div class="media-cover" style="background-image: url\(http://series.mu([^"]+)\)')
        fanart = urlparse.urljoin(host, fanart)
        
        title = scrapedhost + "--" + scrapedaudio + "--" + scrapedcalidad
        itemlist.append( Item(channel=__channel__, action="play", title= title  , url=scrapedurl , thumbnail=item.thumbnail ,show=item.show, plot=scrapedplot, fanart=fanart, folder=True) )


    return itemlist


def episodios(item):
    logger.info("pelisalacarta.seriesmu episodios")
    itemlist = []
    
    
    # Descarga la página
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    
    seguir = scrapertools.get_match(data,'<ul><li text="Siguiendo" color="green" class="([^"]+)"')
    abandonar = scrapertools.get_match(data,'<li text="Abandonada" color="red" class="([^"]+)">')

    fanart = scrapertools.get_match(data,'<div class="media-cover" style="background-image: url\(http://series.mu([^"]+)\)')
    fanart = urlparse.urljoin(host, fanart)
    seguir = urlparse.urljoin(host, seguir)
    abandonar = urlparse.urljoin(host, abandonar)
   
    if not item.title.endswith("XBMC"):
        if '<div class=""></div>' in data:
           url = seguir
           title = bbcode_kodi2html("[COLOR yellow]Seguir[/COLOR]")
           thumbnail= "http://s14.postimg.org/ca5boj275/smseguir.png"
        else:
            url = abandonar
            title = bbcode_kodi2html("[COLOR green]Siguiendo[/COLOR]: [COLOR red]Abandonar[/COLOR]")
            thumbnail="http://s18.postimg.org/hh4l8hj1l/smabandonar2.png"
    
        itemlist.append( Item(channel=item.channel, title=title, url=url, fanart=fanart, thumbnail=thumbnail, action="cambiar_estado", extra=item.url, folder=False))




    patrontemporada = '<ul (temp[^<]+)>(.*?)</ul>'
    matchestemporadas = re.compile(patrontemporada,re.DOTALL).findall(data)
    
    for nombre_temporada,bloque_episodios in matchestemporadas:
        if (DEBUG): logger.info("nombre_temporada="+nombre_temporada)
        if (DEBUG): logger.info("bloque_episodios="+bloque_episodios)
        # Extrae los episodios
        
    
        patron = '<span>(.*?)'
        patron += '</span>([^<]+).*?'
        patron += '<i class="(.*?)".*?'
        patron += '<i class="icon-play".*?'
        patron += 'href="([^"]+)"'
    
    
        matches = re.compile(patron,re.DOTALL).findall(bloque_episodios)
        scrapertools.printMatches(matches)
    
        for scrapednumber, scrapedtitle, scrapedeyes, scrapedurl in matches:
        
            if "open" in scrapedeyes:
               scrapedeyes = re.sub(r"eye-w icon-eye-open",bbcode_kodi2html("[COLOR salmon]"+" [Visto]"+"[/COLOR]"),scrapedeyes)
            if "close" in scrapedeyes:
               scrapedeyes = re.sub(r"eye-w icon-eye-close",bbcode_kodi2html("[COLOR chartreuse]"+" [Pendiente]"+"[/COLOR]"),scrapedeyes)
           
            title = nombre_temporada + "X" + scrapednumber + scrapedtitle + scrapedeyes
            title = title.replace("temp=","Temporada ")
            title = title.replace(scrapedtitle,bbcode_kodi2html("[COLOR white]"+scrapedtitle+"[/COLOR]"))
            puntuacion = scrapertools.get_match(data,'<li><div class="num" id="val-score">(.*?)</div>')
            puntuacion = puntuacion.replace(puntuacion,bbcode_kodi2html("[COLOR yellow]"+puntuacion+"[/COLOR]"))
            puntuacion_title = "Puntuación :"
            puntuacion_title = puntuacion_title.replace(puntuacion_title,bbcode_kodi2html("[COLOR pink]"+puntuacion_title+"[/COLOR]"))
            puntuacion = puntuacion_title + " " + puntuacion + "[CR]"
            scrapedplot = scrapertools.get_match(data,'<h2>(.*?)<div class="card media-chapters">')
            plotformat = re.compile('<p>(.*?)</p>',re.DOTALL).findall(scrapedplot)
            scrapedplot = scrapedplot.replace(scrapedplot,bbcode_kodi2html("[COLOR white]"+scrapedplot+"[/COLOR]"))
            for plot in plotformat:
                scrapedplot = scrapedplot.replace(plot,bbcode_kodi2html("[COLOR skyblue][B]"+plot+"[/B][/COLOR]"))
                scrapedplot = scrapedplot.replace("</h2><p>","[CR]")
                scrapedplot = scrapedplot.replace("</p></div>","")
            scrapedplot = puntuacion + scrapedplot
            fanart = scrapertools.get_match(data,'<div class="media-cover" style="background-image: url\(http://series.mu([^"]+)\)')
            fanart = urlparse.urljoin(host, fanart)
            scrapedurl = urlparse.urljoin(host, scrapedurl)
        
            if scrapedtitle != " ": itemlist.append( Item(channel=__channel__, title =title , url=scrapedurl, action="findvideos", thumbnail=item.thumbnail, plot=scrapedplot, fanart=fanart, show=item.show.strip(), folder=True) )
    if (config.get_platform().startswith("xbmc") or config.get_platform().startswith("boxee")) and len(itemlist)>0:
       itemlist.append( Item(channel=__channel__, title="Añadir esta serie a la biblioteca de XBMC", url=item.url, action="add_serie_to_library", extra="episodios", show=item.show) )
    



    
    

    
    return itemlist

def cambiar_estado(item):
    logger.info("pelisalacarta.seriesmu cambiar_estado")
    
    ## Solicitar Seguir
    data = scrapertools.cache_page(item.url)



    if  "Seguir" in item.title:
        fanart= "http://s6.postimg.org/mchq3cdsh/Siguendomax.png"
        thumbnail ="http://s6.postimg.org/qbqvlwatp/mu2.png"
    
    else:
        fanart= "http://s6.postimg.org/ssqotfmc1/abandonadamax.png"
        thumbnail ="http://s6.postimg.org/7i52owclp/image.png"
    ventana = TextBox2(fanart=fanart, thumbnail=thumbnail)
    
    if item.category == "mis_series":
        xbmc.executebuiltin( "XBMC.Action(back)" )
        xbmc.executebuiltin( "Container.Refresh" )
    else:
        ## Kodi: Refrescar contenedor
        xbmc.executebuiltin( "Container.Refresh" )
        ## Restaurar la url de la serie
        item.url = item.extra
        return episodios(item)
try:
    class TextBox2( xbmcgui.WindowDialog ):
            """ Create a skinned textbox window """
            def __init__( self, *args, **kwargs):
                self.getFanart = kwargs.get('fanart')
                self.getThumbnail = kwargs.get('thumbnail')
            
                self.background = xbmcgui.ControlImage( 330, 30, 600 , 230, 'http://s6.postimg.org/4ub10su6p/ventanucosm.png')
                self.fanart = xbmcgui.ControlImage( 370, 80, 260, 50, self.getFanart )
                self.thumbnail = xbmcgui.ControlImage( 665, 50, 220, 200, self.getThumbnail )
            
            
                self.addControl(self.background)
                self.addControl(self.fanart)
                self.addControl(self.thumbnail)
        
        
        
                self.show(self)
                import time
                time.sleep(3)
                self.close(self)
except: pass









def findvideos(item):
    logger.info("pelisalacarta.seriesmu findvideos")
    
    itemlist = []
    # Descarga la pagina
   
    data = scrapertools.cache_page(item.url)
    data = re.sub(r"\n|\r|\t|\s{2}|&nbsp;","",data)
    
    patronlinks = '<div class="sections episode-links online shown">(.*?)<div class="sections episode-comments">'
    matcheslinks = re.compile(patronlinks,re.DOTALL).findall(data)
    
    for bloque_links in matcheslinks:
        if (DEBUG): logger.info("bloque_links="+bloque_links)
        # Extrae los episodios
        
        patron = '<li><div class="link-row">'
        patron += '<a href="([^"]+)".*?'
        patron += '<div class="host.*?([^<]+)"></div>.*?'
        patron += '<div class="lang audio">([^<]+)</div>.*?'
        patron += '<div class="quality">([^<]+)</div></a></div></li>'
    
    
        matches = re.compile(patron,re.DOTALL).findall(data)
        scrapertools.printMatches(matches)
        if len(matches) == 0:
           itemlist.append( Item(channel=__channel__, title =bbcode_kodi2html("[COLOR skyblue][B]No hay enlaces...[/B][/COLOR]"),fanart="http://s6.postimg.org/oy1rj72oh/pdknoisefan.jpg", thumbnail="http://s6.postimg.org/6kplh7brl/smnotallowed.png", folder=False ) )
        

        for scrapedurl, scrapedhost, scrapedaudio, scrapedcalidad in matches:
            scrapedhost= scrapedhost.replace("net","")
            scrapedhost= scrapedhost.replace("eu","")
            scrapedhost= scrapedhost.replace("sx","")
            scrapedhost = scrapedhost.replace(scrapedhost,bbcode_kodi2html("[COLOR burlywood]"+scrapedhost+"[/COLOR]"))
            scrapedaudio = scrapedaudio.replace(scrapedaudio,bbcode_kodi2html("[COLOR white]"+scrapedaudio+"[/COLOR]"))
            scrapedcalidad = scrapedcalidad.replace(scrapedcalidad,bbcode_kodi2html("[COLOR olive]"+scrapedcalidad+"[/COLOR]"))
            scrapedurl = urlparse.urljoin(host, scrapedurl)
            
            title = scrapedhost + "--" + scrapedaudio + "--" + scrapedcalidad
            
            

            itemlist.append( Item(channel=__channel__, action="play", title= title  , url=scrapedurl , thumbnail=item.thumbnail , fanart=item.fanart, folder=True) )



   



    return itemlist

def play(item):
    logger.info("pelisalacarta.seriesmu play")

    media_url = scrapertools.get_header_from_response(item.url,header_to_get="Location")
    itemlist = servertools.find_video_items(data=media_url)

    if len(itemlist) == 0:
        itemlist = servertools.find_video_items(data=item.url)
    
    
        
    return itemlist






