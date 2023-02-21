import random
import numpy as np


# Keeps track of all the people
# In every location of the grid
class Location:
    def __init__(self):
        self.location_list = []

    def add_pid(self, pid):
        self.location_list.append(pid)

    def get_list(self):
        return self.location_list

    def clear_location(self):
        self.location_list.clear()

    def how_big(self):
        return len(self.location_list)


# Person object
# Moves around every hour
class Person:
    id = 0

    def __init__(self):
        self.id = Person.id
        Person.id += 1
        self.currentRow = random.randint(0, 419)
        self.currentColumn = random.randint(0, 419)

    # Person randomly moves location
    # checks new location if theres someone in there
    # If so prints edgesS
    # then he places himself there in location object
    def move(self):
        self.currentRow = random.randint(0, 419)
        self.currentColumn = random.randint(0, 419)
        grid[self.currentRow][self.currentColumn].add_pid(self.id)


# Create grid
# The grid is to pinpoint where a user moves around
grid = np.empty(shape=(420, 420), dtype=object)
for x in range(0, 420):
    for y in range(0, 420):
        Loc = Location()
        grid[x][y] = Loc

# Contains all the people
dict_of_people = {}

# Creates 3000 People objects and put into dict
for x in range(0, 3000):
    p = Person()
    dict_of_people[p.id] = p
# 2000 is the previous
# 1year previous
# Put all interactions in this file
with open("edge_list_2year.txt", "w", encoding='utf-8') as edgefile:
    for x in range(0, 4000):
        # Goes through each person move him
        for person in dict_of_people:
            dict_of_people[person].move()
            list_interactions = grid[dict_of_people[person].currentRow][dict_of_people[person].currentColumn].get_list()
            if grid[dict_of_people[person].currentRow][dict_of_people[person].currentColumn].how_big() != 0:
                # Goes through the location object and gets all the people in there
                for person2 in list_interactions:
                    if person != person2:
                        # Write the interactions of two people as an edge into the file
                        edgefile.write(str(person) + " " + str(person2) + ' ' + str(x) + "\n")
        # Resets the location object for each spot on the grid for the next time interval
        for r in grid:
            for c in r:
                c.clear_location()

