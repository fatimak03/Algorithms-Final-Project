#Algorithms Group Project
#Group 5
#Members:Fatima Khan, Ayesha Haider, Abhinav Sivasakthi

#importing the necessary libraries needed
#library for reading CSV files
import csv  
#library for working with graphs
import networkx as nx  
#library for plotting graphs
import matplotlib.pyplot as plt  
#library for displaying message boxes
from tkinter import messagebox  

#function to read the graph data from the CSV file
def load_graph_data(filename):
    #initialize an empty dictionary to store the graph data
    graph_structure = {}  

    #open the CSV file and read its contents
    with open(filename, 'r', encoding='utf-8-sig') as file:
        #create a CSV reader object
        csv_reader = csv.reader(file)  

        #iterate through each row of the CSV file
        for row in csv_reader:
            #extract the node from the first element of the row
            node = row[0]
            #initialize an empty dictionary to store the node's neighbors
            neighbors = {}  

            #iterate through the rest of the row by steps of 2
            for i in range(1, len(row), 2):
                #check if the entry is not empty
                if row[i] != '':
                    #add the neighbor and its weight to the neighbors dictionary
                    neighbors[row[i]] = int(row[i + 1])

            #add the node and its neighbors to the graph dictionary
            graph_structure[node] = neighbors

    return graph_structure

#dijkstra's algorithm to find the shortest paths from a starting node to all nodes
def compute_shortest_paths(graph_structure, start_node):
    #initialize distances to all nodes as infinity
    distances = {node: float('inf') for node in graph_structure}  
    #set the distance to the starting node as 0
    distances[start_node] = 0  
    #initialize an empty set to keep track of visited nodes
    visited_nodes = set()  
    #initialize a priority queue with the starting node and its distance
    priority_queue = [(0, start_node)]  
    
    #iterate until the priority queue is empty
    while priority_queue:
        #extract the node with the shortest distance from the priority queue
        current_distance, current_node = priority_queue.pop(0)  
        
        if current_node in visited_nodes:  
            #skip the node if it has already been visited
            continue
        
        #mark the current node as visited
        visited_nodes.add(current_node)  
        
        #skip nodes not in the graph
        if current_node not in graph_structure: 
            continue  # Skip nodes not in the graph
        
        # Iterate through the neighbors of the current node
        for neighbor, weight in graph_structure[current_node].items():
            #process unvisited neighbors
            if neighbor not in visited_nodes:  
                #calculate the new distance to the neighbor
                new_distance = current_distance + weight  
                
                #update the distance if the new distance is shorter than the current distance
                if new_distance < distances[neighbor]:
                    #update the distance to the neighbor
                    distances[neighbor] = new_distance  
                    #add the neighbor to the priority queue
                    priority_queue.append((new_distance, neighbor))  
    
    #return the shortest distances to all nodes from the starting node
    return distances  

#function to highlight the shortest paths to charging stations
def find_shortest_paths_to_stations(graph, start_node, charging_stations):
    #find all shortest paths from the starting node to each charging station
    paths = nx.single_source_shortest_path(graph, start_node)
    shortest_paths = []
    
    #iterate through the charging stations
    for station in charging_stations:
        #check if a path exists to the charging station
        if station in paths:  
            #add the shortest path to the list of shortest paths
            shortest_paths.append(nx.shortest_path(graph, start_node, station))  
    
    #create a subgraph containing nodes along the shortest paths
    subgraph = graph.subgraph([node for path in shortest_paths for node in path])
    
    #return the subgraph and the list of shortest paths
    return subgraph, shortest_paths  

#main function
def main():
    # Provide the absolute path to the CSV file
    filename = '/Users/fatimakhan/Desktop/network_data.csv'  
    
    #read full graph
    graph_structure = load_graph_data(filename)

    #create a graph from the network data with weighted edges
    G = nx.Graph()
    for node, neighbors in graph_structure.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    #create a text box for the title on the first graph
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.text(0.5, 1.05, "EV Charging Station Route Optimization Application",
            horizontalalignment='center', verticalalignment='center',
            fontsize=16, fontweight='bold', transform=ax.transAxes)
    ax.axis('off')
    
    #draw the full graph
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_size=700, node_color='skyblue', font_size=12, edge_color='gray')
    nx.draw_networkx_edge_labels(G, pos, edge_labels={(u, v): d['weight'] for u, v, d in G.edges(data=True)})
    plt.tight_layout()
    plt.show()

    #prompt user to input starting node
    start_node = input("Enter starting node: ").upper()

    #check if starting node is valid
    if start_node not in graph_structure:
        messagebox.showerror("Error", "Invalid starting node.")
        return

    #define charging stations
    charging_stations = ['H', 'K', 'O', 'T']

    #highlight shortest paths to charging stations
    subgraph, shortest_paths = find_shortest_paths_to_stations(G, start_node, charging_stations)

    #create a new figure for the second graph
    plt.figure(figsize=(10, 8))

    #create a text box for the title on the second graph
    ax = plt.gca()
    ax.text(0.5, 1.05, "Best path from {}".format(start_node),
            horizontalalignment='center', verticalalignment='center',
            fontsize=16, fontweight='bold', transform=ax.transAxes)
    ax.axis('off')
   

    #draw the graph with highlighted shortest paths
    node_colors = ['yellow' if node == start_node else 'orange' if node in charging_stations else 'lightgreen' for node in subgraph.nodes()]  # Highlight starting node and charging stations
    nx.draw(subgraph, pos, with_labels=True, node_size=700, node_color=node_colors, font_size=12, edge_color='gray')
    nx.draw_networkx_edge_labels(subgraph, pos, edge_labels={(u, v): d['weight'] for u, v, d in subgraph.edges(data=True)})

    #define colors for arrows
    colors = ['red', 'blue', 'green', 'purple']

    #add arrows to indicate direction from start_node to charging stations
    for i, station in enumerate(charging_stations):
        if nx.has_path(subgraph, start_node, station):
            path = shortest_paths[i]
            for j in range(len(path) - 1):
                offset = 0.05 * (j + 1)
                plt.annotate("", xy=pos[path[j + 1]], xytext=pos[path[j]],
                            arrowprops=dict(arrowstyle="->", color=colors[i], connectionstyle=f"arc3,rad={offset}"))

    #add labels for the total distance of each shortest path
    for i, path in enumerate(shortest_paths):
        total_distance = sum(G[path[j]][path[j+1]]['weight'] for j in range(len(path) - 1))
        node_pos = pos[path[-1]]
        plt.text(node_pos[0], node_pos[1] + 0.1, f"Total Distance: {total_distance}", ha='center', va='center', fontsize=10, fontweight='bold', bbox=dict(facecolor='white', edgecolor='white'))
    #turn off axis labels and ticks
    plt.axis('off')  
    #adjust layout
    plt.tight_layout()  
    #display the plot
    plt.show()  

if __name__ == "__main__":
    main()


