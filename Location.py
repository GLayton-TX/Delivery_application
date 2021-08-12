# class to represent the locations and their corresponding distances from one another

import csv

filename = "location_and_distance_table.csv"


# location object used to hold location data
class Location:
    # time_space complexity of O(1)
    def __init__(self, location_id, name, address, zipcode, distance_list):
        self.location_id = location_id
        self.name = name
        self.address = address
        self.zipcode = zipcode
        self.distance_list = distance_list


# gets the data from locations_and_distance_table.csv file
# time_space complexity of O(N)
def load_distance_info():
    with open(filename) as distances:
        distance_data = csv.reader(distances, delimiter=",")
        locations = []
        for info in distance_data:
            location_id = int(info[0])
            location_name = info[1]
            location_address = info[2]
            location_zip = info[3]
            location_distance = get_distance_info(info)
            temp_location = Location(location_id, location_name, location_address, location_zip, location_distance)
            locations.append(temp_location)
    return locations


# takes distance table info from csv and parses it into an array so it is easier to access
# time_space complexity of O(1)
def get_distance_info(info):
    locations = []
    i = 4
    while i < len(info):
        locations.append(float(info[i]))
        i += 1
    return locations


# loaded location information saved so that we don't have to call the method each time we need to go through the data
# time_space complexity of O(N)
location_distances = load_distance_info()


# returns the location from all locations that matches the search criteria
# time_space complexity of O(N)
def get_location(search_id):
    location = [location for location in location_distances if location.location_id == search_id]
    return location[0]


# returns all the locations created from the .csv
# time_space complexity of O(1)
def get_all_locations():
    return location_distances


# gets the distance between 2 locations according to the distance table provided
# since the distance table is bidirectional not all columns will be filled out for all locations
# this handles it by correcting the order the parameters are passed to the lookup
# time_space complexity of O(1)
def get_distance(current_location, destination):
    if current_location.location_id < destination.location_id:
        swap: Location = current_location
        current_location = destination
        destination = swap
    distance = current_location.distance_list[destination.location_id]
    return distance


# returns the location id number from the locations list for an address from a package
# same as a foreign key lookup
# time_space complexity of O(N)
def get_location_id(package_address):
    location = [location for location in get_all_locations() if package_address == location.address]
    return location[0].location_id
