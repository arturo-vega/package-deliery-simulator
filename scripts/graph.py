import csv

# Creates a graph from the files nodetables.csv and distancetables.csv
class Node:

    totalNodes = 1
    
    def __init__(self, nameAddress, address, zipcode):
        self.nameAddress = nameAddress
        self.address = address
        self.zipcode = zipcode
        # The id is based off of how many nodes have been created so far
        self.id = self.__class__.totalNodes
        self.__class__.totalNodes += 1
        # Stores the id of the edges that each node has
        self.edgeIds = []

    def __str__(self):
        return f"Node ID: {self.id}\nAddress: {self.address}\nZipcode: {self.zipcode}\nEdges: {self.edgeIds}"


class Edge:

    totalEdges = 0

    # Takes in two node objects and a float distance, edge id is based off of how
    # many edges have been created so far.
    def __init__(self, startNode, endNode, distance):
        self.startNode = startNode
        self.endNode = endNode
        self.distance = distance

        self.startNodeId = startNode.id
        self.endNodeId = endNode.id

        self.id = self.__class__.totalEdges
        startNode.edgeIds.append(self.id)
        endNode.edgeIds.append(self.id)
        self.__class__.totalEdges += 1

    def __str__(self):
        return f"Edge {self.id}: {self.startNode.nameAddress} -> {self.endNode.nameAddress}, Distance: {self.distance}"


# Class that holds all edges and nodes and contains the functions for getting them
# from a csv file
class Graph:

    def __init__(self):
        self.nodes = []
        self.edges = []

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, edge):
        self.edges.append(edge)

    # finds a node corresponding to an address
    def get_node(self, address):
        for node in self.nodes:
            if address == node.address:
                return node

    # gets the edge between two addresses
    def get_edge(self, address1, address2):
        node1 = self.get_node(address1)
        node2 = self.get_node(address2)

        for edge in self.edges:
            if (node1 == edge.startNode and node2 == edge.endNode) or (node2 == edge.startNode and node1 == edge.endNode):
                return edge
    # End up never using this
    def get_edge_by_id(self, id):
        for edge in edges:
            if edge.id == id:
                return edge
    # Ended up being redundant since all nodes are connected to each other
    # However could be useful in a case where not all nodes are connected to all
    # other nodes
    def get_neighbors(self, node):
        neighbors = []
        for edge in self.edges:
            if edge.startNode == node:
                neighbors.append(edge.endNode)
            elif edge.endNode == node:
                neighbors.append(edge.startNode)
        return neighbors

    # Gets the distance between two nodes/length of an edge
    def get_edge_weight(self, node1, node2):
        edge = self.get_edge(node1.address, node2.address)
        return edge.distance

    # Takes a starting address and an array of addresses as strings
    # Finds the shortest edge for each node in the list starting with the start address
    # This node is appended to the path and then starts again, returns a list of
    # strings that are the address
    def shortest_path(self, startAddress, nodeList):
        path = [startAddress]
        currentAddress = startAddress

        while len(path) < len(nodeList) + 1:
            currentNode = self.get_node(currentAddress)
            shortestEdge = None
            shortestDistance = float('inf')
            nextAddress = None

            for neighbor in self.get_neighbors(currentNode):
                edge = self.get_edge(currentAddress, neighbor.address)

                if edge.distance < shortestDistance and neighbor.address in nodeList and neighbor.address not in path:
                    shortestEdge = edge
                    shortestDistance = edge.distance
                    nextAddress = neighbor.address

            if nextAddress is None:
                break #No more nodes to look for
            path.append(nextAddress)
            currentAddress = nextAddress

        return path

    def import_nodes(self,fileName):
        with open(fileName, 'r') as file:
            reader = csv.reader(file)

            for row in reader:
                nameAddress, address = row
                # Split the address based on parentheses
                addressParts = address.split('(')
                nameAddressParts = nameAddress.splitlines()
                # Makes sure there is a zipcode in the second row of the nodetable.csv
                # WGU is the only one that doesn't have this so I just input it manually
                if len(addressParts) > 1:
                    address = nameAddressParts[1].strip()
                    zipcode = addressParts[1].split(')')[0].strip()

                else:
                    address = "4001 South 700 East"
                    zipcode = 84107

                self.add_node(Node(nameAddress, address, zipcode))

    # Can only be used after nodes are already imported
    # Should end up with 378 edges
    def import_edges(self,fileName):
        with open(fileName, 'r') as file:
            reader = csv.reader(file)
            nodeNames = [node.nameAddress for node in self.nodes]

            for columnIndex, column in enumerate(reader):
                startNode = self.nodes[columnIndex]

                for rowIndex, value in enumerate(column):
                    if value.strip():
                        endNode = self.nodes[rowIndex]
                        distance = float(value)
                        self.add_edge(Edge(startNode, endNode, distance))