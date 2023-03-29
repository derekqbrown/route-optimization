# Organizes the packages into trucks and finds the shortest paths   space-complexity = O(n)
import datetime
import csv_reader

# list to store packages that must go on a specific truck
trucks = [[], [], []]
# list to store actual delivery order for each truck
delivery = [[], [], []]
# list to store the distances between each package and previous package (based on delivery list)
times_list = [[], [], []]

# These lists store packages with special notes or delivery times
deliver_with = []
early_delivery = []
end_day_delivery = []
delayed_pkgs = []

# These variables refer to csv_reader (used for convenience and readability)
num_packages = len(csv_reader.package_list)
p_list = csv_reader.package_list
pkg_address = csv_reader.packages_address
dist_list = csv_reader.dist_list

# This stores the index for each package available
available_packages = []
total_distance = 0


# This function loads the packages into the truck   time-complexity = O(n^2)
def prepare_packages():
    i = 1
    packages_at_hub = p_list.copy()
    while len(packages_at_hub) > 0:
        note = csv_reader.packages_hash.find(i)[1][7]
        package = csv_reader.packages_hash.find(i)
        # Parse through the notes, assign the packages to trucks if needed
        parse_notes(note, package, packages_at_hub)
        i += 1

    # This loop handles assignment of deliver_with packages
    for pkg in deliver_with:
        if pkg in end_day_delivery:
            end_day_delivery.remove(pkg)
        if pkg in early_delivery:
            early_delivery.remove(pkg)
        j = 0
        # While loop to check each truck for the deliver_with packages and assign accordingly
        while j < len(trucks):
            if pkg in trucks[j]:
                for package in deliver_with:
                    if package not in trucks[j]:
                        trucks[j].append(package)
            j += 1
    for package in trucks[0] + early_delivery + end_day_delivery:
        available_packages.append(package - 1)
        if csv_reader.packages_hash.find(package)[1][5] == "9:00 AM":
            delivery[0].append(package - 1)

    load_packages()
    get_distances()
    set_times()


# This finds the shortest route using nearest neighbor algorithm   time-complexity = O(n)
def load_packages():
    global available_packages
    # add all packages that are initially available
    if len(delivery[0]) != 0:
        start = delivery[0][-1]
    else:
        start = get_nearest(0)
        delivery[0].append(start)
    available_packages.remove(start)
    # Load truck 1
    while len(delivery[0]) < 16 and len(available_packages) > 0:

        nearest = get_nearest(start)

        delivery[0].append(nearest)
        available_packages.remove(nearest)
        start = int(delivery[0][len(delivery[0]) - 1])

    # add in the delayed packages and packages reserved for truck 2
    for package in trucks[1] + delayed_pkgs:
        available_packages.append(package - 1)

    start = get_nearest(0)

    delivery[1].append(start)
    available_packages.remove(start)

    # Load truck 2
    while len(delivery[1]) < 16 and len(available_packages) > 0:

        nearest = get_nearest(start)
        delivery[1].append(nearest)
        available_packages.remove(nearest)
        start = int(delivery[1][-1])

    # Add in packages reserved for last truck
    for package in trucks[2]:
        available_packages.append(package - 1)
    start = get_nearest(0)
    delivery[2].append(start)
    available_packages.remove(start)
    # Update the package with the wrong address
    address_fix = csv_reader.packages_hash.find(9)
    address_fix[1][1] = "410 S State St"
    address_fix[1][2] = "Salt Lake City"
    address_fix[1][3] = "UT"
    address_fix[1][4] = "84111"
    pkg_address[8] = 19

    # Load truck 3
    while len(delivery[2]) < 16 and len(available_packages) > 0:
        nearest = get_nearest(start)
        delivery[2].append(nearest)
        available_packages.remove(nearest)
        start = int(delivery[2][-1])


# This finds the nearest next package   time-complexity = O(n)
def get_nearest(start):
    closest_index = 54
    selected = -1

    close_ind_list = [-1, -1, -1]
    distances = [50, 50, 50]

    # This for loop determines the nearest packages (with priority to deadlines)
    for package in available_packages:
        if start != package:
            distance = dist_list[pkg_address[start]][pkg_address[package]]
            if distance == 0.0:
                return package
            elif distance <= closest_index:
                closest_index = distance
                selected = package
            # This gives some preference to prioritized packages over time
            if package + 1 in early_delivery + trucks[0] + trucks[1] + trucks[2]:
                distance -= 2
                if 16 - len(trucks[0]) < len(delivery[0]) > 6 and len(delivery[0]) != 16:
                    if len(delivery[0]) % 3 == 1:
                        return package
                if 16 - len(trucks[1]) < len(delivery[1]) > 3 and len(delivery[1]) != 16:
                    if len(delivery[1]) % 3 == 1:
                        return package
            # this tracks the nearest three packages for prioritization
            if distance < distances[0]:
                close_ind_list[2] = close_ind_list[1]
                distances[2] = distances[1]
                close_ind_list[1] = close_ind_list[0]
                distances[1] = distances[0]
                close_ind_list[0] = package
                distances[0] = distance
            elif distance < distances[1]:
                close_ind_list[2] = close_ind_list[1]
                distances[2] = distances[1]
                close_ind_list[1] = package
                distances[1] = distance
            elif distance < distances[2]:
                close_ind_list[2] = package
                distances[2] = distance

    # This loop gives priority to packages with early deadlines or special instructions
    for i in range(3):
        if close_ind_list[i] + 1 in early_delivery + trucks[0] + trucks[1] + trucks[2]:
            return close_ind_list[i]

    return selected


# Calculates the total distance and stores individual distances in a list   time-complexity = O(n)
def get_distances():
    global total_distance
    for i in range(3):
        index = 0
        for pkg in range(len(delivery[i])):
            pkg_id = delivery[i][pkg]
            next_pkg = dist_list[index][pkg_address[pkg_id]]
            times_list[i].append(next_pkg)
            total_distance += times_list[i][pkg]
            index = pkg_address[delivery[i][pkg]]


# This converts the times for each package from distance to time   time-complexity = O(n)
def set_times():
    for i in range(3):
        add_time = 0
        for k in range(len(delivery[i])):
            # convert here then append
            time_stamp = datetime.datetime(100, 1, 1, 8, 0, 0)
            if i == 1:
                time_stamp = datetime.datetime(100, 1, 1, 9, 5, 0)
            if i == 2:
                time_stamp = datetime.datetime(100, 1, 1, 10, 30, 0)
            csv_reader.packages_hash.find(delivery[i][k] + 1).append(time_stamp.time())

            add_time += times_list[i][k] * 200
            time_stamp = time_stamp + datetime.timedelta(seconds=add_time)
            csv_reader.packages_hash.find(delivery[i][k] + 1).append(time_stamp.time())


# Prints the status of all packages at a given time --- time-complexity = O(n)
def check_all_status(time):

    cur_distance = 0

    try:
        check_time = datetime.datetime.strptime(time, '%H:%M:%S')
    except:
        print("Time must be in HH:MM:SS format")
        print("Input: " + time)
        return
    print("--Status of all packages at " + str(time) + "--\n")

    for package in p_list:

        pkg = csv_reader.packages_hash.find(int(package))
        pkg_id = pkg[0]
        hub_time = pkg[2]
        deliver_time = pkg[3]
        address = pkg[1][1] + ", " + pkg[1][2] + ", " + pkg[1][3] + ", " + pkg[1][4]
        if "Wrong" in pkg[1][7] and check_time.time() < hub_time:
            address = "300 State St, Salt Lake City, UT, 84103"

        pkg_string = "Package ID: " + pkg[1][0] + " | Address: " \
                     + address + \
                     "\nDeadline: " + pkg[1][5] + " | Weight: " + pkg[1][6]
        if pkg[1][7] != "":
            print(pkg_string + " | Special Note: " + pkg[1][7])
        else:
            print(pkg_string + " | Special Note: N/A")

        if check_time.time() < hub_time:
            if "Delayed" in pkg[1][7]:
                print("Package " + str(pkg_id) + ": Has not arrived at HUB")
            else:
                print("Status: At HUB")
        elif check_time.time() < deliver_time:
            print("Status: Departed HUB at: " + str(hub_time) + " - En route")
        else:
            print("Status: Departed HUB at: " + str(hub_time) + " - Delivered at " + str(deliver_time))
            for i in range(3):
                if pkg_id - 1 in delivery[i]:
                    cur_distance += times_list[i][delivery[i].index(pkg_id - 1)]
        print("-------------")
    print("-------------\nTotal distance travelled at " + str(time) + " is " + "{:.2f}".format(cur_distance) + " miles")


# Returns information for a specific package | time-complexity = O(1)
def check_package_status(package):
    if str(package).isnumeric() and int(package) <= num_packages:
        pkg = csv_reader.packages_hash.find(int(package))
        hub_time = pkg[2]
        deliver_time = pkg[3]
        pkg_string = "Package ID: " + pkg[1][0] + " | Address: " \
                     + pkg[1][1] + ", " + pkg[1][2] + ", " + pkg[1][3] + ", " + pkg[1][4] + \
                     "\nDeadline: " + pkg[1][5] + " | Weight: " + pkg[1][6]
        if pkg[1][7] != "":
            print(pkg_string + " | Special Note: " + pkg[1][7])
        else:
            print(pkg_string + " | Special Note: N/A")
        print("Departs HUB at: " + str(hub_time) + " | Delivery at: " + str(deliver_time))
    else:
        print("Input Error - Please try again")


# This will check a specific package at a given time | time-complexity = O(n)
def check_package_time(package_time):
    pkg_time = package_time.split(",")
    pkg_id = "PACKAGE ID"
    time = "TIME"
    # Parse the input to and sort by time and package
    for part in pkg_time:
        if ":" in part:
            time = part.strip()
        else:
            pkg_id = part.strip()
    if not str(pkg_id).isnumeric():
        print("Input Error - Please try again")
        return
    if ":" not in time:
        print("Input Error - Please try again")
        return

    hub_time = csv_reader.packages_hash.find(int(pkg_id))[2]
    deliver_time = csv_reader.packages_hash.find(int(pkg_id))[3]
    try:
        check_time = datetime.datetime.strptime(time, '%H:%M:%S')
    except:
        print("Time must be in HH:MM:SS format")
        print("Input: " + time)
        return
    print("Status of Package " + pkg_id + " at " + time + ":")
    if check_time.time() < hub_time:
        if "Delayed" in csv_reader.packages_hash.find(pkg_id)[1][7]:
            print("Has not arrived at HUB")
        else:
            print("At HUB")
    elif check_time.time() < deliver_time:
        print("En route")
    else:
        print("Delivered at: " + str(deliver_time))


# Checks the input to decide which function to call | time-complexity = O(1)
def check_switch(usr_input):
    if "," in str(usr_input):
        check_package_time(usr_input)
    elif ":" in str(usr_input):
        check_all_status(usr_input)
    else:
        check_package_status(usr_input)


# This function parses the notes and loads trucks accordingly | time-complexity = O(n)
def parse_notes(note, package, packages_at_hub):

    # If it must be on truck 2, load onto truck 2
    if "truck 2" in note:
        trucks[1].append(package[0])
    # If the address is wrong, load onto third truck
    if "Wrong address" in note:
        if package[1][5] == "EOD":
            trucks[2].append(package[0])
        else:
            early_delivery.append(package[0])
    # If the package is delayed and has an early delivery deadline, load into truck 2
    if "Delayed" in note:
        if package[1][5] == "10:30 AM":
            trucks[1].append(package[0])
        else:
            delayed_pkgs.append(package[0])
    # This creates a list of packages that must be delivered together
    if "delivered with" in note:
        index = note.find("with") + 4
        with_list = note[index:].split(",")
        # Parse the substring and separate values for packages to be delivered with
        for w in with_list:
            if w[0] == " ":
                w.replace(" ", "")
            w_int = int(w)
            pkg = csv_reader.packages_hash.find(w_int)
            # Check if the package is at the hub, remove from hub list if so
            if w_int in packages_at_hub:
                deliver_with.append(pkg[0])
                packages_at_hub.remove(w_int)
            elif w_int in early_delivery + end_day_delivery and w_int not in deliver_with:
                deliver_with.append(pkg[0])
        deliver_with.append(package[0])
    # if the packages are not already assigned a truck, sort by deliver schedule
    if package[0] not in trucks[0] + trucks[1] + trucks[2]:
        match package[1][5]:
            case "9:00 AM":
                trucks[0].append(package[0])
            case "10:30 AM":
                early_delivery.append(package[0])
            case _:
                if package[0] not in delayed_pkgs:
                    end_day_delivery.append(package[0])
    # This removes the package from the hub list
    if package[0] in packages_at_hub:
        packages_at_hub.remove(package[0])
