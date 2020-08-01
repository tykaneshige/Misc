import os
import random

class PrayerSheet:

    def __init__(self, r_file, w_file):
        self.read_file = r_file
        self.write_file = w_file
        self.members = []
        self.numMembers = 0
        self.numOdd = False
        self.memberHash = {}
        self.partners = {}

    # Read in members of the small group
    def read_names(self):
    
        # Check if the file is empty
        if os.stat(self.read_file).st_size == 0:
            return 1

        # Read in the names and remove any newlines
        # Get a total number of members
        with open(self.read_file, 'r') as fd:
            for n in fd:
                self.members.append(str.rstrip(str(n)))
                self.numMembers += 1

        # Calculate if there is an odd number of members
        if self.numMembers % 2:
            self.numOdd = True

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
        complete = False
        counter = 0
        while not complete:

            # Generate two random integers
            num1 = random.randint(0,self.numMembers-1)
            num2 = random.randint(0,self.numMembers-1)

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
                        if num1 == self.numMembers-1:
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
                        if num2 == self.numMembers-1:
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
                if counter == self.numMembers-1:
                    complete = True
            else:
                if counter == self.numMembers:
                    complete = True

        # Write the partners to a csv file
        with open(self.write_file, 'w') as fd:
            for key,val in self.partners.items():
                fd.write(str(key) + "," + str(val) +'\n')