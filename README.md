# EctoresBot
Hi, this is my first Discord bot project. In Summary, the bot has 3 funtionalities (but 2 are very similars) where: 

1. With a command, the bot text "bad jokes".
2. When 2 specific users connect at the same time in a voice channel, the bot enter and reproduce a mp3 file (User1 and User2 -> Sound1)
3. When 1 specific user connects a voice channel, the bot enter and reproduce a mp3 file (User3 or User4 -> Sound2)

# Before use the bot:

Create a ".env" file with the following variables:

+ DISCORD_TOKEN=
+ DISCORD_USER1=
+ DISCORD_USER2=
+ DISCORD_USER3=
+ DISCORD_USER4=
+ DISCORD_COMMAND=

- DISCORD_TOKEN is the bot token. See https://discord.com/developers/applications for more information
- DISCORD_COMMAND is a custom command you can choose :D. It can be "/eb" like EctoresBot :D
- DISCORD_USER is a UserID for each user. Activate the Developer Mode in Discord for see de ID (is a number with 18 digits)

Also, you will need a "jokes.txt" where are all the jokes you want the bot write like 1 joke per line.

And Finally, move your mp3 files at the mp3 folder and it's done (there is a default.mp3 and it will play when someone wanna play a mp3 but it doesn't exist)

# It's done, use the EctoresBot :D
