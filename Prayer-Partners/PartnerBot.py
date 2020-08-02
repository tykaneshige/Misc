from prayersheet import *

import asyncio
import discord
import os

from discord.ext import commands

read_file = 'files/names.txt'
write_file = 'files/partners.csv'

client = discord.Client()
bot = commands.Bot(command_prefix='?')

class PartnerBot(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.ps = PrayerSheet(read_file, write_file)

        # Clear any old data
        self.ps.clear()

        # Read in the list names from the file
        self.ps.read_names()

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

    # Basic connection test
    @commands.command()
    async def ping(self, ctx):
        await ctx.send('pong!')

    # Loads the names available on the text file
    @commands.command()
    async def load(self, ctx):

        try:
            # Check if the file is empty
            if self.ps.read_names() == 1:
                await ctx.send('Name file is empty!')
                return
        
            await ctx.send('Names successfully loaded.')
        except:
            await ctx.send('Error loading names.')

    # Adds names to prayersheet object (but not from txt file)
    @commands.command()
    async def add(self, ctx, *args):

        # Check for an empty arg list
        if len(args) == 0:
            await ctx.send('Please pass 1 or more names.')
            return

        # Add names to prayersheet object
        try:
            self.ps.add_names(args)
            await ctx.send('Names successfully added.')
        except:
            await ctx.send('Error adding names.')

    # Removes names from prayersheet object (but not from txt file)
    @commands.command()
    async def remove(self, ctx, *args):

        # Check for an empty arg list
        if len(args) == 0:
            await ctx.send('Please pass 1 or more names.')
            return

        # Check for an empty name list
        if len(self.ps.members) == 0:
            await ctx.send('There are no members to remove.')
            return

        # Remove names from prayersheet object
        try:
            self.ps.remove_names(args)
            await ctx.send('Names successfully removed.')
        except:
            await ctx.send('Error removing names.')

    # List all members to be paired
    @commands.command()
    async def list(self, ctx):

        # Check if the list is empty
        if not self.ps.members:
            await ctx.send('No members exist yet!')
            return

        for name in self.ps.members:
            await ctx.send(str(name) + '\n')

    # Randomize names
    @commands.command()
    async def pair(self, ctx):
        
        # Verify that the number of members is greater than 0
        if len(self.ps.members) == 0:
            await ctx.send('There are no members to pair!')

        try:
            self.ps.randomize()
            await ctx.send('Names successfully paried.')
        except:
            await ctx.send('Error pairing names.')

    # List the pairings
    @commands.command()
    async def pairings(self, ctx, send_file=''):

        # Verify that there are pairings
        if len(self.ps.partners) == 0:
            await ctx.send('There are no pairings yet!')
            return

        # Check if the user wants the pairings in file format
        if send_file == 'file':
            try:
                await ctx.send(file=discord.File(write_file))
                return
            except:
                await ctx.send('Error sending file.')
                return

        try:
            # Write to the server
            for key in self.ps.members:
                if key not in self.ps.partners:
                    continue
                await ctx.send('{}: {}'.format(key,self.ps.partners[key]))
        except:
            await ctx.send('Error listing pairings.')

    # Clears all pairings (from both the object and file)
    @commands.command()
    async def clear(self, ctx):

        try:
            self.ps.clear()
            await ctx.send('Successfully cleared pairings.')
        except:
            await ctx.send('Error clearing pairings.')

    # Swaps two partners
    @commands.command()
    async def swap(self, ctx, *args):

        # Check if two names were passed
        if len(args) != 2:
            await ctx.send('Please pass *two* names.')
        
        n1 = args[0]
        n2 = args[1]

        # Swap the names
        try:
            result = self.ps.swap(n1,n2)

            if result == 1:
                await ctx.send('Name 1 is invalid.')
                return
            
            if result == 2:
                await ctx.send('Name 2 is invalid.')
                return

            await ctx.send('Successfully swapped \'{}\' and \'{}\'.'.format(n1,n2))
        except:
            await ctx.send('Error swapping names.')


    # Exit commands
    @commands.command()
    async def exit(self, ctx):
        await ctx.send('Shutting down.')
        await self.bot.close()

        if self.bot.is_closed():
            print('Bot succesfully shut down.')
        else:
            print('Bot did not properly shut down.')

# Main function
if __name__ == '__main__':
    bot.add_cog(PartnerBot(bot))
    bot.run('Insert Token Here')