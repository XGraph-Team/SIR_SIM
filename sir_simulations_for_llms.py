# -*- coding: utf-8 -*-
"""SIR simulations for LLMs.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1DBcAgExEUVM628rEBGVZ79Sb4x9aq-JE
"""

# !pip install networkx
# !pip install ndlib
# !pip install torch_geometric

import os
import networkx as nx
import ndlib
import ndlib.models.epidemics as ep
import ndlib.models.ModelConfig as mc
from time import time
import matplotlib.pyplot as plt
import torch_geometric.datasets as ds
import random
from torch_geometric.datasets import Planetoid
import json
from networkx.readwrite import json_graph
import numpy as np

temp_dir = 'temp/'
os.makedirs(temp_dir, exist_ok=True)

def toEdgeList(G, graph_name, run_number):
    # filename = f"edge_list_{graph_name}_run{run_number}.txt"
    filename = f"temp/edge_list_{graph_name}_run{run_number}.txt"
    nx.write_edgelist(G, filename)
    
def toWeightedEdgeList(G, graph_name, run_number):
    filename = f"temp/weighted_edge_list_{graph_name}_run{run_number}.txt"
    nx.write_weighted_edgelist(G, filename)

def toAdjMatrix(G, graph_name, run_number):
    # Get adjacency matrix as a SciPy sparse matrix
    adj_matrix_sparse = nx.adjacency_matrix(G)

    # Convert to a dense matrix (NumPy array)
    adj_matrix_dense = adj_matrix_sparse.todense()

    # Print the dense adjacency matrix
    # print(adj_matrix_dense)

    # Save this to a file
    filename = f'temp/adjacency_matrix_{graph_name}_run{run_number}.txt'
    with open(filename, 'w') as f:
        np.savetxt(f, adj_matrix_dense, fmt='%d')

    
def toJSON(G, graph_name, run_number):
    # Convert to JSON data
    data = json_graph.node_link_data(G)
    
    # Convert JSON object to a string
    json_data = json.dumps(data, indent=4)
    
    # Print JSON string
    # print(json_data)
    
    # Save to a file
    filename = f'temp/graph_{graph_name}_run{run_number}.json'
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)

    
def connSW(beta=None):
    print('connSW beta', beta)
    # Randomize size between 1000 and 1500
    # n = random.randint(1000, 1500) # The number of nodes
    # n = 100 # The number of nodes
    n = 20 # The number of nodes
    k = 10  # Number of nearest neighbors in the ring topology
    p = 0.15 # The probability of rewiring each edge

    G = nx.connected_watts_strogatz_graph(n, k, p)

    config = mc.Configuration()

    for a, b in G.edges():
        weight = random.randrange(40, 80)
        weight = round(weight / 100, 2)
        if beta:
            weight = beta
        G[a][b]['weight'] = weight
        config.add_edge_configuration("threshold", (a, b), weight)
    
    return G, config

def BA():
    g = nx.barabasi_albert_graph(1000, 5)

    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(40,80)
        weight = round(weight / 100, 2)
        g[a][b]['weight'] = weight
        config.add_edge_configuration("threshold", (a, b), weight)

    return g, config

def ER():

    g = nx.erdos_renyi_graph(5000, 0.002)

    while nx.is_connected(g) == False:
        g = nx.erdos_renyi_graph(5000, 0.002)

    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(40,80)
        weight = round(weight / 100, 2)
        config.add_edge_configuration("threshold", (a, b), weight)
        g[a][b]['weight'] = weight

    return g, config

def CiteSeer():
    dataset = Planetoid(root='./Planetoid', name='CiteSeer')  # Cora, CiteSeer, PubMed
    data = dataset[0]
    edges = (data.edge_index.numpy()).T.tolist()
    G = nx.from_edgelist(edges)

    c = max(nx.connected_components(G), key=len)
    g = G.subgraph(c).copy()
    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(40,80)
        weight = round(weight / 100, 2)
        config.add_edge_configuration("threshold", (a, b), weight)
        g[a][b]['weight'] = weight

    return g, config

def PubMed():
    dataset = Planetoid(root='./Planetoid', name='PubMed')  # Cora, CiteSeer, PubMed
    data = dataset[0]
    edges = (data.edge_index.numpy()).T.tolist()
    G = nx.from_edgelist(edges)

    c = max(nx.connected_components(G), key=len)
    g = G.subgraph(c).copy()
    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(40,80)
        weight = round(weight / 100, 2)
        config.add_edge_configuration("threshold", (a, b), weight)
        g[a][b]['weight'] = weight

    return g, config

def Cora():
    dataset = Planetoid(root='./Planetoid', name='Cora')  # Cora, CiteSeer, PubMed
    data = dataset[0]
    edges = (data.edge_index.numpy()).T.tolist()
    G = nx.from_edgelist(edges)

    c = max(nx.connected_components(G), key=len)
    g = G.subgraph(c).copy()
    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(40,80)
        weight = round(weight / 100, 2)
        config.add_edge_configuration("threshold", (a, b), weight)
        g[a][b]['weight'] = weight

    return g, config

def photo():

    dataset = ds.Amazon(root='./geo', name = 'Photo')
    data = dataset[0]
    edges = (data.edge_index.numpy()).T.tolist()
    G = nx.from_edgelist(edges)
    g = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)

    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(5,20)
        weight = round(weight / 100, 2)
        config.add_edge_configuration("threshold", (a, b), weight)
        g[a][b]['weight'] = weight

    return g, config

def coms():

    dataset = ds.Amazon(root='./geo', name = 'Computers')
    data = dataset[0]
    edges = (data.edge_index.numpy()).T.tolist()
    G = nx.from_edgelist(edges)
    g = nx.convert_node_labels_to_integers(G, first_label=0, ordering='default', label_attribute=None)

    config = mc.Configuration()

    for a, b in g.edges():
        weight = random.randrange(5,20)
        weight = round(weight / 100, 2)
        config.add_edge_configuration("threshold", (a, b), weight)
        g[a][b]['weight'] = weight

    return g, config

def run_and_save_sir_model(graph_func, graph_name, run_number, graph_args=[], beta=0.1, gamma=0.1, steps=10):
    G, config = graph_func(*graph_args)
    # toJSON(G, graph_name, run_number)
    # toAdjMatrix(G, graph_name, run_number)
    # toEdgeList(G, graph_name, run_number)
    toWeightedEdgeList(G, graph_name, run_number)

    # Model selection
    model = ep.SIRModel(G)

    # Model Configuration
    config = mc.Configuration()
    config.add_model_parameter('beta', beta)
    config.add_model_parameter('gamma', gamma)

    # Set the initial infected node using a fixed seed for consistency
    random.seed(42)  # Fixed seed

    # # Select the node with the highest degree
    # initial_infected = max(G, key=G.degree)
    # config.add_model_initial_configuration("Infected", [initial_infected])

    # Calculate top 5% nodes by degree
    top_5_percent = int(0.05 * G.number_of_nodes())
    nodes_sorted_by_degree = sorted(G.degree, key=lambda x: x[1], reverse=True)
    initial_infected = [node for node, degree in nodes_sorted_by_degree[:top_5_percent]]
    config.add_model_initial_configuration("Infected", initial_infected)

    model.set_initial_status(config)

    # Simulation execution
    iterations = model.iteration_bunch(steps)

    # Write only infected nodes at each iteration to a file
    # with open(f'infected_nodes_{graph_name}_run{run_number}.txt', 'w') as file:
    #     file.write(f"{graph_name} run {run_number} - Infected nodes per iteration:\n")
    #     for iteration in iterations:
    #         infected_nodes = [node for node, status in iteration['status'].items() if status == 1]
    #         file.write(f"Iteration {iteration['iteration']} - Infected nodes: {infected_nodes}\n")

    # # Initialize a set to keep track of currently infected nodes
    # currently_infected_nodes = set()
    
    # # Write currently infected nodes at each iteration to a file
    # with open(f'infected_nodes_{graph_name}_run{run_number}.txt', 'w') as file:
    #     file.write(f"{graph_name} run {run_number} - Infected nodes per iteration:\n")
        
    #     for iteration in iterations:
    #         # Update the set of currently infected nodes
    #         for node, status in iteration['status'].items():
    #             if status == 1:  # If node is infected
    #                 currently_infected_nodes.add(node)
    #             elif node in currently_infected_nodes and status != 1:  # If node was infected but now is not
    #                 currently_infected_nodes.remove(node)
    
    #         # Write the set of currently infected nodes to the file
    #         file.write(f"Iteration {iteration['iteration']} - Infected nodes: {sorted(currently_infected_nodes)}\n")

    # Define states for clarity (modify as per your model's definitions)
    SUSCEPTIBLE = 0
    INFECTED = 1
    RECOVERED = 2

    # Initialize a dictionary to keep track of each node's current state
    current_node_states = {}

    # Write node states at each iteration to a file
    with open(f'temp/node_states_{graph_name}_run{run_number}.txt', 'w') as file:
        file.write(f"{graph_name} run {run_number} - Node states per iteration:\n")
        
        for iteration in iterations:
            # Update the dictionary of node states
            for node, status in iteration['status'].items():
                current_node_states[node] = status

            # Prepare data for writing to file: summarizing node states
            infected_nodes = [node for node, state in current_node_states.items() if state == INFECTED]
            recovered_nodes = [node for node, state in current_node_states.items() if state == RECOVERED]
            susceptible_nodes = [node for node, state in current_node_states.items() if state == SUSCEPTIBLE]

            # Write the summary of node states to the file
            file.write(f"Iteration {iteration['iteration']}:\n")
            file.write(f"  Infected nodes: {sorted(infected_nodes)}\n")
            file.write(f"  Recovered nodes: {sorted(recovered_nodes)}\n")
            file.write(f"  Susceptible nodes: {sorted(susceptible_nodes)}\n\n")

    # Note: Modify the SUSCEPTIBLE, INFECTED, RECOVERED constants according to your simulation's state definitions.


    # Write iterations to a file
    with open(f'temp/iterations_{graph_name}_run{run_number}.txt', 'w') as file:
        file.write(f"{graph_name} iterations:\n")
        for iteration in iterations:
            file.write(str(iteration) + "\n")

    # draw graphs for all iterations
    for iteration_index, iteration in enumerate(iterations):
        # update the status of nodes
        # based on the current iteration's status data.
        for node, status in iteration['status'].items():
            G.nodes[node]['status'] = status
    
        # Node colors based on status
        status_colors = {0: 'green', 1: 'red', 2: 'blue'}
        colors = [status_colors[G.nodes[node]['status']] for node in G.nodes()]
    
        # Draw the graph
        pos = nx.spring_layout(G)
        nx.draw(G, pos, node_color=colors, with_labels=False, node_size=20)
    
        # Save the plot with run number and iteration in the filename
        # plt.savefig(f'graph_infected_state_{graph_name}_run{run_number}_iteration{iteration_index}.png', format='PNG')
        
        # Save the plot with run number and iteration in the filename
        plt_filename = f'temp/graph_infected_state_{graph_name}_run{run_number}_iteration{iteration_index}.png'
        plt.savefig(plt_filename, format='PNG')
        plt.close()

# List of graph functions, their names, and specific arguments
graphs = [
    # (connSW, "connSW", [0.3]),  # connSW requires beta
    (connSW, "connSW", [])
    # (BA, "BA", []),
    # (ER, "ER", []),
    # (CiteSeer, "CiteSeer", []),
    # (PubMed, "PubMed", []),
    # (Cora, "Cora", []),
    # (photo, "photo", []),
    # (coms, "coms", [])
]

# Run and save for each graph type 20 times
for graph_func, graph_name, graph_args in graphs:
    print('graph_args', graph_args)
    for run_number in range(0, 1):  # Run 20 times
        run_and_save_sir_model(graph_func, graph_name, run_number, graph_args, 0.5, 0.3, 10) # beta, gamma, steps
