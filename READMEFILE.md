# EV Charging Station Route Optimization Application

## Project Description
The EV Charging Station Route Optimization Application aims to enhance user convenience for electric vehicle (EV) drivers by analyzing distances between different charging station locations. This application helps users find efficient routes by selecting a starting location within a 23-node network, determining the fastest path to each charging station, and recommending the best route.

## Project Requirements
This project requires:
- Python 3.x
- `matplotlib`
- `networkx`
- `tkinter`
- `csv`

## Installation
pip install matplotlib networkx

### Prerequisites
Ensure you have Python 3.x installed on your machine

### Setting Up the Environment

1. **Install Conda**

2. **Create a Virtual Environment**:
    ```sh
    conda create -n ev-route-optimization python=3.8
    conda activate ev-route-optimization
    ```

3. **Install Required Libraries**:
    ```sh
    pip install matplotlib networkx
    ```

## Usage

1. Ensure the script (`Algorithms Group Project.py`) and the CSV file (`network_data.csv`) are in the same directory.

2. **Run the Script**:
    ```sh
    python "Algorithms Group Project.py"
    ```

3. Enter the starting node in the prompt when requested.

### File Structure
- `Algorithms Group Project.py`: Main Python script to run the application.
- `network_data.csv`: CSV file containing the graph data.
- `README.md`: Instructions and information about the project.

## Creating the `network_data.csv` File

The CSV file should contain the graph data representing nodes and their connections with weights. Here's how you can create it:

### Steps to Create `network_data.csv`:

1. Open a text editor or a spreadsheet software like Excel.
2. Enter the following data:

A,B,6,F,5,,,,
B,A,6,C,5,G,6,,
C,B,5,D,7,H,5,,
D,C,7,E,7,I,8,,
E,D,7,I,6,N,15,,
F,A,5,G,8,J,7,,
G,B,6,F,8,H,9,K,8
H,C,5,G,9,I,12,,
I,D,8,E,6,H,12,M,10
J,F,7,K,5,O,7,,
K,G,8,J,5,L,7,,
L,K,7,M,7,P,7,,
M,I,10,L,7,N,9,,
N,E,15,M,9,R,7,,
O,J,7,P,13,S,9,,
P,L,7,O,13,Q,8,U,11
Q,P,8,R,9,,,,
R,N,7,Q,9,W,10,,
S,O,9,T,9,,,,
T,S,9,U,8,,,,
U,P,11,T,8,V,8,,
V,U,8,W,5,,,,
W,R,10,V,5,,,,

3. Save the file as `network_data.csv`.

## Acknowledgments
This project was developed by group 5. Special thanks to the course instructors for their guidance and support.

## License
This project is licensed under the MIT License.

## Contact
For any questions or comments, please contact fatima.khan4@ontariotechu.ca

---

## Group Project Details

**Course**: INFR-2820U ALGORITHMS & DATA STRUCTURES

