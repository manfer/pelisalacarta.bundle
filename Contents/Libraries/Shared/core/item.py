class Item(object):
    channel = ""
    title = ""
    url = ""
    page = ""
    thumbnail = ""
    art = ""
    plot = ""
    duration = ""
    fanart = ""
    folder = ""
    action = ""
    server = "directo"
    extra = ""
    show = ""
    category = ""
    childcount = 0
    language = ""
    type = ""
    context = ""
    subtitle = ""
    totalItems =0
    overlay = None
    password = ""
    fulltitle = ""
    viewmode = "list"

    def __init__(self, channel="", title="", url="", page="", thumbnail="", art="", plot="", duration="", fanart="", action="", server="directo", extra="", show="", category = "" , language = "" , subtitle="" , folder=True, context = "",totalItems = 0, overlay = None, type="", password="", fulltitle="", viewmode="list" ):
        self.channel = channel
        self.title = title
        self.url = url
        if page=="":
            self.page = url
        else:
            self.page = page
        self.thumbnail = thumbnail
        self.art = art
        self.plot = plot
        self.duration = duration
        self.fanart = fanart
        self.folder = folder
        self.server = server
        self.action = action
        self.extra = extra
        self.show = show
        self.category = category
        self.childcount = 0
        self.language = language
        self.type = type
        self.context = context
        self.subtitle = subtitle
        self.totalItems = totalItems
        self.overlay = overlay
        self.password = password
        self.fulltitle = fulltitle
        self.viewmode = viewmode

    def tostring(self):
        return "title=["+self.title+"], url=["+self.url+"], thumbnail=["+self.thumbnail+"], action=["+self.action+"], show=["+self.show+"], category=["+self.category+"]"
    
    def serialize(self):
        separator = "|>|<|"
        devuelve = ""
        devuelve = devuelve + self.title + separator
        devuelve = devuelve + self.url + separator
        devuelve = devuelve + self.channel + separator
        devuelve = devuelve + self.action + separator
        devuelve = devuelve + self.server + separator
        devuelve = devuelve + self.extra + separator
        devuelve = devuelve + self.category + separator
        devuelve = devuelve + self.fulltitle + separator
        devuelve = devuelve + self.viewmode + separator
        devuelve = devuelve + self.thumbnail + separator
        devuelve = devuelve + self.art + separator
        return devuelve
    
    def deserialize(self,cadena):
        trozos=cadena.split("|>|<|")
        self.title = trozos[0]
        self.url = trozos[1]
        self.channel = trozos[2]
        self.action = trozos[3]
        self.server = trozos[4]
        self.extra = trozos[5]
        self.category = trozos[6]
        self.fulltitle = trozos[7]
        self.viewmode = trozos[8]
        self.thumbnail = trozos[9]
        self.art = trozos[10]

if __name__ == "__main__":
    item = Item(title="bla b", url="http://bla")
    cadena=item.serialize()
    print cadena
    
    item2 = Item()
    item2.deserialize(cadena)
    print item2.title,item2.url
