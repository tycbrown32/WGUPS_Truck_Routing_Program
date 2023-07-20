# Tyler Brown 010479775
import csv
from datetime import datetime, date, time, timedelta


class Package:
    def __init__(self, pack_id, delivery_address, delivery_city, delivery_state,
                 delivery_zipcode, delivery_deadline, mass_kg, notes):
        self.package_id = pack_id
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zipcode = delivery_zipcode
        self.delivery_deadline = delivery_deadline
        self.mass = mass_kg
        self.notes = notes
        self.delivery_status = "HUB"
        self.delivery_timestamp = "Waiting delivery.."

    def __str__(self):  # overwriting print(Package)
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.delivery_address, self.delivery_city,
                                                       self.delivery_state, self.delivery_zipcode,
                                                       self.delivery_deadline, self.mass, self.notes,
                                                       self.delivery_status, self.delivery_timestamp)


class Truck:
    def __init__(self, truck_id, time, left_hub, location="HUB", pack_limit=16, truck_speed=18):
        self.truck_id = truck_id
        self.location = location
        self.time = time
        self.left_hub = left_hub
        self.pack_limit = pack_limit
        self.packages = []
        self.truck_speed = truck_speed

    def add_package(self, pack_id):
        if len(self.packages) >= self.pack_limit:
            print('Truck is full!')
        else:
            self.packages.append(pack_id)

    # Move delivery algorithm here?


# ------Chaining Hash Table Class-----------------------------------------------
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


# ------Function to load data into Package objects----------------------------------------
def load_package_data(csv_file, hash_table):
    # https://docs.python.org/3/library/csv.html
    with open(csv_file, newline='') as packages_csv:
        package_data = csv.reader(packages_csv, delimiter=',', quotechar='|')
        next(package_data)  # Skip header
        for row in package_data:
            package_obj = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            hash_table.insert(int(package_obj.package_id), package_obj)


package_hash = ChainingHashTable()  # Create hash table

load_package_data('packages.csv', package_hash)  # Load package data from .csv file

"""
# Get data from hash table
for i in range(len(package_hash.table) * 4):
    print("Key: {} and Package {}".format(i + 1, package_hash.search(i + 1)))

print('\n', package_hash.search(15).package_id)
"""


# -------Create distance array and address list -----------------------------------------
def create_distance_array(csv_file):
    with open(csv_file, newline='') as distances_csv:
        distances = csv.reader(distances_csv, delimiter=',', quotechar='|')
        next(distances)  # Skip header
        distance_arr = []
        for row in distances:
            distance_arr.append(row)
        return distance_arr


distance_array = create_distance_array('distances.csv')
# print('\n\n\nDistance Array: ', distance_array)


def create_address_list(csv_file):
    with open(csv_file, newline='') as addresses_csv:
        addresses = csv.reader(addresses_csv, delimiter=',', quotechar='|')
        next(addresses)  # Skip header
        list_addresses = []
        for row in addresses:
            list_addresses.append(row)
        return list_addresses


address_list = create_address_list('addresses.csv')
# print('\nAddress List: ', address_list)
# print('\nSingle Address: ', address_list[1][1])


def address_lookup(address_str, list_addresses):
    row_count = 0
    for row in list_addresses:
        for col in row:
            if address_str in col:
                return row_count
        row_count += 1


# print('\nAddress Lookup: ', address_lookup('6351 S 900 East', address_list))
# print('\nDistance Between: ',
    # distance_array[address_lookup('6351 S 900 East', address_list)][address_lookup('5025 State St', address_list)])


truck_packages = [package_hash.search(1).package_id, package_hash.search(2).package_id,
                  package_hash.search(3).package_id, package_hash.search(4).package_id,
                  package_hash.search(5).package_id, package_hash.search(6).package_id,
                  package_hash.search(7).package_id, package_hash.search(8).package_id,
                  package_hash.search(9).package_id, package_hash.search(10).package_id,
                  package_hash.search(11).package_id, package_hash.search(12).package_id,
                  package_hash.search(13).package_id, package_hash.search(14).package_id,
                  package_hash.search(15).package_id, package_hash.search(16).package_id]

# print('\nTRUCK PACKAGE: ', package_hash.search(int(truck_packages[0])).delivery_address, '\n\n')


curr_time = datetime(2023, 7, 19, 8, 0)
# tdelta = timedelta(minutes=12)
# print(type(curr_time), '  ', type(tdelta))
# print(curr_time + tdelta)


def delivery_algorithm(pack_list, current_time):  # Trying for nearest neighbor
    avg_speed = 18 / 60  # avg_speed in miles per minute

    # Determine the next address and associated distance
    curr_address = address_lookup('4001 S 700 East', address_list)  # Always start package delivery from HUB
    total_distance = 0
    while len(pack_list) > 0:
        short_distance = float("inf")  # Next distance will always be less than infinity so next address will update

        # Determine the package with the nearest delivery location
        package_index = 0
        for package in pack_list:
            tmp_next_address = address_lookup(package_hash.search(int(pack_list[package_index])).delivery_address, address_list)
            tmp_distance = float(distance_array[tmp_next_address][curr_address])

            # If the temp_distance is less than the current short_distance -> update short_distance
            if tmp_distance < short_distance:
                next_address = tmp_next_address
                short_distance = tmp_distance
                remove_package = package

            package_index += 1  # Iterate to next package to determine distance from current location

        # Travel to next destination. Update current address (with next_address).
        travel_time = timedelta(minutes=(short_distance / avg_speed))  # Calculate travel time (minutes)
        curr_address = next_address  # Update current address
        current_time = current_time + travel_time

        # 'Deliver' package by removing it from the truck's package list and timestamping it.
        print('Heading to address ', package_hash.search(next_address).delivery_address, ', ', short_distance,
              ' miles. Delivering package ', remove_package, '. Package delivered at ', current_time.strftime('%H:%M'), '.')

        pack_list.remove(remove_package)
        package_hash.search(remove_package).delivery_status = "DELIVERED"
        package_hash.search(remove_package).delivery_timestamp = current_time.strftime('%H:%M')
        total_distance = float("%0.2f" % (total_distance + short_distance))

        print('Truck package list: ', pack_list)
        print('Current address is ', curr_address, '. Total distance travelled is ',
              total_distance, ' miles.\n')

    print('\nReturning to HUB.')
    distance_to_hub = float(distance_array[0][curr_address])
    time_at_hub = current_time + timedelta(minutes=(distance_to_hub / avg_speed))
    total_distance = total_distance + distance_to_hub  # Calculate distance after return to HUB
    print('\nTotal distance travelled was ', total_distance, ' miles. Current time is ', time_at_hub.strftime('%H:%M'), '.')


print("DELIVERING:")
delivery_algorithm(truck_packages, curr_time)

print(package_hash.search(16))

"""
# ------Dijkstra Algorithm---------------------------------------------------
class Vertex:
    def __init__(self, label):
        self.label = label


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
"""
