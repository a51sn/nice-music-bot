# nice-music-bot
Discord bot that collects all the song links sent in a channel and adds them to a Spotify playlist.


## Commands
It responds to 7 commands (all using the prefix "!nm"):
- **cleanup**    - Deletes all bot-related messages in channel (commands sent by users, messages sent by the bot).
- **collect**    - Adds all Spotify links in a channel to a playlist, reacts to messages with ✅  if it was successfully added.
- **help**       - Lists all the commands with brief descriptions.
- **link**       - Sends a link to the playlist in the channel.
- **ping**       - Checks if bot is online.
- **uncheck**    - Removes all ✅  reactions in this channel.
- **uncheckred** - Removes all red box reactions in this channel.

## Setup
To use this bot on your own server / with your own playlists, you'll need to register an application with both [Discord](https://discord.com/developers/) and [Spotify](https://developer.spotify.com/dashboard/), and create a file named `.env` in the nice-music-bot directory that specifies the value of the following: 
- `DISCORD_TOKEN` - found in Bot settings in the Discord Developer Portal
- `CLIENT_ID` - in the Spotify for Developers > Dashboard > your application settings
- `CLIENT_SECRET` - also in Spotify for Developers > Dashboard > your application settings
- `USER` - your Spotify username
- `PLAYLIST` - the Spotify URI of the playlist you want to collect songs in (must be a playlist that you own)

To add the bot to your server, go to Discord Developer Portal > OAuth2 > URL Generator, and under Scopes, check `bot` and under Bot Permissions, check `Read Messages`, `Send Messages`, `Manage Messages`, `Read Message History`, and `Add Reactions`, and send the URL to someone with administrator access to your server. 

Then, run `bot.py`. You should see the message "Bot connected as {username of your bot}". Your bot will be online as long as this program continues running!

## Hosting! 
I finally figured out how to make the bot available even when my laptop is not on to run the program! Here's how I did it.

I set up an e2 micro VPS on Google Cloud Compute Engine (I chose this because it's within GCP's "always-free" tier! Alternatively, you could use other VPS providers like AWS, Azure, Digital Ocean,  etc). This allowed me to ssh into a VM where I cloned this repo, installed all the dependencies, and then looked for a way to keep bot.py running even after I logged out. I explored 3 different approaches before I found what worked best for me.

### **1. running bot.py within a separate tmux session**
[tmux](https://linuxize.com/post/getting-started-with-tmux/) stands for "terminal multiplexer", which is basically a tool that lets you create and access multiple, persistent terminal sessions from one screen. Instead of just running the python program and not being able to interact with the shell or close the terminal without interrupting the program, tmux allows me to run the program from a separate terminal session and then "detach" from it, freeing up my terminal while letting bot.py continue to run in the background.

I installed tmux with `sudo apt install tmux`. Then, I created a new session with `tmux a`, navigated to the repo folder, and ran `python3 bot.py`. Once I saw the confirmation message "Bot connected as {bot-username}", I detached with `Ctrl-b d` and then closed the window. Lastly, I checked to see if my bot was still online by pinging it from a Discord server I had added to, and it worked! 

This approach was great for keeping my bot online 24/7. However, within a week I ran into an issue when my [Spotify access tokens](https://developer.spotify.com/documentation/general/guides/authorization/code-flow/) expired and I could no longer collect any songs. The easiest way to get around the issue seemed to be just logging on and restarting the program, but I didn't want to go through the hassle of manually restarting the program every time the bot stopped working. 

I started looking for a way to stop and start the program at regular intervals and learned about [cron jobs](https://www.hivelocity.net/kb/what-is-cron-job/). I think this is definitely possible to automate using tmux and cron, and I did come across some [promising ways forward on StackExchange](https://superuser.com/questions/492266/run-or-send-a-command-to-a-tmux-pane-in-a-running-tmux-session), but it was taking so long that I decided to look for alternatives to tmux.

### **2. nohup in the background**
[nohup](https://linuxize.com/post/linux-nohup-command/#running-the-command-in-background) is short for no hang up. It is a command that takes another command as its argument and runs it as a process that doesn't close when the session is terminated. Running `nohup python3 bot.py &` ran the program in the background and gave me a process ID as an output, so I could run `kill -9 [process ID]` when I wanted to stop the program. 

However, I also read that nohup is not the best for processes that need to stay running indefinitely, since they can also be terminated for reasons other than a closed terminal. I saw suggestions to "daemonize" the program with systemd, which brought me to my third approach.

### **3. creating a systemd service + regular restarts with cron**
writing in progress! 

