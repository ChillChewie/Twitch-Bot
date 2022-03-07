# Twitch-Bot
Twitch bot is used for a mostly League of Legends stream on twitch.
The commands for this bot can be seen here - https://chillchewie.com/commands

This bot primarily uses the Twitch API and Riot API for the commands to pull information about the streamer and summoners. 
There is a setup process to getting this python code working with your setup.
1.)	Create a twitch account for your bot – exp. ChillChewie_bot
2.)	You need to register the application with the Twitch API login under your bot account - https://dev.twitch.tv/console/apps
a.	Create an application
b.	Copy clientid and the client secret
c.	Add them both to the cfg.py file under the variables clientid and clientsecret
d.	Enter this url replacing the XXX you’re your clientid -https://id.twitch.tv/oauth2/authorize?response_type=token&client_id=XXX &redirect_uri=http://localhost
e.	Authorize with your bot channel. The page will redirect and give you an accesstoken. Exp. - http://localhost/#access_token=XXXX&scope=&token_type=bearer
f.	Add the access token to the cfg.py file in the variable accesstoken

3.)	You need a RIOT API login - https://developer.riotgames.com
a.	You can sign in with an existing Riot account.
b.	Register a personal API key and project
c.	Once approved you can get the API Key
d.	Add API key to the cfg.py file under the variable leagueAPI
e.	This API key may expire and you will need to  regenerate a key
4.)	There is one more thing to do to register the chat bot for IRC access.
a.	Go to https://twitchapps.com/tmi/ and register the bot account.
b.	Copy the code and enter into the cfg.py variable- PASS

ENJOY!
