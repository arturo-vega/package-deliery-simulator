'''
Arturo Vega
011023005
'''


import csv
import msvcrt
import time
from scripts.graph import Graph
from scripts.package import Package
from scripts.truck import Truck
from scripts.clock import Clock
from scripts.hashtable import HashTable

'''
Package Statuses:
Home
Outbound
Delivered
'''
# Gets the packages from the package file and returns an array of Package objects
def process_csv(fileName):
    packages = []
    with open(fileName, 'r') as csvFile:
        reader = csv.reader(csvFile, delimiter=',')
        next(reader) #skip header
        for row in reader:
            id, address, city, state, zipcode, deadline, weight, special_notes = row
            packages.append(Package(int(id), address, city, state, zipcode, deadline, int(weight), special_notes))
    return packages

# Handles time, simulation speed, and checks for if a package is delayed and when important times have occured
def update_time(simulationClock, packageList, simulationSpeed):
    time.sleep(.5 / simulationSpeed)

    simulationClock.advance_time()

    if simulationClock.ticks > 545:
        simulationClock.nineOFive = True
    if simulationClock.ticks > 620:
        simulationClock.tenTwenty = True

    for package in packageList:
        if package.get_deadline_in_ticks() < simulationClock.ticks and package.missedDelivery == False and package.status != "Delivered":
            print(f"Package {package.id} has missed it's deadline {package.deadline}")
            package.missedDelivery = True

# Logic for creating the path when a truck leaves the HUB, sets packages in the truck to 'Outbound'
def truck_departs(truck, my_graph, packageList):
    nodeList = []
    for package in truck.packages:
        #package needs to be subtracted by 1 to match up with the packageList "package-1"
        nodeList.append(packageList[package - 1].address)
        packageList[package - 1].status = 'Outbound'
    truck.route = my_graph.shortest_path("4001 South 700 East", nodeList)
    truck.set_next_node()
    truck.distanceToNextNode = my_graph.get_edge_weight(my_graph.get_node(truck.currentNode), my_graph.get_node(truck.nextNode))
    truck.driver = True

# Subtracks the distance to next node by the speed of the truck, checks if the truck has
# arrived at the next node and if it has print out information of the truck and set the next node
def trucks_move(trucks, simulationClock, packageList, my_graph):
    for truck in trucks:
        if truck.driver == True:
            truck.drive_forward()

            if truck.distanceToNextNode <= 0:
                print("_______________________________________")
                print(f"Current Time is: {simulationClock.get_formatted_time()}\n")
                print(f"Truck{truck.id} Arrived at {truck.nextNode}")
                print(f"Miles driven: {truck.milesTraveled:.1f}")
                print(f"Weight in truck: {truck.totalWeight}")
                print(f"Packages in Truck{truck.id}: {len(truck.packages)}")

                for package in packageList:
                    if package.address == truck.nextNode and package.id in truck.packages:
                        truck.deliver_package(package)
                        package.status = "Delivered"
                        package.deliverTime = simulationClock.get_formatted_time()

                truck.set_next_node()
                truck.distanceToNextNode = my_graph.get_edge_weight(my_graph.get_node(truck.currentNode), my_graph.get_node(truck.nextNode))

# Prints out information, use three different arrays for the package status so the program
# only has to go through the list once instead of three times
def print_packages_status(packageList):
    outbound = []
    delivered = []
    home = []

    for package in packageList:
        if package.status == "Outbound":
            outbound.append(package)
        if package.status == "Delivered":
            delivered.append(package)
        if package.status == "Home":
            home.append(package)

    print("\nPackages at HUB")
    print("_______________________________________________________________________________________________________________________\n")
    for package in home:
        print(package)

    print("\nOutbound Packages")
    print("_______________________________________________________________________________________________________________________\n")
    for package in outbound:
        print(package)

    print("\nDelivered Packages")
    print("_______________________________________________________________________________________________________________________\n")
    for package in delivered:
        print(package)

# Prints out all packages but organized by what truck they are on, uses the package hashmap
def print_package_status_for_truck(packageHash, trucks):
    for truck in trucks:
        if truck.route == []:
            print(f"Truck {truck.id} - Waiting at Station\n_________________________________________________\n")
        elif truck.returned == True:
            print(f"Truck {truck.id} - Returned to HUB\n_________________________________________________\n")
        elif truck.nextNode == "4001 South 700 East":
            print(f"Truck {truck.id} - Returning to HUB\n_________________________________________________\n")
        else:
            print(f"Truck {truck.id} - Next Stop: {truck.route[truck.routeProgress + 1]}\n_________________________________________________\n")
        for package in truck.packages:
            print(packageHash.get(package))

# Prints out information when needed, saves redundant reptition by putting it here
def print_pause_message(simulationClock):
    print("_______________________________________")
    print(f"Current Time: {simulationClock.get_formatted_time()}\n")
    print("Simulation Paused...")
    print("Enter a number (1-40) to see details of a specific package.")
    print("Enter 'a' to see all package information.")
    print("Enter 'd' to see all packages by truck.")
    print("Enter 't' to see all truck information.")
    print("Enter 'x' to unpause.")

# Assigns when a truck should leave the station based on certain criteria
def assign_truck_priority(truck, package):
    delayed = "Delayed on flight---will not arrive to depot until 9:05 am"
    if package.deadline != 'EOD' and package.special_notes != delayed and truck.priority > 1:
        truck.priority -= 3
    if package.deadline != 'EOD' and package.special_notes == delayed and truck.priority > 2:
        truck.priority -= 2
    if package.special_notes == "Wrong address listed" and truck.priority > 3:
        truck.priority -= 1

# Logic for when the simulation has finished, only when all packages have the
# 'delivered' status and all trucks don't have drivers (when they return to HUB)
def check_all_packages(packageList, trucks):
    allPackagesDelivered = True
    for package in packageList:
        if package.status != "Delivered":
            allPackagesDelivered = False

    for truck in trucks:
        if truck.returned == False:
            allPackagesDelivered = False

    return allPackagesDelivered

# If a truck has returned to HUB free the driver to get in another truck, set the
# returning truck to not have a driver
def check_for_free_driver(trucks, freeDrivers):
    for truck in trucks:
        if truck.returned == True and truck.driver == True:
            print(f"Truck{truck.id} has returned to HUB")
            freeDrivers += 1
            print(f"Free drivers = {freeDrivers}")
            truck.driver = False
    return freeDrivers

def main():
    # Setting variables for the start of the program, getting information from csv files
    #_______________________________________________________________________________________________
    simulationClock = Clock()
    # Package list contains all the Package objects
    packageList = process_csv("data/PackageFile.csv")

    packageHash = HashTable(10)
    for package in packageList:
        packageHash.insert(package.id, package)


    my_graph = Graph()
    my_graph.import_nodes("data/nodetable.csv")
    my_graph.import_edges("data/distancetable.csv")

    truck1 = Truck(1, my_graph.get_node("4001 South 700 East"))
    truck2 = Truck(2, my_graph.get_node("4001 South 700 East"))
    truck3 = Truck(3, my_graph.get_node("4001 South 700 East"))
    trucks = [truck1, truck2, truck3]

    freeDrivers = 2
    allPackagesDelivered = False

    # Trucks only get the package ID not the package object
    for package in packageList:
        loadedPackages = []

        if package.id == 1 or package.id == 13 or package.id == 14 or package.id == 15 or package.id == 16 or package.id == 19 or package.id == 20 or package.id == 29 or package.id == 30 or package.id == 31 or package.id == 34 or package.id == 37 or package.id == 40:
            truck1.load_package(package)
            loadedPackages.append(package)

        if package.id == 3 or package.id == 6 or package.id == 12 or package.id == 17 or package.id == 18 or package.id == 21 or package.id == 22 or package.id == 23 or package.id == 24 or package.id == 26 or package.id == 27 or package.id == 35 or package.id == 36 or package.id == 38 or package.id == 39:
            truck2.load_package(package)
            loadedPackages.append(package)

        if package not in loadedPackages:
            truck3.load_package(package)
            loadedPackages.append(package)

    print("WGU Package Delivery Simulator\n")
    print("Press SPACE to pause simulation and check truck or package statuses\n")
    while True:
        try:
            simulationSpeed = int(input("Enter ticks persecond (simulation speed): "))
            break
        except ValueError:
            print("Enter an integer.")
    # ______________________________________________________________________________________________

    # Main loop
    while allPackagesDelivered == False:

        freeDrivers = check_for_free_driver(trucks, freeDrivers)

        if simulationClock.tenTwenty == True and truck3.returned == False and truck3.driver == False:
            packageList[8].address = "410 S State St"
            packageList[8].city = "Salt Lake City"
            packageList[8].state = "UT"
            packageList[8].zipcode = "84111"
            print("_______________________________________")
            print(f"Current Time: {simulationClock.get_formatted_time()}")
            print(f"Package {packageList[8].id} updated, new address:\n{packageList[8].address} {packageList[8].city}, {packageList[8].state} ({packageList[8].zipcode})\n")

        for truck in trucks:
            if freeDrivers > 0:
                if truck.priority == 1 and truck.driver == False and truck.returned == False:
                    truck_departs(truck, my_graph, packageList)
                    freeDrivers -= 1
                    print("_______________________________________")
                    print(f"Current Time: {simulationClock.get_formatted_time()}")
                    print(f"Truck{truck.id} depearting from HUB\n")
                if truck.priority == 2 and truck.returned == False and simulationClock.nineOFive == True and truck.driver == False:
                    truck_departs(truck, my_graph, packageList)
                    freeDrivers -= 1
                    print("_______________________________________")
                    print(f"Current Time: {simulationClock.get_formatted_time()}")
                    print(f"Truck{truck.id} depearting from HUB\n")
                if truck.priority == 3 and truck.returned == False and simulationClock.tenTwenty == True and truck.driver == False:
                    truck_departs(truck, my_graph, packageList)
                    freeDrivers -= 1
                    print("_______________________________________")
                    print(f"Current Time: {simulationClock.get_formatted_time()}")
                    print(f"Truck{truck.id} depearting from HUB\n")
        
        trucks_move(trucks, simulationClock, packageList, my_graph)

        allPackagesDelivered = check_all_packages(packageList, trucks)

        update_time(simulationClock, packageList, simulationSpeed)

        # Handles input from the user
        if msvcrt.kbhit():
            key = msvcrt.getch()
            if key == b" ":
                print_pause_message(simulationClock)

                while True:
                    inputKey = input("...")

                    if inputKey.isnumeric():
                        packageNum = int(inputKey)
                        print(packageHash.get(packageNum))
                        print_pause_message(simulationClock)

                    elif inputKey.lower() == 'a':
                        print_packages_status(packageList)
                        print_pause_message(simulationClock)

                    elif inputKey.lower() == 'd':
                        print_package_status_for_truck(packageHash, trucks)
                        print_pause_message(simulationClock)

                    elif inputKey.lower() == 't':
                        for truck in trucks:
                            print(truck)
                        print_pause_message(simulationClock)

                    elif inputKey.lower() == "x":
                        break

                    else:
                        continue
    
    print("_______________________________________")
    print("\n")
    print("All packages delivered, all trucks returned to HUB.")
    print(f"Total miles driven: {truck1.milesTraveled + truck2.milesTraveled + truck3.milesTraveled:.1f}\n")


if __name__ == "__main__":
    main()

