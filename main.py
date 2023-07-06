# Tyler Brown 010479775

class Package:
    def __init__(self, package_id, street, city, state, zipcode, deadline, mass_kg, status):
        self.package_id = package_id
        self.street = street
        self.city = city
        self.state = state
        self.zip = zipcode
        self.deadline = deadline
        self.mass = mass_kg
        self.status = status


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
    def __init__(self, initial_capacity=40):
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Insert new item into hash table
    def insert(self, item):
        bucket = hash(item) % len(self.table)
        bucket_list = self.table[bucket]

    # Search for item in hash table
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for key in bucket list
        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            # If key is not found.
            return None

    # Remove item from hash table
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]

        # Search for and remove item.
        if key in bucket_list:
            bucket_list.remove(key)


"""
Populate hash table.
    Pull in data from Excel
    Instantiate packages
    Insert packages to hash table

Load trucks
    Pull package id from hash table
        Verify that package is able to go with said truck
        Confirm that package is loaded with 'sister' packages
        Change package status to "en route"

Send trucks out
    Change status of package to "delivered" once delivered
"""
