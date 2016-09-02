import xml.sax


# Stores the XML nodes
class XMLNode:
    def __init__(self, wid, lon, lat):
        self.id = wid
        self.lon = lon
        self.lat = lat
        self.tags = {}


# Stores the XML ways
class XMLWay:
    def __init__(self, wid):
        self.id = wid
        self.nds = []
        self.tags = {}


# Most important class for the parsing process. Overrides the methods
#   of the father class xml.sax.ContentHandler to adapt them to the OSM XML file (in this case to get highways).
class OSMHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.ways = []
        self.nodes = {}
        xml.sax.ContentHandler.__init__(self)

    def startElement(self, name, attrs):
        if name == 'node':
            self.currElem = XMLNode(int(attrs['id']), float(attrs['lon']), float(attrs['lat']))
        elif name == 'way':
            self.currElem = XMLWay(int(attrs['id']))
        elif name == 'tag':
            self.currElem.tags[str(attrs['k'])] = attrs['v']
        elif name == 'nd':
            self.currElem.nds.append(int(attrs['ref']))

    def endElement(self, name):
        if name == 'node':
            self.nodes[str(self.currElem.id)] = self.currElem
        elif name == 'way':
            self.ways.append(self.currElem)

    def setDocumentLocator(self, loc):
        pass

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def characters(self, chars):
        pass
