import math
import os
import random

class PrayerSheet:

    def __init__(self, r_file, w_file):
        self.read_file = r_file
        self.write_file = w_file
        self.members = []
        self.numOdd = False
        self.memberHash = {}
        self.partners = {}

    # Read in members of the small group
    def read_names(self):
    
        # Check if the file is empty
        if os.stat(self.read_file).st_size == 0:
            return 1

        # Read in the names and remove any newlines
        with open(self.read_file, 'r') as fd:
            for n in fd:
                self.members.append(str.rstrip(str(n)))

        # Calculate if there is an odd number of members
        if len(self.members) % 2:
            self.numOdd = True

    # Alphabetizes the list of members
    def alphabetize_names(self, start, end):

        if start == end:
            return self.members[start]
        else:

            midpoint = math.floor((end - start) / 2)
            left = self.members[:midpoint]
            right = self.members[midpoint:]

            sorted_left = alphabetize_names(left)
            sorted_right = alphabetize_names(right)

            pass

    # Add any number of names
    def add_names(self, *args):

        # Check for duplicate names
        for arg in args:
            if arg not in self.members:
                self.members.append(arg)

    # Remove any number of names
    def remove_names(self, *args):
        
        # Check that the name exists
        for arg in args:
            if arg in self.members:
                self.members.remove(arg)

    # Randomize members
    def randomize(self):

        # Creates a hash (number -> name) of the members
        for i,n in enumerate(self.members, start=0):
            self.memberHash[i] = str(n)

        # Repeatedly generate pairings until finished
        numMembers = len(self.members)
        complete = False
        counter = 0
        while not complete:

            # Generate two random integers
            num1 = random.randint(0,numMembers-1)
            num2 = random.randint(0,numMembers-1)

            # Check if the two numbers are equal
            if num1 == num2:
                continue

            # Generate the names from the number
            name1 = self.memberHash[num1]
            name2 = self.memberHash[num2]

            # Both names are not yet used
            if (name1 not in self.partners) and (name2 not in self.partners):

                self.partners[name1] = str(name2)
                self.partners[name2] = str(name1)
                counter += 2

            # Repeatedly search for a new partner until a new one is found
            else:

                # Name 1 is already used
                if (name1 in self.partners):

                    while 1:
                        if num1 == numMembers-1:
                            num1 = 0
                        else:
                            num1 += 1

                        if num1 == num2:
                            continue

                        name1 = self.memberHash[num1]

                        if name1 not in self.partners:
                            break
                
                # Name 2 is already used
                if (name2 in self.partners):

                    while 1:
                        if num2 == numMembers-1:
                            num2 = 0
                        else:
                            num2 += 1

                        if num1 == num2:
                            continue

                        name2 = self.memberHash[num2]

                        if name2 not in self.partners:
                            break

                self.partners[name1] = str(name2)
                self.partners[name2] = str(name1)
                counter += 2

            # Check if all names are used
            if self.numOdd:
                if counter == numMembers-1:
                    complete = True
            else:
                if counter == numMembers:
                    complete = True

        # Write the partners to a csv file
        with open(self.write_file, 'w') as fd:
            for key,val in self.partners.items():
                fd.write(str(key) + "," + str(val) +'\n')

    # Clears pairings
    def clear(self):
        
        # Clear pairings from object
        self.partners.clear()
        
        # Clear pairings from file
        with open(write_file, 'r+') as fd:
            fd.truncate(0)

    # Swaps two partners
    def swap(self, name1, name2):

        # Verify that both names are in the partner dict
        if name1 not in self.partners:
            return 1

        if name2 not in self.partners:
            return 2

        # Find the partners of both members
        partner1 = self.partners[str(name1)]
        partner2 = self.partners[str(name2)]

        # Swap the members
        self.partners[str(partner1)] = name2
        self.partners[str(partner2)] = name1

        # Swap the partners
        self.partners[str(name1)] = partner2
        self.partners[str(name2)] = partner1

        # Write the partners to a csv file
        with open(self.write_file, 'w') as fd:
            for key,val in self.partners.items():
                fd.write(str(key) + "," + str(val) +'\n')