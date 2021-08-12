# this is the class that holds all the items for creating the command line interface

import Package
import Utility


# prints a greeting to the cli when the program is started
# time_space complexity of O(1)
def main_screen():
    print("""
    Welcome to the WGUPS Package system.
    Press [Q] at any input to quit the program.
    """)


# prints a line of "*" used to help separate different sections
# time_space complexity of O(1)
def divider():
    print("*" * 100)


# calls the main menu to be printed to the terminal
# gets input from the user to determine further action
# time_space complexity of O(1)
def main_menu():
    while True:
        divider()
        print("""
            1. Look-up a Package's delivery report.
            2. Run a time based report.
            3. View Total Miles driven.
            Q = Quit the program
            """)
        choice = str.lower(input("Please chose an option number from the above list: "))
        if choice == "1":
            print("\nThis will return all the delivery data on a particular Package: ")
            package_look_up()
        elif choice == "2":
            print("\nThis will return a report for all package's at a specified time.")
            time_based_report()
        elif choice == "3":
            print("\nTotal mileage traveled by all trucks, for all packages = " + str(Utility.get_total_miles()))
        elif choice == "q":
            if quit_dialog():
                quit()
        else:
            print("\n")
            divider()
            main_menu()
            break


# returns the information associated with a particular package object
# time_space complexity of O(N)
def package_look_up():
    divider()
    valid = False
    while not valid:
        package_id = input("Enter a Package ID to look up between 1-40: ")
        if package_id.isdigit():
            package_id = int(package_id)
            if package_id <= 40:
                Package.get_package_info(package for package in Package.get_all_packages() if
                                         package.package_id == package_id)
                valid = True
            else:
                print("Please enter a number between 1-40: ")
        elif str.lower(package_id) == "q":
            if quit_dialog():
                quit()
            print(str(package_id) + " is not a valid Package ID number: ")


# prompts the user any time "q" or "Q" is entered in as an input
# if the user confirms then the program will terminate
# time_space complexity of O(1)
def quit_dialog():
    done = False
    close = str.lower(input("Do you wish to exit the program? [Y]es?: "))
    if close == "y":
        print("Thank you.")
        done = True
    return done


# prompts the user for input
# takes input and uses it to search for a particular moment in time to run the report for
# time_space complexity of O(1)
def time_based_report():
    divider()
    hour = 0
    mins = 0
    am_pm = ""
    good_hour = False
    while not good_hour:
        h = input("Please enter an hour for the report (1-12): ")
        if h.isdigit():
            h = int(h)
            if h in range(0, 13):
                good_hour = True
                hour = h
            else:
                print("Please enter an Hour value between 1-12 ")
        else:
            if str.lower(h) == "q":
                if quit_dialog():
                    quit()
            print(h + " Is not a valid number")
    good_min = False
    while not good_min:
        m = input("Please enter the minutes for the search (00-60): ")
        if m.isdigit():
            m = int(m)
            if m in range(0, 61):
                good_min = True
                mins = m
            else:
                print("Please enter a Minute value between 0(00)-60 ")
        else:
            if str.lower(m) == "q":
                if quit_dialog():
                    quit()
            print(m + " Is not a valid number")
    good_am_pm = False
    while not good_am_pm:
        morn_night = (input("Please enter AM or PM: "))
        if morn_night.isalpha():
            meridians = ["am", "pm"]
            morn_night = str.lower(morn_night)
            if morn_night in meridians:
                good_am_pm = True
                am_pm = morn_night
            elif morn_night == "q":
                if quit_dialog():
                    quit()
            else:
                print(morn_night + " is not valid. Please enter either AM or PM ")
    converted = Utility.format_time_to_min(hour, mins, am_pm)
    divider()
    if converted < 480:
        print("Trucks do not leave until 8:00am")
    formated_mins = mins
    if mins < 10:
        formated_mins = ("0" + str(mins))
    print(f"Report ran for {hour}:{formated_mins} {am_pm}")
    Utility.time_report(converted)
