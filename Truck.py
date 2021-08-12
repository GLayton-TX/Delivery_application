# class for the truck object

# max of 16 packages
# travel at 18mph
# 3 trucks but only 2 drivers
# 8am earliest departure from hub

import Location
import Utility
import Package


# the truck object, initializes with parameters set in the assessment
# time_space complexity of O(1)
class Truck:

    def __init__(self):
        self.truck_number = 1
        self.speed = 18
        self.trip_odometer = 0.0
        self.odometer = 0.0
        self.time_out = 0.0
        self.location: Location = Location.get_location(0)
        self.max_cargo = 16
        self.cargo = []
        self.is_full = False
        self.delivered = []
        self.start_time = 0

    # takes a package object and loads it into the truck objects cargo list
    # updates packages values
    # ensures that the maximum of packages the truck can hold is not exceeded
    # time_space complexity of O(1)
    def load_package(self, package: Package):
        if len(self.cargo) < self.max_cargo:
            self.cargo.append(package)
            package.package_status = "En Route"
            package.package_truck_number = self.truck_number
            package.package_load_time = Utility.format_min_to_time(self.time_out + self.start_time)
        else:
            self.is_full = True
            print(f"Truck is full did not load package #{package.package_id}")

    # removes a package from the trucks cargo
    # could be used if there was a transfer of packages between trucks or returned to hub without being delivered
    # time_space complexity of O(1)
    def remove_package(self, package):
        self.cargo.remove(package)

    # delivers a package from a trucks cargo
    # updates package's info
    # moves package data from cargo to delivered
    # time_space complexity of O(N))
    def deliver_package(self, package_id):
        delivered_at = self.start_time + self.time_out

        # updates the relevant package data upon delivery
        # time_space complexity of O(1)
        def update_on_delivery(package):
            package.package_delivered_at = delivered_at
            package.package_status = "Delivered"
            self.delivered.append(package)
            self.remove_package(package)

        [update_on_delivery(package) for package in self.cargo if package.package_id == package_id]

    # resets truck data for the start of a route
    # could be used if you wanted to see data from each run the truck makes as opposed to total data
    # time_space complexity of O(1)
    def start_route(self):
        self.time_out = 0.0
        self.location = Location.get_location(0)
        self.trip_odometer = 0.0
        self.cargo = []
        self.is_full = False
        self.delivered = []

    # simulates the truck moving from location to location
    # updates the location attribute, as well as the odometer's and timers
    # time_space complexity of O(1)
    def drive_truck(self, destination_id):
        destination = Location.get_location(destination_id)
        distance = Location.get_distance(self.location, destination)
        self.time_out += (distance / self.speed) * 60
        self.trip_odometer += distance
        self.odometer += distance
        self.location = destination

    # boolean value for whether the truck has no more packages in cargo
    # time_space complexity of O(1)
    def truck_is_empty(self):
        if len(self.cargo) == 0:
            return True
