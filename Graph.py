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

def plotDegeneracyEq(plotA, plotB):
    # Convert dictionary data to numpy arrays (ensure same x)
    xA = np.array(list(plotA.keys()))
    yA = np.array(list(plotA.values()))
    xB = np.array(list(plotB.keys()))
    yB = np.array(list(plotB.values()))

    # For safety, only use x values present in both dictionaries
    common_x = np.intersect1d(xA, xB)
    yA_aligned = np.array([plotA[x] for x in common_x])
    yB_aligned = np.array([plotB[x] for x in common_x])

    # Create a simple graph structure (optional)
    G = nx.Graph()
    for i in range(len(common_x) - 1):
        G.add_edge((common_x[i], yA_aligned[i]), (common_x[i + 1], yA_aligned[i + 1]))
        G.add_edge((common_x[i], yB_aligned[i]), (common_x[i + 1], yB_aligned[i + 1]))

    # Plot both lines
    plt.figure(figsize=(7,5))
    plt.plot(common_x, yA_aligned, label='Plot A', marker='o', color='blue')
    plt.plot(common_x, yB_aligned, label='Plot B', marker='o', color='orange')

    # Shade the area between the two curves
    plt.fill_between(common_x, yA_aligned, yB_aligned, color='lightgreen', alpha=0.5)

    # Customize labels and title
    plt.plot(common_x, yA_aligned, label="MI^(Per)(X^(u);O")
    plt.plot(common_x, yB_aligned, label='MI^(Per)(X)˅(j)^(u);O)')
    plt.legend()
    plt.xlabel('x values - perturbed subset size of u')
    plt.ylabel('y values')
    plt.title('Area Between Plot A and Plot B - Degeneracy')
    plt.legend()
    plt.grid(True)
    plt.show()

# plot the degeneracy value only
def plotDegeneracyOnly(plot):
        # Convert dictionary data to numpy arrays (ensure same x)
    xA = np.array(list(plot.keys()))
    yA = np.array(list(plot.values()))

    # For safety, only use x values present in both dictionaries

    yA_aligned = np.array([plot[x] for x in xA])

    # Create a simple graph structure (optional)
    G = nx.Graph()
    for i in range(len(xA) - 1):
        G.add_edge((xA[i], yA_aligned[i]), (xA[i + 1], yA_aligned[i + 1]))

    # Plot both lines
    plt.figure(figsize=(7,5))
    plt.plot(xA, yA_aligned, label='Plot A', marker='o', color='blue')


    # Customize labels and title
    plt.plot(xA, yA_aligned, label="D˅(N)(X;O)")
    plt.legend()
    plt.xlabel('x values - perturbed subset size of u')
    plt.ylabel('y values')
    plt.title('Degeneracy Value')
    plt.legend()
    plt.grid(True)
    plt.show()