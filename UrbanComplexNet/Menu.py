from OSMparser import *
from GraphUtils import *

class Menu:
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

        g = Graph()
        timer = GraphUtils.Timer()

        timer.start_timer()

        # if use_utf8:
        #     reload(sys)
        #     sys.setdefaultencoding("utf-8")

        # Make the graph directed to simulated better the city streets environment
        g.__init__(directed=(not will_print == 'y'))

        my_parser = OSMHandler()

        # Starts the parsing processes on the XML Database
        xml.sax.parse("highways.xml", my_parser)

        g = GraphUtils.graph_creator(g, my_parser, will_print)

        GraphUtils.test_graph(g)

        if will_save == 'y':
            GraphUtils.save_graph(g)

        timer.end_timer()
        timer.show_time()

        if will_print == 'y':
            GraphUtils.print_graph(g, 4, 2, (900, 900))

        return g

    @classmethod
    def gml_load_graph(cls):
        while True:
            will_print = input("\n You will want to print your graph [y/n]: ")

            if will_print == 'y' or will_print == 'n':
                break
            else:
                print("\n Wrong input, try again... ")

        g = GraphUtils.load_graph(will_print)

        GraphUtils.test_graph(g)

        if will_print == 'y':
            GraphUtils.print_graph(g, 4, 2, (900, 900))

        return g
