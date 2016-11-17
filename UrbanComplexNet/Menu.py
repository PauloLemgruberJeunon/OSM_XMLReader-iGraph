from OSMparser import *
from GraphUtils import *

class Menu:

    # Private Variables:
    graph_dict = {}

    @classmethod
    def xml_graph(cls):
        while True:
            will_print = input("\n You will want to print your graph [y/n]: ")

            if will_print == 'y' or will_print == 'n':
                break
            else:
                print("\n Wrong input, try again... ")

        while True:
            will_save = input("\n You want to save your graph [y/n]: ")

            if will_save == 'y' or will_save == 'n':
                break
            else:
                print("\n Wrong input, try again... ")

        timer = GraphUtils.Timer()

        timer.start_timer()

        # if use_utf8:
        #     reload(sys)
        #     sys.setdefaultencoding("utf-8")

        # Make the graph directed to simulated better the city streets environment

        my_parser = OSMHandler()

        # Starts the parsing processes on the XML Database
        xml.sax.parse("StreetsRawData/albany_new-york.osm", my_parser)

        GraphUtils.graph_creator(my_parser, will_print, Menu.graph_dict)

        # GraphUtils.test_graph(g)

        if will_save == 'y':
            GraphUtils.save_graph(Menu.graph_dict['full_graph'], "full_graph")
            GraphUtils.save_graph(Menu.graph_dict['bus_graph'], "bus_graph")

        timer.end_timer()
        timer.show_time()

    @classmethod
    def gml_load_graph(cls):
        while True:
            will_print = input("\n You will want to print your graph [y/n]: ")

            if will_print == 'y' or will_print == 'n':
                break
            else:
                print("\n Wrong input, try again... ")

        g = GraphUtils.load_graph(will_print)

        # GraphUtils.test_graph(g)

        if will_print == 'y':
            GraphUtils.print_graph(g, 4, 2, (900, 900))

        return g
