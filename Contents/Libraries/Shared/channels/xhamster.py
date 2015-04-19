# -*- coding: utf-8 -*-
#------------------------------------------------------------
# pelisalacarta - XBMC Plugin
# Canal para xhamster
# http://blog.tvalacarta.info/plugin-xbmc/pelisalacarta/
# Por boludiko
#------------------------------------------------------------
import cookielib
import urlparse,urllib2,urllib,re
import os
import sys
import unicodedata

from core import logger
from core import config
from core import scrapertools
from core.item import Item
from servers import servertools

__channel__ = "xhamster"
__category__ = "F"
__type__ = "generic"
__title__ = "xHamster"
__language__ = "ES"
__adult__ = "true"

DEBUG = config.get_setting("debug")

BASE_URL = "http://es.xhamster.com/"

def isGeneric():
    return True

def mainlist(item):
    logger.info("[xhamster.py] mainlist")
    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            action = "videos",
            title = "Novedades",
            url = BASE_URL
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "listorientacionsexual",
            title = "Categorías"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "videos",
            title = "Vídeos HD",
            url = urlparse.urljoin( BASE_URL, "/channels/new-hd_videos-1.html" )
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "videos",
            title = "Recomendados",
            url = urlparse.urljoin( BASE_URL, "/recommended_for_me.php" )
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "frecuencia",
            title = "Más Votados",
            url = urlparse.urljoin( BASE_URL, "/rankings/%s-top-videos.html" )
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "frecuencia",
            title = "Más Vistos",
            url = urlparse.urljoin( BASE_URL, "/rankings/%s-top-viewed.html" )
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "frecuencia",
            title = "Más Comentados",
            url = urlparse.urljoin( BASE_URL, "/rankings/%s-top-commented.html" )
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "search",
            title = "Buscar"
        )
    )
    return itemlist

# REALMENTE PASA LA DIRECCION DE BUSQUEDA

def search(item,texto):
    logger.info("[xhamster.py] search")
    itemlist = []

    texto = texto.replace( " ", "+" )
    try:
        # Series
        item.url = urlparse.urljoin( BASE_URL, "/search.php?q=%s&qcat=video" )
        item.url = item.url % texto
        itemlist.extend(videos(item))

        return itemlist

    # Se captura la excepción, para no interrumpir al buscador global si un canal falla
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line )
        return []

# SECCION ENCARGADA DE BUSCAR

def frecuencia(item):
    frecuencias = ["weekly", "montly", "alltime"]
    itemlist = []

    for frecuencia in frecuencias:
        itemlist.append(
            Item(
                channel = __channel__,
                action = "videos",
                title = frecuencia.title(),
                url = item.url % frecuencia
            )
        )

    return itemlist

def videos(item):
    #logger.info("[xhamster.py] videos")
    data = scrapertools.downloadpageWithoutCookies(item.url)
    #data = scrapertools.get_match(data,'<td valign="top" id="video_title">(.*?)<div id="footer">')
    itemlist = []

    '''
    <a href="/movies/1280051/pussy_pump_002.html?s=10" class='hRotator' >
    <img src='http://et1.xhamster.com/t/051/10_1280051.jpg' width='160' height='120' alt="pussy pump 002"/>
    <img class='hSprite' src="http://eu-st.xhamster.com/images/spacer.gif" width='160' height='120' sprite='http://et1.xhamster.com/t/051/s_1280051.jpg' id="1280051" onmouseover="hRotator.start2(this);">
    '''
    '''
    <a href='http://es.xhamster.com/movies/1627978/its_so_big_its_stretching_my_insides.html'  class='hRotator' >
    <img src='http://et18.xhamster.com/t/978/4_1627978.jpg' width='160' height='120' class='thumb' alt="Its So Big its Stretching My Insides"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et18.xhamster.com/t/978/s_1627978.jpg' id='1627978' onmouseover='hRotator.start2(this);'><b>12:13</b><u title="Its So Big its Stretching My Insides">Its So Big its Stretching My Insides</u></a><div class='hRate'><div class='fr'>94%</div>Views: 168,430</div></div><div class='video'><a href='http://es.xhamster.com/movies/1445375/busty_preggo_mom_dp_fuck.html'  class='hRotator' ><img src='http://et15.xhamster.com/t/375/3_1445375.jpg' width='160' height='120' class='thumb' alt="Busty preggo mom dp fuck"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et15.xhamster.com/t/375/s_1445375.jpg' id='1445375' onmouseover='hRotator.start2(this);'><b>13:38</b><u title="Busty preggo mom dp fuck">Busty preggo mom dp fuck</u></a><div class='hRate'><div class='fr'>93%</div>Views: 246,305</div></div><div class='video'><a href='http://es.xhamster.com/movies/745518/lauren_calendar_audition_netvideogirls.html'  class='hRotator' ><img src='http://et18.xhamster.com/t/518/2_745518.jpg' width='160' height='120' class='thumb' alt="Lauren Calendar Audition - netvideogirls"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et18.xhamster.com/t/518/s_745518.jpg' id='745518' onmouseover='hRotator.start2(this);'><b>46:25</b><u title="Lauren Calendar Audition - netvideogirls">Lauren Calendar Audition - netvideogirls</u></a><div class='hRate'><div class='fr'>95%</div>Views: 691,072</div></div><div class='clear' /></div><div class='video'><a href='http://es.xhamster.com/movies/1609732/pantyhose_hooker_nylon_prostitute_fetish_sex.html'  class='hRotator' ><img src='http://et12.xhamster.com/t/732/5_1609732.jpg' width='160' height='120' class='thumb' alt="pantyhose hooker nylon prostitute fetish sex"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et12.xhamster.com/t/732/s_1609732.jpg' id='1609732' onmouseover='hRotator.start2(this);'><b>13:02</b><u title="pantyhose hooker nylon prostitute fetish sex">pantyhose hooker nylon prostitute fetish sex</u><div class="hSpriteHD"></div></a><div class='hRate'><div class='fr'>95%</div>Views: 232,148</div></div><div class='video'><a href='http://es.xhamster.com/movies/1670755/tattooed_and_pierced_lesbians_licking_pussies.html'  class='hRotator' ><img src='http://et15.xhamster.com/t/755/7_1670755.jpg' width='160' height='120' class='thumb' alt="tattooed and pierced lesbians licking pussies"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et15.xhamster.com/t/755/s_1670755.jpg' id='1670755' onmouseover='hRotator.start2(this);'><b>13:32</b><u title="tattooed and pierced lesbians licking pussies">tattooed and pierced lesbians licking pussies</u></a><div class='hRate'><div class='fr'>92%</div>Views: 68,202</div></div><div class='video'><a href='http://es.xhamster.com/movies/1460297/brunette_en_jupe_jaune_baise_dehors.html'  class='hRotator' ><img src='http://et17.xhamster.com/t/297/6_1460297.jpg' width='160' height='120' class='thumb' alt="Brunette en jupe jaune baise dehors"/><img class='hSprite' src='http://eu-st.xhamster.com/images/spacer.gif' width='160' height='120' sprite='http://et17.xhamster.com/t/297/s_1460297.jpg' id='1460297' onmouseover='hRotator.start2(this);'><b>13:31</b><u title="Brunette en jupe jaune baise dehors">Brunette en jupe jaune baise dehors</u></a><div class='hRate'><div class='fr'>91%</div>Views: 64,222</div></div><div class='clear' /></div><div class="loader"></div>
    '''

    patron = "<a href='([^']+)'[^<]+<img src='([^']+)' width='[^']+' height='[^']+' class='[^']+' alt=\"([^\"]+)\""
    matches = re.compile(patron,re.DOTALL).findall(data)
    for scrapedurl, scrapedthumbnail, scrapedtitle in matches:
        try:
            #title = unicode( scrapedtitle, "utf-8" ).encode( "iso-8859-1" )
            title = scrapedtitle.strip()
        except:
            title = scrapedtitle
        title = unicode( title, "utf-8" )
        url = urlparse.urljoin( BASE_URL, scrapedurl )
        thumbnail = scrapedthumbnail
        plot = ""
        # Depuracion
        #if (DEBUG): logger.info("title=["+title+"], url=["+url+"], thumbnail=["+thumbnail+"]")            
        itemlist.append(
            Item(
                channel = __channel__,
                action = "play",
                title = title,
                fulltitle = title,
                url = url,
                thumbnail = thumbnail,
                plot = plot,
                show = title,
                viewmode = "movie",
                folder = False
            )
        )

    # EXTRAE EL PAGINADOR
    #<a href="/channels/new-grannies-2.html" class="last colR"><div class="icon iconPagerNextHover"></div>Próximo</a>
    #<a href="/channels/new-grannies-479.html" class="last" overicon="iconPagerNextHover"><div class="icon iconPagerNext"></div>Próximo</a>
    patronvideos = "<a href='([^']+)' class='last(?: colR)?'(?: overicon='iconPagerNextHover')?><div class='icon iconPagerNext"
    siguiente = re.compile(patronvideos,re.DOTALL).findall(data)
    scrapertools.printMatches(siguiente)
    if len(siguiente)>0:
        itemlist.append(
            Item(
                channel = __channel__,
                action = 'videos',
                title = u"Página siguiente >>",
                url = urlparse.urljoin( BASE_URL, siguiente[0] ),
                thumbnail = "",
                plot = "",
                folder = False
            )
        )
    else:
        paginador = None

    return itemlist

# SECCION ENCARGADA DE VOLCAR EL LISTADO DE CATEGORIAS CON EL LINK CORRESPONDIENTE A CADA PAGINA
def listorientacionsexual(item):
    logger.info("[xhamster.py] listorientacinosexual")
    itemlist = []
    itemlist.append(
        Item(
            channel = __channel__,
            action = "listcategorias",
            title = "Heterosexual"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "listcategorias",
            title = "Transexuales"
        )
    )
    itemlist.append(
        Item(
            channel = __channel__,
            action = "listcategorias",
            title = "Gays"
        )
    )
    return itemlist

def listcategorias(item):
    logger.info("[xhamster.py] listcategorias")
    itemlist = []
    unsorted = {}

    data = scrapertools.cachePage( urlparse.urljoin( BASE_URL, '/channels.php' ) )
    data = scrapertools.find_single_match(data,'<div class="title">' + item.title + '</div>\s+</div>\s+<div class="list">(.*?)</div>\s+<div')
    #logger.debug(data)

    patron  = '<a class="btnBig" href="([^"]+)">([^"]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    scrapertools.printMatches(matches)

    for scrapedurl, scrapedcategory in matches:
        itemlist.append(
            Item(
                channel = __channel__,
                action = "videos",
                title = scrapedcategory.strip(),
                extra = remove_accents( scrapedcategory.strip() ),
                url = urlparse.urljoin( BASE_URL, scrapedurl )
            )
        )
    itemlist = sorted(itemlist, key=lambda Item: Item.extra)

    return itemlist

# OBTIENE LOS ENLACES SEGUN LOS PATRONES DEL VIDEO Y LOS UNE CON EL SERVIDOR
def play(item):
    logger.info("[xhamster.py] play")
    itemlist = []

    data = scrapertools.cachePage(item.url)
    #logger.debug(data)

    url = scrapertools.get_match(data,'<video poster="[^"]+" type=\'video/mp4\' file="([^"]+)"')
    logger.debug("url=" + url)

    itemlist.append(
        Item(
            channel = __channel__,
            action = "play",
            title = item.title,
            fulltitle = item.fulltitle,
            url = url,
            thumbnail = item.thumbnail,
            plot = item.plot,
            show = item.title,
            server = "directo",
            folder = False
        )
    )

    return itemlist


# Verificación automática de canales: Esta función debe devolver "True" si todo está ok en el canal.
def test():
    bien = True

    # mainlist
    mainlist_itemlist = mainlist(Item())
    video_itemlist = videos(mainlist_itemlist[0])
    
    # Si algún video es reproducible, el canal funciona
    for video_item in video_itemlist:
        play_itemlist = play(video_item)

        if len(play_itemlist)>0:
            return True

    return False

def remove_accents(data):
    text = unicodedata.normalize("NFKD", data.decode('unicode-escape')).encode("ascii", "ignore")
    return text
