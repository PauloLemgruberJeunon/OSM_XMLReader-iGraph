from igraph import *
import time
import math


class GraphUtils:
    @classmethod
    def wrong_highway(cls, value):
        for v in ["unclassified", "service", "footway", "track", "cycleway", "pedestrian", "birdleway"]:
            if value == v:
                return True
        return False

    @classmethod
    def graph_creator(cls, g, my_parser, will_print):
        vs_reference = {}
        vs_counter = [0]
        my_es = [0]
        for w in range(len(my_parser.ways)):
            way = my_parser.ways[w]
            if len(way.nds) <= 1 or (not ("highway" in way.tags.keys())) or cls.wrong_highway(
                    way.tags["highway"]) == True:
                pass
            else:
                # Add the vertices in the useful Way to the graph
                for nd in way.nds:
                    if str(nd) in my_parser.nodes:
                        lon = my_parser.nodes[str(nd)].lon
                        lat = my_parser.nodes[str(nd)].lat
                        attri = {"id": nd, "lon": lon, "lat": lat, "myines": "", "myoutes": ""}
                        del my_parser.nodes[str(nd)]
                        g.add_vertex(None, **attri)
                        vs_reference[str(nd)] = vs_counter[0]
                        vs_counter[0] += 1

                # Add information to the wayTag
                way.tags["WayID"] = way.id
                # Delete useless way tags
                way.tags.pop("source", None)
                way.tags.pop("created_by", None)
                way.tags.pop("name:pt", None)
                for j in range(len(way.nds) - 1):
                    vs1 = g.vs[vs_reference[str(way.nds[j])]]
                    vs2 = g.vs[vs_reference[str(way.nds[j + 1])]]

                    # Add additional information to edges and, after, create the edges
                    way.tags["lonDiff"] = math.radians(abs(vs1["lon"] - vs2["lon"]))
                    way.tags["latDiff"] = math.radians(abs(vs1["lat"] - vs2["lat"]))

                    # Haversine formula to calculate distance between to points on Earth
                    vs1LatRad = math.radians(vs1["lat"])
                    vs2LatRad = math.radians(vs2["lat"])
                    a = pow(sin(way.tags["latDiff"]/2), 2) + \
                        (cos(vs1LatRad) * cos(vs2LatRad) * pow(sin(way.tags["lonDiff"]/2), 2))
                    c = 2 * math.atan2(math.sqrt(a), math.sqrt((1-a)))
                    d = c * 6371e3  # Earth radius

                    way.tags["distance"] = d

                    g.add_edge(vs1, vs2, **way.tags)

                    # Stores the iGraph Edge id inside the vertex for after eliminate the edges with lower "k"
                    vs1["myoutes"] += (str(my_es[0]) + "-")
                    vs2["myines"] += (str(my_es[0]) + "-")

                    my_es[0] += 1

                    # For streets that supports traffic in both ways
                    if not will_print and 'oneway' in way.tags.keys() and way.tags['oneway'] == "no":
                        g.add_edge(vs2, vs1, **way.tags)
                        my_es[0] += 1
                        vs1["myines"] += (str(my_es[0]) + "-")
                        vs2["myoutes"] += (str(my_es[0]) + "-")

        return g

    @classmethod
    def save_graph(cls, g):
        save = open("save", "w")
        g.write(save, "gml")

    @classmethod
    def load_graph(cls, will_print):
        g = Graph()
        g.__init__(directed=(not will_print == 'y'))
        save = open("save", "r")
        g = g.Read(save, "gml")
        return g

    @classmethod
    def print_graph(cls, g, vertex_size, edge_width, img_size):
        coords = []
        for vertex in g.vs:
            delta_lon = vertex["lon"]
            delta_lat = vertex["lat"]
            coord = [delta_lat, delta_lon]
            coords.append(coord)

        layout = Layout(coords)
        visual_style = {}
        visual_style["vertex_size"] = vertex_size
        visual_style["vertex_color"] = ["red"]
        visual_style["edge_width"] = edge_width
        visual_style["layout"] = layout
        visual_style["bbox"] = img_size
        visual_style["margin"] = 20
        plot(g, **visual_style)

    # @classmethod
    # def graph_simplifier(cls, g):

    @classmethod
    def test_graph(cls, g):
        testNum = 32
        print("\n\n in_es = ", g.vs[testNum]["myines"], "\n\n my_id = ", g.vs[testNum]["id"])
        strings = g.vs[testNum]["myines"].split('-')
        strings2 = g.vs[testNum]["myoutes"].split('-')
        print("        strings = ", strings)
        print(g.es[int(strings2[0])])
        print(g.es[int(strings[0])])
        print("\n Source = ", g.es[int(strings[0])].source, " - target = ", g.es[int(strings[0])].target)
        print("\n Source2 = ", g.es[int(strings2[0])].source, " - target2 = ", g.es[int(strings2[0])].target)

    # A class to measure execution time
    class Timer:
        def __init__(self):
            self.start = 0
            self.stop = 0
            self.elapsed_time = 0

        def start_timer(self):
            self.start = time.clock()

        def end_timer(self):
            self.stop = time.clock()
            if self.stop < self.start:
                print("Most likely you forgot to start the timer before ending it...")
                self.elapsed_time = -1
            else:
                self.elapsed_time = self.stop - self.start

        def show_time(self):
            if self.start == 0 or self.stop == 0:
                print("\n You forgot to start or to end the timer....")
            else:
                print("\n Time elapsed = %f seconds" % self.elapsed_time)
