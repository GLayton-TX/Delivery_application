# Package class for creating package objects

import csv
import HashTable
import Location
import Utility

filename = "package_list.csv"


# package object used to represent the packages for delivery
class Package:

    # default constructor, assigns all info into the new object
    # time_space complexity of O(1)
    def __init__(self, package_id, package_destination_id, package_address, package_city, package_state, package_zip,
                 package_deadline, package_mass, package_notes, package_status, package_truck_number, package_load_time, package_delivered_at):
        self.package_id = package_id
        self.package_destination_id = package_destination_id
        self.package_address = package_address
        self.package_city = package_city
        self.package_state = package_state
        self.package_zip = package_zip
        self.package_deadline = package_deadline
        self.package_mass = package_mass
        self.package_notes = package_notes
        self.package_status = package_status
        self.package_truck_number = package_truck_number
        self.package_load_time = package_load_time
        self.package_delivered_at = package_delivered_at

    # constructor that takes in another package as an object
    # reduces parameters needed to be passed in when copying package objects for reporting
    # time_space complexity of O(1)
    @classmethod
    def copy_package(cls, package):
        copied = Package(package.package_id,
                         package.package_destination_id,
                         package.package_address,
                         package.package_city,
                         package.package_state,
                         package.package_zip,
                         package.package_deadline,
                         package.package_mass,
                         package.package_notes,
                         package.package_status,
                         package.package_truck_number,
                         package.package_load_time,
                         package.package_delivered_at)
        return copied


# gets all data from the package_list.csv file and inserts into a hash table
# time_space complexity of O(N)
def load_package_info():
    with open(filename) as packages:
        package_data = csv.reader(packages, delimiter=",")
        my_hash = HashTable.ChainingHashTable()
        i = 0
        for temp_package in package_data:
            package_id = int(temp_package[0])
            package_address = temp_package[1]
            package_destination_id = Location.get_location_id(package_address)
            package_city = temp_package[2]
            package_state = temp_package[3]
            package_zip = temp_package[4]
            package_deadline = temp_package[5]
            package_mass = int(temp_package[6])
            package_notes = temp_package[7]
            package_status = "At Hub"
            package_truck_number = 0
            package_load_time = ""
            package_delivered_at = 0.0

            temp_package = Package(package_id, package_destination_id, package_address, package_city, package_state, package_zip,
                                   package_deadline, package_mass, package_notes, package_status, package_truck_number, package_load_time, package_delivered_at)

            my_hash.insert(package_id, temp_package)

    return my_hash


# loaded package information saved so that we don't have to call the method each time we need to go through the data
# time_space complexity of O(N)
package_list = load_package_info()


# Algorithm used to determine the next closest destination from available packages loaded on truck
# returns the package who's location is the closest to the current location of the truck
# time_space complexity of O(N^2)
def greedy(manifest, current_location):
    closest = 100.0
    next_package = None
    for package in manifest:
        if Location.get_distance(current_location, Location.get_location(package.package_destination_id)) < closest:
            closest = Location.get_distance(current_location, Location.get_location(package.package_destination_id))
            next_package = package
    return next_package


# returns a list of all the objects from the hashed dataset
# time_space complexity of O(N)
def get_all_packages():
    object_list = [package_list.search(i) for i in range(1, 41)]
    return object_list


# updates the address of a particular package object
# time_space complexity of O(N)
def update_address(package_id, street_address, city, state, zipcode, notes, manual_list):
    def set_new_address(package_to_update):
        package_to_update.package_address = street_address
        package_to_update.package_destination_id = Location.get_location_id(street_address)
        package_to_update.package_city = city
        package_to_update.package_state = state
        package_to_update.package_zip = zipcode
        package_to_update.package_notes = notes

    [set_new_address(package) for package in manual_list if package.package_id == package_id]


# creates a report for the package requested
# prints this report to the CLI
# time_space complexity of O(N)
def get_package_info(package):
    Utility.create_report(package)
