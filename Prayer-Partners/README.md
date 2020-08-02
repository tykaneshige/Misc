# Prayer Partners

A simple program used to create prayer partners from a list of names.

Created By: 
*Thomas Kaneshige (tykaneshige.work@gmail.com)*

---

## Description

* PartnerBot is a simple bot that takes in a list of names and pairs them up.
  * Upon startup, the bot will upload a set of names from a txt file.
  * The bot will randomly pair names until finished, even if there are an odd number of names.

* This bot comes with two files by default.
  * 'names.txt': This file contains a list of names. 
    * These names will be read in initially when starting up the bot.
  * 'partners.csv': This file will contain the pairs after '?pair' is called.

---

## Instructions

* Requirements
  * You must be using Python 3.5 or later.

1. Start by cloning the the repository using 'git clone'.
2. After cloning the repository, go to the Discord Developer site.
   1. This can be accessed by searching up 'Discord SDK' on Google.
3. After logging in, click on 'Applications' > 'New Application'.
   1. You may need to authrorize 2-Factor Authentication.
4. Give the bot a name, picture, and description (last two are optional).
5. After finishing the initial setup, create a new bot by going to 'Bot' > 'Add Bot'.
6. After creating a new bot, go to 'OAuth2' and fill out the following fields.
   1. In 'Scopes', identify this bot as a 'Bot'.
   2. In 'Bot Permissions', authorize (at least) 'Send Messages', 'Attach Files', and 'Read Message History'. This can be changed later.
7. A link should be generated in the center of the page. Follow the link to an authorization page.
8. Add the bot to your server of choice. You must have admin-level permissions to do this.
9. After adding the bot to your server, go back to the Discord Developer site.
10. Go back to the bot you created, and click on 'Bot'.
11. Scroll down to find the bot's token (which should be hidden).
12. Copy the token and insert it in PartnerBot.py where it says, "Insert Token Here".
13. Start the bot by running the command 'python3 PartnerBot.py' (python3 is necessary).
14. The command line should state that the bot is logged in. Verify by texting '?ping' in your server.
15. If the bot responds with 'pong!', then it is ready to be used!

---

## Documentation

* Commands
  * All commands with begin with the prefix '?'.

```
-?ping: Simple command to test that for a working connection with the bot. 
        The bot should respond with "pong!".

-?load: This command reloads all the names from files/names.txt.

-?add <name1> <name2> ... : Adds a name to the member list.

-?remove <name1> <name2> ... : Removes a name from the member list.

-?list: Prints the member list.

-?pair: Randomly pairs the names.

-?pairings <file=optional>: Prints the list of pairs.
  -If passed with the argument 'file', PartnerBot will send the pairings as a csv file instead.

-?clear: Clears the pairings file.

-?swap <name1> <name2>: Swaps two members and their partners.

-?exit: Disconnects the bot.
```
