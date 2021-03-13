# nice-music-bot
Discord bot that collects all the song links sent in a channel and adds them to a Spotify playlist 

It responds to 7 commands (all using the prefix "!nm"):
- **cleanup**    - Deletes all bot-related messages in channel (commands sent by users, messages sent by the bot).
- **collect**    - Adds all Spotify links in a channel to a playlist, reacts to messages with ✅  if it was successfully added.
- **help**       - Lists all the commands with brief descriptions.
- **link**       - Sends a link to the playlist in the channel.
- **ping**       - Checks if bot is online.
- **uncheck**    - Removes all ✅  reactions in this channel.
- **uncheckred** - Removes all red box reactions in this channel.
