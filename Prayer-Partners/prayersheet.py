import math
import os
import random

class PrayerSheet:

    def __init__(self, r_file, w_file):
        self.read_file = r_file
        self.write_file = w_file
        self.members = []
        self.partners = {}

    # Read in members of the small group
    def read_names(self):
    
        # Check if the file is empty
        if os.stat(self.read_file).st_size == 0:
            return 1

        # Clear the members list
        self.members.clear()

        # Read in the names and remove any newlines
        with open(self.read_file, 'r') as fd:
            for n in fd:
                self.members.append(str.rstrip(str(n)))

        # Alphabetize names
        self.alphabetize_names(self.members)

    # Alphabetizes the list of members
    def alphabetize_names(self, arr):

        if len(arr) > 1:

            midpoint = math.floor(len(arr) / 2)
            left = arr[:midpoint]
            right = arr[midpoint:]

            self.alphabetize_names(left)
            self.alphabetize_names(right)

            l = r = i = 0

            while l < len(left) and r < len(right):
                if left[l] < right[r]:
                    arr[i] = left[l]
                    l += 1
                else:
                    arr[i] = right[r]
                    r += 1
                i += 1

            while l < len(left):
                arr[i] = left[l]
                l += 1
                i += 1
            
            while r < len(right):
                arr[i] = right[r]
                r += 1
                i += 1

    # Add any number of names
    def add_names(self, names):

        # Check for duplicate names
        for name in names:
            if name not in self.members:
                self.members.append(name)
                self.partners[name] = 'None'

        # Alphabetize names
        self.alphabetize_names(self.members)

    # Remove any number of names
    def remove_names(self, names):
        
        # Check that the name exists
        for name in names:
            if name in self.members:
                self.members.remove(name)

        # Remove name in the pairings
        for key,value in self.partners.items():
            if value in names:
                self.partners[key] = 'None'

    # Randomize members
    def randomize(self):

        # Clear any pairings
        self.partners.clear()

        # Creates a hash (number -> name) of the members
        memberHash = {}
        for i,n in enumerate(self.members, start=0):
            memberHash[i] = str(n)

        # Repeatedly generate pairings until finished
        numMembers = len(self.members)

        # Calculate if there is an odd number of members
        numOdd = False
        if numMembers % 2:
            numOdd = True
        
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
            name1 = memberHash[num1]
            name2 = memberHash[num2]

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

                        name1 = memberHash[num1]

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

                        name2 = memberHash[num2]

                        if name2 not in self.partners:
                            break

                self.partners[name1] = str(name2)
                self.partners[name2] = str(name1)
                counter += 2

            # Check if all names are used
            if numOdd:
                if counter == numMembers-1:
                    complete = True

                    # Add an entry for the member with no partner
                    for key in self.members:
                        if key not in self.partners:
                            self.partners[key] = 'None'
            else:
                if counter == numMembers:
                    complete = True

        # Write the partners to a csv file
        with open(self.write_file, 'w') as fd:
            for key in self.members:
                fd.write('{},{}\n'.format(key, self.partners[key]))

    # Clears pairings
    def clear(self):
        
        # Clear pairings from object
        self.partners.clear()
        
        # Clear pairings from file
        with open(self.write_file, 'r+') as fd:
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
        self.partners[str(name1)] = partner2
        self.partners[str(name2)] = partner1
        
        # Swap the partners
        if partner1 not in self.partners:
            self.partners[str(partner2)] = name1
        elif partner2 not in self.partners:
            self.partners[str(partner1)] = name2
        else:
            self.partners[str(partner1)] = name2
            self.partners[str(partner2)] = name1

        # Write the partners to a csv file
        with open(self.write_file, 'w') as fd:
            for key in self.members:
                fd.write('{},{}\n'.format(key, self.partners[key]))