# Tyler Brown 010479775
import csv
from enum import Enum


class DeliveryStatus(Enum):
    HUB = 0
    EnROUTE = 1
    DELIVERED = 2


class Package:
    def __init__(self, package_id, delivery_address, delivery_city, delivery_state,
                 delivery_zipcode, delivery_deadline, mass_kg, notes):
        self.package_id = package_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zipcode = delivery_zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = mass_kg
        self.notes = notes
        self.delivery_status = "HUB"

    def __str__(self):  # overwriting print(Package)
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.delivery_address, self.delivery_city,
                self.delivery_state, self.delivery_zipcode, self.delivery_deadline, self.mass, self.notes, self.delivery_status)


class Truck:
    def __init__(self, truck_id, location, time, left_hub, pack_limit=16, truck_speed=18):
        self.truck_id = truck_id
        self.location = location
        self.time = time
        self.left_hub = left_hub
        self.pack_limit = pack_limit
        self.packages = []
        self.truck_speed = truck_speed

    def add_package(self, package_id):
        if len(self.packages) >= self.pack_limit:
            print('Truck is full!')
        else:
            self.packages.append(package_id)


class ChainingHashTable:
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert new item into hash table
    def insert(self, key, obj):
        # get bucket list where val will go
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update bucket_list information if key already exists
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = obj
                return True

        # insert val to end of bucket list
        key_value = [key, obj]
        bucket_list.append(key_value)
        return True

    # Search for item in hash table
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Remove item from hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for and remove item.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
        return None


def load_package_data(csv_file, hash_table):
    # https://docs.python.org/3/library/csv.html
    with open(csv_file, newline='') as packages_csv:
        package_data = csv.reader(packages_csv, delimiter=',', quotechar='|')
        next(package_data)  # Skip header
        for row in package_data:
            package_obj = Package(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            hash_table.insert(int(package_obj.package_id), package_obj)


package_hash = ChainingHashTable()

load_package_data('packages.csv', package_hash)

# Get data from hash table
for i in range(len(package_hash.table)*4):
    print("Key: {} and Package {}".format(i+1, package_hash.search(i+1)))

# print(package_hash.search(15))


class Vertex:
    def __init__(self, label):
        self.label = label


def create_distance_array(csv_file):
    with open(csv_file, newline='') as distances_csv:
        distances = csv.reader(distances_csv, delimiter=',', quotechar='|')
        next(distances)  # Skip header
        distance_arr = []
        for row in distances:
            distance_arr.append(row)
        return distance_arr


distance_array = create_distance_array('distances.csv')
print('\n', distance_array)


def create_address_list(csv_file):
    with open(csv_file, newline='') as addresses_csv:
        addresses = csv.reader(addresses_csv, delimiter=',', quotechar='|')
        next(addresses)  # Skip header
        list_addresses = []
        for row in addresses:
            list_addresses.append(row)
        return list_addresses


address_list = create_address_list('addresses.csv')
print('\n', address_list)
print('\n', address_list[1][1])


def address_lookup(address_str, list_addresses):
    row_count = 0
    for row in list_addresses:
        for col in row:
            if address_str in col:
                return row_count
        row_count += 1


print('\n', address_lookup('1330 2100 South', address_list))


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)


def dijkstra_shortest_path(graph, start_vertex):
    # Put all vertices in an unvisited queue
    unvisited_queue = []
    for current_vertex in graph.adjacency_list:
        unvisited_queue.append(current_vertex)

    # start_vertex has a distance of 0 from itself (HUB)
    start_vertex.distance = 0

    # Remove on vertex with each iteration until list is empty
    while len(unvisited_queue) > 0:
        # Visit vertex with minimum distance from start_vertex
        smallest_index = 0
        for i in range(1, len(unvisited_queue)):
            if unvisited_queue[i].distance < unvisited_queue[smallest_index].distance:
                smallest_index = i
        current_vertex = unvisited_queue.pop(smallest_index)

        # Check potential path lengths from current_vertex to all neighbors
        for adj_vertex in graph.adjacency_list[current_vertex]:
            edge_weight = graph.edge_weights[(current_vertex, adj_vertex)]
            alternative_path_distance = current_vertex.ditance + edge_weight

            # If shorter path found, update adj_vertex distance and predecessor
            if alternative_path_distance < adj_vertex.distance:
                adj_vertex.distance = alternative_path_distance
                adj_vertex.pred_vertex = current_vertex


def get_shortest_path(start_vertex, end_vertex):
    # Start from end_vertex and build path backwards
    path = ''
    current_vertex = end_vertex
    while current_vertex is not start_vertex:
        path = ' -> ' + str(current_vertex.label) + path
        current_vertex = current_vertex.pred_vertex
    path = start_vertex.label + path
    return path
