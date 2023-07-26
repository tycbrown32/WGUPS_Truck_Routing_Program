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
        self.time_left_hub = "7:00"
        self.truck = "No Truck"
        self.delivery_time = "8:00"

    def __str__(self):  # overwriting print(Package)
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s" % (self.package_id, self.delivery_address,
                                                                   self.delivery_city, self.delivery_state,
                                                                   self.delivery_zipcode, self.delivery_deadline,
                                                                   self.mass, self.notes, self.delivery_status,
                                                                   self.time_left_hub, self.truck, self.delivery_time)


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

    # Method to singularly 'load' packages to truck.
    # Runtime complexity = O(1). Space Complexity = O(1)
    def add_package(self, pack_id):
        if len(self.packages) >= self.pack_limit:
            print('Truck is full!')
        else:
            self.packages.append(pack_id)

    # Method for loading truck given a list of packages. Also updates package objects.
    # Runtime complexity = O(n^2). Space Complexity = O(n)
    def load_packages_onto_truck(self, packs):
        for pack in packs:
            self.add_package(pack)
            package_hash.search(pack).delivery_status = "IN ROUTE"
            package_hash.search(pack).time_left_hub = self.truck_time.strftime("%H:%M")
            package_hash.search(pack).truck = 'Truck ' + str(self.id)

    # Package delivery algorithm using nearest neighbor.
    # Runtime = O(n^3). Space Complexity = O(n).
    def package_delivery(self):
        avg_speed = self.speed / 60  # Average speed in miles per minute.

        # Determine the next address and associated distance
        curr_address = address_lookup('4001 S 700 East', address_list)  # Always start package delivery from hub.

        # Loop through package list until list is empty.
        while len(self.packages) > 0:
            short_distance = float("inf")  # Next distance will always be less than 'inf' so next address will update.

            # Determine the package with the nearest delivery location.
            pack_index = 0
            for package in self.packages:
                new_next_address = address_lookup(package_hash.search(int(self.packages[pack_index])).delivery_address,
                                                  address_list)
                new_distance = float(distance_array[new_next_address][curr_address])

                # If the temp_distance is less than the current short_distance -> update short_distance.
                if new_distance < short_distance:
                    next_address = new_next_address
                    short_distance = new_distance
                    removal_package = package  # ID of package to be removed

                pack_index += 1  # Iterate to next package to determine distance from current location.

            # Travel to next destination. Update current address (with next_address).
            travel_time = timedelta(minutes=(short_distance / avg_speed))  # Calculate travel time (minutes).
            curr_address = next_address  # Update current address.
            self.truck_time = self.truck_time + travel_time

            # 'Deliver' package by removing it from the truck's package list and timestamping it.
            self.packages.remove(removal_package)
            package_hash.search(removal_package).delivery_status = "DELIVERED"
            package_hash.search(removal_package).delivery_time = self.truck_time.strftime('%H:%M')
            self.distance_travelled = float("%0.2f" % (self.distance_travelled + short_distance))

        # 'Return to hub'. Update distance travelled by truck and time truck returned to hub.
        distance_to_hub = float(distance_array[0][curr_address])  # Calculate distance back to hub.
        time_to_hub = distance_to_hub / avg_speed  # Calculate time to return to hub (minutes).
        self.truck_time = self.truck_time + timedelta(minutes=time_to_hub)  # Calculate and update time returned to hub.
        self.distance_travelled = self.distance_travelled + distance_to_hub  # Calculate distance after return to hub.

    def __str__(self):  # overwriting print(Truck)
        return "%s, %s, %s, %s" % (self.id, self.location, self.truck_time.strftime("%H:%M"), self.distance_travelled)


# Chaining Hash Table Class---------------------------------------------------------------------------------------------
# Runtime complexity = O(n). Space Complexity = O(n)
class ChainingHashTable:
    # Initialize hash table.
    def __init__(self, initial_capacity=10):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert new object into hash table.
    def insert(self, key, obj):
        # Get bucket list where obj will be inserted.
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Update bucket_list information if key already exists.
        for kv in bucket_list:
            if kv[0] == key:
                kv[1] = obj
                return True

        # Insert key_value to end of bucket list.
        key_value = [key, obj]
        bucket_list.append(key_value)
        return True

    # Search for and return object from hash table.
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        for kv in bucket_list:
            if kv[0] == key:
                return kv[1]
        return None

    # Remove object from hash table.
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for and remove item.
        for kv in bucket_list:
            if kv[0] == key:
                bucket_list.remove(kv)
        return None


package_hash = ChainingHashTable()  # Define a hash table.
package_hash_key = []  # List of keys for the hash table. Provides a method for iterating the hash table.


# Function to load data from .csv file into Package objects-------------------------------------------------------------
# Runtime complexity = O(n). Space Complexity = O(n)
def load_package_data(csv_file, hash_table, hash_key):
    # https://docs.python.org/3/library/csv.html
    with open(csv_file, newline='') as packages_csv:
        package_data = csv.reader(packages_csv, delimiter=',', quotechar='|')
        next(package_data)  # Skip header
        for row in package_data:
            package_obj = Package(int(row[0]), row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            hash_table.insert(int(package_obj.package_id), package_obj)
            hash_key.append(int(row[0]))


load_package_data('packages.csv', package_hash, package_hash_key)  # Load package data from .csv file.


# Create distance array and address list from .csv file ----------------------------------------------------------------
# Runtime complexity = O(n). Space Complexity = O(n)
def create_distance_array(csv_file):
    with open(csv_file, newline='') as distances_csv:
        distances = csv.reader(distances_csv, delimiter=',', quotechar='|')
        next(distances)  # Skip header
        distance_arr = []
        for row in distances:
            distance_arr.append(row)
        return distance_arr


distance_array = create_distance_array('distances.csv')  # Create array of distances.


# Create address list from .csv file -----------------------------------------------------------------------------------
# Runtime complexity = O(n). Space Complexity = O(n)
def create_address_list(csv_file):
    with open(csv_file, newline='') as addresses_csv:
        addresses = csv.reader(addresses_csv, delimiter=',', quotechar='|')
        next(addresses)  # Skip header
        list_addresses = []
        for row in addresses:
            list_addresses.append(row)
        return list_addresses


address_list = create_address_list('addresses.csv')  # Create address list.


# Address lookup function: provides a number to be associated with an address ------------------------------------------
# Runtime complexity = O(n^2). Space Complexity = O(n^2)
def address_lookup(address_str, list_addresses):
    row_count = 0
    for row in list_addresses:
        for col in row:
            if address_str in col:
                return row_count
        row_count += 1


# Function to determine package status at a specified time -------------------------------------------------------------
# Runtime complexity = O(n^2). Space Complexity = O(n).
def package_status(check_time, hash_table, hash_table_key):
    for pack in hash_table_key:
        delivery_time_str = hash_table.search(pack).delivery_time
        delivery_time = time_correction(delivery_time_str)

        time_left_hub_str = hash_table.search(pack).time_left_hub
        time_left_hub = time_correction(time_left_hub_str)

        if delivery_time <= check_time:
            print('Package ', pack, ' delivered.')
        elif time_left_hub <= check_time:
            print('Package ', pack, ' in route.')
        else:
            print('Package ', pack, ' at Hub.')


# Function to adjust a time to "Today" when given hour and minute string inputs ----------------------------------------
# Runtime complexity = O(1). Space Complexity = O(1)
def time_correction(time_str):
    time_hour = datetime.strptime(time_str, "%H:%M").hour
    time_minute = datetime.strptime(time_str, "%H:%M").minute

    curr_year = datetime.today().year
    curr_month = datetime.today().month
    curr_day = datetime.today().day

    corrected_time = datetime(curr_year, curr_month, curr_day, time_hour, time_minute)
    return corrected_time


# WGUPS Operation execution --------------------------------------------------------------------------------------------
# Establish today's month, day, and year.
month = datetime.today().month
day = datetime.today().day
year = datetime.today().year

truck1_start_time = datetime(year, month, day, 8, 0)  # truck1 starts first delivery at 8:00AM
truck2_start_time = datetime(year, month, day, 9, 5)  # truck2 starts first delivery at 9:05AM (delayed packages arrive)

tp1 = [13, 39, 14, 15, 16, 34, 19, 20, 21, 29, 7, 30, 8, 31, 32, 6]
tp2 = [2, 33, 10, 11, 12, 17, 22, 23, 24]
tp3 = [4, 40, 1, 25, 26, 38, 5, 37]
tp4 = [3, 18, 36, 28, 35, 27, 9]

# Begin delivery process.
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

print('\nTotal distance travelled was', float("%0.2f" % (truck1.distance_travelled + truck2.distance_travelled)),
      'miles.\n')

# User interface -------------------------------------------------------------------------------------------------------
# Runtime complexity = O(n^2). Space Complexity = O(n)
next_step = 'm'  # Initialize variable to go to the 'main menu'
while next_step != 'e':
    check = input("\nCheck delivery status (d) OR view package information (v) OR exit (e): ")

    if check == 'd':
        # Ask user for time to view package status. Convert time string to datetime
        req_time_str = input("\nEnter time to check package delivery status (H:M, 24-hour): ")
        req_time = time_correction(req_time_str)

        package_status(req_time, package_hash, package_hash_key)
    elif check == 'v':
        packageID = input("\nEnter package ID for package info  or 'all' for info of all packages. ")
        print('')

        if packageID == 'all':  # Print information for all packages.
            for item in package_hash_key:
                print('Package ', item, ': ', package_hash.search(item))
        else:  # Print information for provided package id.
            print('Package ', packageID, ': ', package_hash.search(int(packageID)))
    else:
        next_step = 'e'
        print("\nExiting application.")
        break

    next_step = input("\nReturn to main menu (m) OR exit (e)? ")
    if next_step == 'e':
        print("\nExiting application.")

