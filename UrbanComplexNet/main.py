from Menu import *

if __name__ == '__main__':

    while True:
        choice = input("\n To use get the graph by an XML file enter 'x', or enter 'l' to load "
                       "a previus saved graph: ")
        if choice == 'x' or choice == 'l':
            break
        else:
            print("\n Wrong input, try again... ")

    if choice == 'x':
        Menu.xml_graph()
    else:
        g = Menu.gml_load_graph()
