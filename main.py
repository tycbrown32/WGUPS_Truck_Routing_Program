# Tyler Brown 010479775
import csv
from datetime import datetime, timedelta


# Package Class --------------------------------------------------------------------------------------------------------
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
        self.delivery_status = "AT HUB"
        self.status_update_time = "Waiting delivery.."

    def __str__(self):  # overwriting print(Package)
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.delivery_address, self.delivery_city,
                                                           self.delivery_state, self.delivery_zipcode,
                                                           self.delivery_deadline, self.mass, self.notes,
                                                           self.delivery_status, self.status_update_time)


# Truck Class ----------------------------------------------------------------------------------------------------------
class Truck:
    def __init__(self, truck_id, truck_time, location="AT HUB", pack_limit=16, speed=18):
        self.id = truck_id
        self.location = location
        self.truck_time = truck_time
        self.pack_limit = pack_limit
        self.packages = []
        self.speed = speed
        self.distance_travelled = float("%0.2f" % 0)

    def add_package(self, pack_id):
        if len(self.packages) >= self.pack_limit:
            print('Truck is full!')
        else:
            self.packages.append(pack_id)

    def load_packages_onto_truck(self, packs):
        for pack in packs:
            self.add_package(pack)
            package_hash.search(pack).delivery_status = "IN ROUTE"
            package_hash.search(pack).status_update_time = self.truck_time.strftime("%H:%M")

    # Package delivery algorithm using nearest neighbor. Runtime O(n) = xx. Space Complexity O(n) = xx.
    def package_delivery(self):
        avg_speed = self.speed / 60  # Average speed in miles per minute

        # Determine the next address and associated distance
        curr_address = address_lookup('4001 S 700 East', address_list)  # Always start package delivery from HUB

        # Loop through package list until list is empty
        while len(self.packages) > 0:
            short_distance = float("inf")  # Next distance will always be less than infinity so next address will update

            # Determine the package with the nearest delivery location
            package_index = 0
            for package in self.packages:
                tmp_next_address = address_lookup(package_hash.search(int(self.packages[package_index])).delivery_address,
                                                  address_list)
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
            self.truck_time = self.truck_time + travel_time

            # 'Deliver' package by removing it from the truck's package list and timestamping it.
            """ print('Heading to address ', package_hash.search(next_address).delivery_address, ', ', short_distance,
                  ' miles. Delivering package ', remove_package, '. Package delivered at ',
                  self.truck_time.strftime('%H:%M'), '.')"""

            self.packages.remove(remove_package)
            package_hash.search(remove_package).delivery_status = "DELIVERED"
            package_hash.search(remove_package).status_update_time = self.truck_time.strftime('%H:%M')
            self.distance_travelled = float("%0.2f" % (self.distance_travelled + short_distance))

            """print('Truck package list: ', self.packages)
            print('Current address is ', curr_address, '. Total distance travelled is ',
                self.distance_travelled, ' miles.\n')"""

        # 'Return to hub'. Update distance travelled by truck and time truck returned to hub.
        """print('\nReturning to HUB.')"""
        distance_to_hub = float(distance_array[0][curr_address])  # Calculate distance back to hub
        self.truck_time = self.truck_time + timedelta(minutes=(distance_to_hub / avg_speed))  # Calculate and update time returned to hub
        self.distance_travelled = self.distance_travelled + distance_to_hub  # Calculate distance after return to HUB
        """print('Total distance travelled was ', self.distance_travelled, ' miles. Current time is ',
              self.truck_time.strftime('%H:%M'), '.\n\n')"""

    def __str__(self):  # overwriting print(Truck)
        return "%s, %s, %s, %s" % (self.id, self.location, self.truck_time.strftime("%H:%M"), self.distance_travelled)


# Chaining Hash Table Class---------------------------------------------------------------------------------------------
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

        # Insert val to end of bucket list
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


package_hash = ChainingHashTable()  # Create hash table


# Function to load data from .csv file into Package objects-------------------------------------------------------------
def load_package_data(csv_file, hash_table):
    # https://docs.python.org/3/library/csv.html
    with open(csv_file, newline='') as packages_csv:
        package_data = csv.reader(packages_csv, delimiter=',', quotechar='|')
        next(package_data)  # Skip header
        for row in package_data:
            package_obj = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            hash_table.insert(int(package_obj.package_id), package_obj)


load_package_data('packages.csv', package_hash)  # Load package data from .csv file

"""
# Get data from hash table
for i in range(len(package_hash.table) * 4):
    print("Key: {} and Package {}".format(i + 1, package_hash.search(i + 1)))
"""


# Create distance array and address list from .csv file ----------------------------------------------------------------
def create_distance_array(csv_file):
    with open(csv_file, newline='') as distances_csv:
        distances = csv.reader(distances_csv, delimiter=',', quotechar='|')
        next(distances)  # Skip header
        distance_arr = []
        for row in distances:
            distance_arr.append(row)
        return distance_arr


distance_array = create_distance_array('distances.csv')  # Create array of distances


# Create address list from .csv file -----------------------------------------------------------------------------------
def create_address_list(csv_file):
    with open(csv_file, newline='') as addresses_csv:
        addresses = csv.reader(addresses_csv, delimiter=',', quotechar='|')
        next(addresses)  # Skip header
        list_addresses = []
        for row in addresses:
            list_addresses.append(row)
        return list_addresses


address_list = create_address_list('addresses.csv')  # Create address list


# Address lookup function to determine a number associated with and address --------------------------------------------
def address_lookup(address_str, list_addresses):
    row_count = 0
    for row in list_addresses:
        for col in row:
            if address_str in col:
                return row_count
        row_count += 1

"""
def delivery_time(check_time):
    for pack in package_hash:
        if package_hash.search(pack).delivery_status == "DELIVERED" and
            package_hash.search(pack).status_update_time >= check_time:
"""


# WGUPS Operation execution --------------------------------------------------------------------------------------------
truck1_start_time = datetime(2023, 7, 19, 8, 0)  # truck1 starts its first delivery at 8:00 AM
truck2_start_time = datetime(2023, 7, 19, 9, 5)  # truck2 starts its first delivery at 9:05 AM when delayed packages arrive

tp1 = [13, 39, 14, 15, 16, 34, 19, 20, 21, 29, 7, 30, 8, 31, 32, 6]
tp2 = [2, 33, 10, 11, 12, 17, 22, 23, 24]
tp3 = [4, 40, 1, 25, 26, 38, 5, 37]
tp4 = [3, 18, 36, 28, 35, 27, 9]

print("DELIVERING:")
truck1 = Truck(1, truck1_start_time)
truck2 = Truck(2, truck2_start_time)

truck1.load_packages_onto_truck(tp1)
truck1.package_delivery()

truck2.load_packages_onto_truck(tp2)
truck2.package_delivery()

truck1.load_packages_onto_truck(tp3)
truck1.package_delivery()

truck2.load_packages_onto_truck(tp4)
truck2.package_delivery()


req_time = input("Enter time to check package delivery status: ")

print('Package 1 delivered at ', package_hash.search(1).status_update_time, '\n',
      'Package 6 delivered at ', package_hash.search(6).status_update_time, '\n',
      'Package 13 delivered at ', package_hash.search(13).status_update_time, '\n',
      'Package 14 delivered at ', package_hash.search(14).status_update_time, '\n',
      'Package 15 delivered at ', package_hash.search(15).status_update_time, '\n',
      'Package 16 delivered at ', package_hash.search(16).status_update_time, '\n',
      'Package 20 delivered at ', package_hash.search(20).status_update_time, '\n',
      'Package 25 delivered at ', package_hash.search(25).status_update_time, '\n',
      'Package 29 delivered at ', package_hash.search(29).status_update_time, '\n',
      'Package 30 delivered at ', package_hash.search(30).status_update_time, '\n',
      'Package 31 delivered at ', package_hash.search(31).status_update_time, '\n',
      'Package 34 delivered at ', package_hash.search(34).status_update_time, '\n',
      'Package 37 delivered at ', package_hash.search(37).status_update_time, '\n',
      'Package 40 delivered at ', package_hash.search(40).status_update_time, '\n')
print('Total distance travelled is', float("%0.2f" % (truck1.distance_travelled + truck2.distance_travelled)), 'miles.')
