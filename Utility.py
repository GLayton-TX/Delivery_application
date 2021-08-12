# Class for utility methods

from typing import List
import Package
import Truck

# list containing the package objects already delivered
delivery_report = []

# the package ids of the packages sorted by route
priority = [1, 2, 4, 13, 14, 15, 16, 19, 20, 21, 29, 31]
early = [6, 25, 26, 27, 28, 30, 33, 34, 35, 37, 39, 40]
ten_twenty = [3, 5, 7, 8, 9, 10, 11, 12, 17, 18, 22, 23, 24, 32, 36, 38]

# creates the truck objects used in the program to deliver the packages
# time_space complexity of O(1)
truck1 = Truck.Truck()  # Just a truck
ali_the_best_ups_driver_truck2 = Truck.Truck()  # Used as I work in a warehouse and Ali is indeed the best UPS driver
stuart_truck3 = Truck.Truck()  # Truck 3 is not used, and Stuart is also useless
ali_the_best_ups_driver_truck2.truck_number = 2
stuart_truck3.truck_number = 3


# runs the route delivering all the packages and returning to the hub when empty
# can be used with any sorted list of packages
# time_space complexity of O(N)
def run_generic_route(truck, id_list):
    truck.start_route()
    manual_list = list(map(Package.package_list.search, id_list))
    # represents the address being fixed for package number 9 at 10:20am
    if truck.start_time == 620:
        Package.update_address(9, " 410 S State St", "Salt Lake City", "UT", "84111",
                               "Wrong address listed. CORRECTED: 10:20 am", manual_list)
    for package in manual_list:
        truck.load_package(package)
        if truck.is_full:
            break
    [manual_list.remove(loaded) for loaded in truck.cargo if loaded in manual_list]
    while not truck.truck_is_empty():
        next_delivery = Package.greedy(truck.cargo, truck.location)
        truck.drive_truck(next_delivery.package_destination_id)
        truck.deliver_package(next_delivery.package_id)
    truck.drive_truck(0)
    delivery_report.append([package for package in truck.delivered])


# returns the total miles traveled by all the trucks
# time_space complexity of O(1)
def get_total_miles():
    total_miles = truck1.odometer + ali_the_best_ups_driver_truck2.odometer + stuart_truck3.odometer
    return round(total_miles, 2)


# creates and prints a report in a more readable fashion
# time_space complexity of O(N)
def create_report(report_type):
    for package in report_type:
        p_id = package.package_id
        p_address = package.package_address
        p_deadline = package.package_deadline
        p_status = package.package_status
        p_loaded = package.package_load_time
        p_truck = ""
        p_delivered = ""
        if package.package_truck_number == 0:
            p_truck = "Not Loaded"
            p_delivered = "N/A"
            p_status = "At Hub"
        elif package.package_truck_number > 0:
            if package.package_status == "Delivered":
                p_truck = f"Delivered by Truck: " + str(package.package_truck_number)
                p_delivered = format_min_to_time(package.package_delivered_at)
            else:
                p_truck = f"Loaded on Truck: " + str(package.package_truck_number) + " at " + p_loaded
                p_delivered = "N/A"
                p_status = "En Route"
        p_notes = package.package_notes
        print(
            f"ID: {p_id} | {p_truck} | Address: {p_address} | Deadline: {p_deadline} | Status: {p_status}"
            f" | Delivered at: {p_delivered} | Notes: {p_notes}")


# gathers and correctly assigns data based on a time entered by the user
# prints a report for all packages based on this time
# time_space complexity of O(N)
def time_report(time_query):
    result = []
    delivered = []
    filtered: List[Package.Package] = []

    # used to allow the list to be sorted by package number
    # time_space complexity of O(1)
    def get_id(widget):
        return widget.package_id

    for items in Package.get_all_packages():
        if items.package_delivered_at <= time_query:
            new_package = Package.Package.copy_package(items)
            delivered.append(new_package)
        else:
            filtered.append(items)
    for item in filtered:
        if item.package_id in priority and time_query > 480:
            new_package = Package.Package.copy_package(item)
            new_package.package_status = ""
            result.append(new_package)
        elif item.package_id in early and time_query > 545:
            new_package = Package.Package.copy_package(item)
            new_package.package_status = ""
            result.append(new_package)
        elif item.package_id in ten_twenty and time_query > 620:
            new_package = Package.Package.copy_package(item)
            new_package.package_status = ""
            result.append(new_package)
        else:
            new_package = Package.Package.copy_package(item)
            new_package.package_truck_number = 0
            result.append(new_package)
            if item.package_id == 9:
                Package.update_address(9, " 300 State St", "Salt Lake City", "UT", "84103",
                                       "Wrong address listed", result)
    for final in delivered:
        result.append(final)
    result.sort(key=get_id)
    create_report(result)


# used to take a min of the day value used by the program and create a human readable string
# time_space complexity of O(1)
def format_min_to_time(time_in_min):
    hour = int(time_in_min / 60)
    minutes = int(time_in_min % 60)
    am_pm = "am"
    if hour >= 12:
        am_pm = "pm"
    add_tens = False
    if minutes < 10:
        add_tens = True
    if add_tens:
        converted = f"{hour}:0{minutes} {am_pm}"
    else:
        converted = f"{hour}:{minutes} {am_pm}"
    return converted


# used to take a standard time as written and turn it into a min of the day value to be used by the program
# time_space complexity of O(1)
def format_time_to_min(hour, mins, am_pm):
    converted = 0.0
    if am_pm == "pm":
        converted = ((hour + 12) * 60)
    elif am_pm == "am":
        converted = (hour * 60)
    time_in_min = converted + mins
    return time_in_min


# sets the start time for each run based on factors such as start time and package availability
# loads all trucks with packages from the sorted routes
# using the greedy algorithim each trucks route is dynamicly updated for the next closest destination they have a package for
# delivers each package and updates the delivery list
# time_space complexity of O(N)
def run_all_routes():
    ali_the_best_ups_driver_truck2.start_time = 480
    run_generic_route(ali_the_best_ups_driver_truck2, priority)
    truck1.start_time = 545
    run_generic_route(truck1, early)
    ali_the_best_ups_driver_truck2.start_time = 620
    run_generic_route(ali_the_best_ups_driver_truck2, ten_twenty)
