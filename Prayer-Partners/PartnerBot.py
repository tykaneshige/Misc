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

    @commands.Cog.listener()
    async def on_ready(self):
        print('Logged in as')
        print(self.bot.user.name)
        print(self.bot.user.id)
        print('------')

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
            # Check for duplicate names
            for arg in args:
                if arg not in self.ps.members:
                    self.ps.members.append(arg)

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

        # Remove names from prayersheet object
        try:
            # Check that the name exists
            for arg in args:
                if arg in self.ps.members:
                    self.ps.members.remove(arg)

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
        
        try:
            self.ps.randomize()
            await ctx.send('Names successfully paried.')
        except:
            await ctx.send('Error pairing names.')

    # List the pairings
    @commands.command()
    async def pairings(self, ctx):

        try:
            # Check if the file is empty
            if os.stat(self.ps.write_file).st_size == 0:
                await ctx.send('Partner file is empty!')
                return

            # Write the server
            with open(self.ps.write_file, 'r') as fd:
                for line in fd:
                    p1,p2 = line.split(',')
                    await ctx.send('{}: {}'.format(str(p1), str(p2)))
        except:
            await ctx.send('Error listing pairings.')

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