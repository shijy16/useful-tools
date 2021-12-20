import re
import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, name, inputs):
        self.name = name
        self.inputs = inputs
        self.children = 0
    
    def __init__(self, node_lines):
        self.inputs = []
        self.name = None
        self.built = False
        self.children = 0
        for line in node_lines:
            name_match = re.search('name: \"([^\"]+)\"', line)
            if name_match is not None:
                self.name = name_match.group(1)
                # print(self.name)
            input_match = re.search('input: \"([^\"]+)\"', line)
            if input_match is not None:
                self.inputs.append(input_match.group(1))
        if self.name is not None:
            self.built = True

    def find_parent(self, node_lists):
        self.parent = []
        for t in self.inputs:
            found = False
            for node in node_lists:
                if t == node.name:
                    self.parent.append(node)
                    found = True
                    node.children += 1
                    break
            if not found:
                self.parent.append(None)

def build_graph(file_name):
    node_list = []
    with open(file_name, 'r') as f:
        node_lines = []
        for line in f.readlines():
            line = line.strip('\n')
            if line.startswith('  }'):
                node = Node(node_lines)
                if node.built:
                    node_list.append(node)
                node_lines.clear()
            else:
                node_lines.append(line)
        if node.built:
            node = Node(node_lines)
    for node in node_list:
        node.find_parent(node_list)
    edge_list = []
    for node in node_list:
        for p in node.parent:
            edge_list.append((p.name, node.name))
    return node_list, edge_list

def draw_graph(node_list, edge_list, out_file):
    plt.figure(figsize=(15, 15))
    plt.axis('off')
    G = nx.DiGraph()
    for node in node_list:
        if len(node.parent) == 0:
            G.add_node(node.name, Type='in')
        elif(node.children == 0):
            G.add_node(node.name, Type='out')
        else:
            G.add_node(node.name, Type='mid')
    print(edge_list)
    G.add_edges_from(edge_list)

    in_nodes = [n for (n,ty) in nx.get_node_attributes(G,'Type').items() if ty == 'in']
    mid_nodes = [n for (n,ty) in nx.get_node_attributes(G,'Type').items() if ty == 'mid']
    out_nodes = [n for (n,ty) in nx.get_node_attributes(G,'Type').items() if ty == 'out']

    pos = nx.spring_layout(G)
    # nx.draw(G, pos=pos, with_labels=True, node_alpha=0)
    labels = {}
    for node,_ in G.nodes(data="False"):
        labels[node] = node
    nx.draw_networkx_labels(G, pos, labels, font_size=10)
    nx.draw_networkx_nodes(G, pos, nodelist=in_nodes, node_color='red', node_shape='o', alpha=0.3)
    nx.draw_networkx_nodes(G, pos, nodelist=mid_nodes, node_color='blue', node_shape='o', alpha=0.3)
    nx.draw_networkx_nodes(G, pos, nodelist=out_nodes, node_color='purple', node_shape='o', alpha=0.3)
    nx.draw_networkx_edges(G, pos, arrows=True, arrowstyle="->", arrowsize=15, edge_color='black', width=2, alpha='0.5')
    # plt.show()
    plt.tight_layout()
    plt.savefig(out_file + ".png", format="PNG", bbox_inches='tight')
        

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('usage: python graphdef2png.py graphdef_filename')
        exit(0)
    node_list, edge_list = build_graph(sys.argv[1])
    draw_graph(node_list, edge_list, sys.argv[1])