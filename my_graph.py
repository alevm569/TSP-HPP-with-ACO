import sys
import lxml.etree
import networkx as nx
import matplotlib.pyplot as plt
import random

def create_graph(file, node_number):
    node = range(0, node_number)
    g = nx.complete_graph(node)
    attrs_nodes = {}

    for i in list(node):
        coord = {}
        for c in list(range(2)):
            coord['y'] = round(random.uniform(1.0, 14.5), 3)
            coord['x'] = round(random.uniform(1.0, 14.5), 3)
        attrs_nodes[i] = coord
    nx.set_node_attributes(g, attrs_nodes)
    nx.write_graphml_lxml(g, file, infer_numeric_types=True, named_key_ids=True)
    nx.draw(g)
    plt.show()
def read_graph(file):
    # Processing XML
    # Changing file's type to ElementTree to parsing only elements XML
    parse_file = lxml.etree.parse(file)
    # URI Prefixes
    name_space = parse_file.getroot().nsmap
    # Find the default URI
    default_ns = list(filter(lambda x: "http://graphml.graphdrawing.org/xmlns" in x[1], name_space.items()))
    #Validations to namespaces/URI
    if len(default_ns) < 1:
        print(f"{file} does not contain the default graphml namespace")
        sys.exit(1)
    # If the default namespace has a name, use it, otherwise, assign a generic name to it
    if default_ns[0][0] is not None:
        glns = default_ns[0][0]

    else:
        glns = "_q_q";  # Or something else as absurd, with zero chance of overwriting another key from the nsmap
        name_space[glns] = default_ns[0][1]
        del (name_space[None])
    #Get graph attributes
    atr_graph = parse_file.xpath(f"/{glns}:graphml/{glns}:key[@for='graph']", namespaces=name_space)
    #Get nodes attributes
    atr_node = parse_file.xpath(f"/{glns}:graphml/{glns}:key[@for='node']", namespaces=name_space)
    #Get edges attributes
    atr_edges = parse_file.xpath(f"/{glns}:graphml/{glns}:key[@for='edge']", namespaces=name_space)
    #Get all nodes
    all_nodes = parse_file.xpath(f"/{glns}:graphml/{glns}:graph/{glns}:node", namespaces=name_space)
    #Get all edged
    all_edges = parse_file.xpath(f"/{glns}:graphml/{glns}:graph/{glns}:edge", namespaces=name_space)
    data_type_conversion_map = {"boolean": bool, "int": int, "long": int, "float": float, "double": float, "string": str}
    nodes = {}
    for node in all_nodes:
        id = node.attrib["id"]
        info_node = dict(
            map(lambda x: (x.attrib["attr.name"],
                           data_type_conversion_map[x.attrib["attr.type"]](
                               node.xpath(f"{glns}:data[@key='{x.attrib['attr.name']}']", namespaces=name_space)[0].text)
                           ),atr_node))
        if id not in nodes:
            nodes[id] = info_node
        else:
            print(f"Node id {id} is not unique in {file}")
            sys.exit(1)
    edges = {}
    id_edge=0
    for edge in all_edges:
        edge_start = edge.attrib["source"]
        edge_final = edge.attrib["target"]
        links = (edge_start, edge_final)
        id_edge +=1

        if links not in edges:
            edges[id_edge] = links
        else:
            print(f"Node id {id_edge} is not unique in {file}")
            sys.exit(1)
    return nodes, edges