class Truck:

    def __init__(self, id, currentNode="4001 South 700 East"):

        self.id = id
        self.driver = False #Boolean
        self.packages = []
        self.totalPackages = 0
        self.capacity = 16
        self.milesPerHour = 18
        self.speed = self.milesPerHour / 60
        self.milesTraveled = 0
        self.totalWeight = 0
        self.priority = id
        self.returned = False
        self.routeProgress = 0
        self.distanceToNextNode = 0
        self.currentNode = currentNode
        self.nextNode = currentNode
        self.route = []

    def __str__(self):
        nextStop = ''
        if self.route == []:
            nextStop = 'Waiting at Station'
        elif self.nextNode == "4001 South 700 East":
            nextStop = 'Returning to HUB'
        elif self.returned == True:
            nextStop = 'Returned to HUB'
        else:
            nextStop = self.route[self.routeProgress + 1]
        return f"Truck{self.id}\n__________________________________\nHas Driver: {self.driver}\nMiles Traveled: {self.milesTraveled:.1f}\nNext Stop: {nextStop}, {self.distanceToNextNode:.1f} Miles\nPackages: {self.packages}\n"

    # Sets the next node from the route
    def set_next_node(self):
        #  If the truck has returned to the HUB then set the truck as returned
        if self.routeProgress == len(self.route) - 1 and self.nextNode == "4001 South 700 East":
            self.currentNode = "4001 South 700 East"
            self.returned = True
        # If the truck has visited all nodes in the route then set the next node to the HUB
        elif self.routeProgress == len(self.route) - 1 and not self.nextNode == "4001 South 700 East":
            self.nextNode = "4001 South 700 East"
            self.currentNode = self.route[self.routeProgress]
        # Get next node in the route array, set progress++
        else:
            self.currentNode = self.route[self.routeProgress]
            self.nextNode = self.route[self.routeProgress + 1]
            self.routeProgress += 1
    # Takes a package object, sets it to delivered, removes the id from the packages array in the truck
    def deliver_package(self, package):
        if package.id in self.packages:
            self.packages.remove(package.id)
            self.totalWeight -= package.weight
            package.status = "Delivered"
            print(f"Removing Package #{package.id} from truck. {len(self.packages)} left.\n")
            print(f"Packages in truck: {self.packages}\n")
        else:
            print(f"Package #{package.id} not in packages list\n")
    # Self explanatory
    def drive_forward(self):
        self.distanceToNextNode -= self.speed
        self.milesTraveled += self.speed
        
    # Self explanatory
    def load_package(self, package):
        if len(self.packages) == self.capacity:
            print(f"Truck{self.id} is full.")

        else:
            self.packages.append(package.id)
            self.totalPackages += 1
            self.totalWeight += package.weight
            

