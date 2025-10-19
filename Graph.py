# graph the data

import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

# For a given node dictionary, graph the nodes
def graphNetwork(nodeDict):

    # Create blank directed graph canvas
    canvas = nx.DiGraph()

    # Add nodes
    for node in nodeDict:
        canvas.add_node(node)
    
    # Add edges
    for node in nodeDict:
        obj = nodeDict[node]
        inputNodeList = obj.inputNodes
        firstNode = obj.id
        for inNode in inputNodeList:
            secondNodeObj = inNode
            secondNode = secondNodeObj.id
            canvas.add_edge( secondNode, firstNode, weight=1)
    
    # Lists i.e. Settings
    nodeSizes = [200] * len(canvas.nodes())  # Ensure nodeSizes matches the number of nodes
    color_map = ['grey'] * len(canvas.nodes())  # One color for each node
    edge_color = "black"
    # Compute layout
    pos = nx.spring_layout(canvas)

    # Draw Canvas
    nx.draw(canvas, pos, with_labels=True, font_size=16, node_size=nodeSizes, 
            node_color=color_map, arrows=True, arrowsize=20, edge_color=edge_color)
    plt.show()


# Need to plot the degeneracy function next