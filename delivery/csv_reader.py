# Imports data from the resource files into usable formats    space-complexity = O(n)
import csv
import os
from hash import HashMap

delivery_dir = os.path.dirname(__file__)

packages_hash = HashMap()
distances_hash = HashMap()
# This holds a matrix containing the distances between locations
dist_list = []
# This holds the indexes for the package addresses
packages_address = []

# Opens the Package file to insert packages into hash map   time-complexity = O(n)
with open(delivery_dir + '/resources/WGUPS Package File.csv') as packages:
    package_info = csv.reader(packages, delimiter=',')
    package_list = []
    # For loop to store the packages in a hash map
    for row in package_info:
        # Add the packages to the map - this will add the id as the first entry, package info as
        packages_hash.insert(int(row[0]), row)
        package_list.append(int(row[0]))
# Opens the distance table to create a graph   time-complexity = O(n)
with open(delivery_dir + '/resources/WGUPS Distance Table.csv') as distances:
    distance_info = csv.reader(distances, delimiter=',')

    i = 0
    # For loop to store the distances in a hash map
    for row in distance_info:
        distances_hash.insert(i, row[0])
        dist_list.append(row[1:])
        i += 1

    row = 0
    # This while loop flips the values across the diagonal to make it easier to lookup when finding the shortest path
    while row < len(dist_list[0]):
        column = 0
        while column < len(dist_list[0]):

            if dist_list[row][column] == '':
                dist_list[row][column] = dist_list[column][row]

            if not dist_list[row][column].isalpha():
                dist_list[row][column] = float(dist_list[row][column])

            column += 1
        row += 1
# This loop will populate the packages_address list (used for distance lookups)  time-complexity = O(n)
for num in package_list:
    i = 0
    while i < len(dist_list):
        if packages_hash.find(num)[1][1] in distances_hash.find(i)[1]:
            packages_address.append(i)
        i += 1
