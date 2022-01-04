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

