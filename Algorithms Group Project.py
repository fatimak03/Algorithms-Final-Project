#ALGORITHMS FINAL GROUP PROJECT
#MD AL MARUF
#GROUP MEMBERS: Fatima Khan 100812028, Ayesha Haider 100869659, Abhinav Siva 100699812

# Import the csv library for handling CSV files
import csv

# Import the networkx library for working with graphs
import networkx as nx

# Import matplotlib for plotting graphs
import matplotlib.pyplot as plt

# Import Tkinter for GUI-related tasks, specifically for displaying message boxes
from tkinter import Tk, messagebox

# Define a function to read the graph data from a CSV file
def load_graph_data(filename):
    # Initialize an empty dictionary to store the graph structure
    graph_structure = {}

    # Open the CSV file for reading
    with open(filename, 'r', encoding='utf-8-sig') as file:
        # Create a CSV reader object
        csv_reader = csv.reader(file)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # The first element in the row is the node
            node = row[0]

            # Initialize a dictionary to store the neighbors of the node
            neighbors = {}

            # Iterate over the rest of the row in steps of 2 (neighbor and weight)
            for i in range(1, len(row), 2):
                # Check if the neighbor entry is not empty
                if row[i] != '':
                    # Add the neighbor and its associated weight to the neighbors dictionary
                    neighbors[row[i]] = int(row[i + 1])

            # Add the node and its neighbors to the graph structure
            graph_structure[node] = neighbors

    # Return the graph structure dictionary
    return graph_structure

# Define a function to calculate and display paths to charging stations
def calculate_and_display_paths(graph, start_node, charging_stations):
    # Initialize dictionaries to store paths and their associated costs
    paths_and_costs = {}
    shortest_paths = {}

    # Loop through each charging station to calculate the shortest path
    for station in charging_stations:
        try:
            # Calculate the shortest path from the start node to the current station
            path = nx.shortest_path(graph, start_node, station, weight='weight')

            # Calculate the total cost (distance) of this path
            cost = nx.shortest_path_length(graph, start_node, station, weight='weight')

            # Store the cost and path for the current station
            paths_and_costs[station] = cost
            shortest_paths[station] = path

            # Print the path and its cost
            print(f"Path to {station}: {path} with cost of {cost}")
        except nx.NetworkXNoPath:
            # If no path exists, note it and assign an infinite cost
            print(f"No path to {station}.")
            paths_and_costs[station] = float('inf')

    # Identify and print the closest charging station based on the lowest cost
    if paths_and_costs:
        closest_charger = min(paths_and_costs, key=paths_and_costs.get)
        print(f"\nThe closest charger is {closest_charger}")
    else:
        # If no valid paths were found, inform the user
        print("No valid paths were found from the start node to any of the charging stations.")
    
    # Return the dictionary of shortest paths
    return shortest_paths

# Define a function to create and display a subgraph for the shortest paths
def create_and_display_subgraph(graph, start_node, shortest_paths, charging_stations):
    # Create a set to store all nodes involved in the shortest paths
    all_nodes_in_paths = set()

    # Loop through each path and add its nodes to the set
    for path in shortest_paths.values():
        all_nodes_in_paths.update(path)
    
    # Create a subgraph using only the nodes in the shortest paths
    subgraph = graph.subgraph(all_nodes_in_paths)

    # Plot the subgraph if it contains nodes
    if len(subgraph.nodes) > 0:
        # Create a new figure for the plot
        plt.figure(figsize=(10, 8))

        # Calculate positions for the nodes in the subgraph
        pos = nx.spring_layout(subgraph, seed=42)  # Fixed layout for consistency

        # Draw the subgraph with labels and specified node size, color, and font settings
        nx.draw(subgraph, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=14, font_weight='bold')

        # Draw the edge labels (weights) in the subgraph
        nx.draw_networkx_edge_labels(subgraph, pos, edge_labels={(u, v): d['weight'] for u, v, d in subgraph.edges(data=True)}, font_color='blue')

        # Loop through each charging station to draw arrows for the paths
        for station in charging_stations:
            if station in shortest_paths:
                path = shortest_paths[station]
                for j in range(len(path) - 1):
                    # Annotate the plot with arrows showing the direction of each path
                    plt.annotate("", xy=pos[path[j + 1]], xytext=pos[path[j]],
                                 arrowprops=dict(arrowstyle="->", color='red', connectionstyle=f"arc3,rad=0.2"))

        # Set the title of the subgraph
        plt.suptitle(f"Shortest Paths from Node {start_node} to Charging Stations", fontsize=20)

        # Display the plot
        plt.show()
    else:
        # If the subgraph is empty, print a debug message
        print("[DEBUG] Subgraph has no nodes to display.")

# Define the main function that orchestrates the program's execution
def main():
    # Specify the path to the CSV file containing the network data
    filename = '/Users/fatimakhan/Desktop/algorithms final project group 5/network_data.csv'

    # Load the graph data from the CSV file
    graph_structure = load_graph_data(filename)

    # Create a new graph using the NetworkX library
    G = nx.Graph()

    # Add nodes and edges to the graph based on the loaded data
    for node, neighbors in graph_structure.items():
        for neighbor, weight in neighbors.items():
            G.add_edge(node, neighbor, weight=weight)

    # Initialize Tkinter root (for using message boxes) and hide the main window
    root = Tk()
    root.withdraw()

    # Prompt the user to input a starting node
    start_node = input("Enter a source node from A to W (eg. S): ").upper()

    # Check if the start node is valid
    if start_node not in graph_structure:
        # Show an error message if the start node is invalid
        messagebox.showerror("Error", "Invalid starting node.")
        return

    # Define the list of charging stations in the network
    charging_stations = ['H', 'K', 'O', 'T']

    # Calculate and display the paths to each charging station from the start node
    shortest_paths = calculate_and_display_paths(G, start_node, charging_stations)

    # Create and display the subgraph showing the shortest paths
    create_and_display_subgraph(G, start_node, shortest_paths, charging_stations)

# Check if the script is being run directly (not imported)
if __name__ == "__main__":
    # Call the main function to start the program
    main()

















