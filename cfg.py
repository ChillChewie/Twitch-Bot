#all the information to connect to the IRC channel and API calls

#IRC Channel
HOST = "irc.chat.twitch.tv"
PORT = 6667
NICK = "chillchewie_bot" #bot name - change from chillchewie_bot / will need make a twitch channel for bot
PASS = "oauth:XXXX" #https://twitchapps.com/tmi/ - sign in with bot channel
CHAN = "chillchewie" # your main channel - change from chillchewie
RATE = (100/120) # messages per second



Banned={}  #dictionary to store banned users

# APIs for calls
clientid = "XXXXX" #Step 2 #https://dev.twitch.tv/console/apps
clientsecret = "XXXX" #Step 2
accesstoken = 'XXXX' #Step 2
leagueAPI = "RGAPI-XXXX" #Step 3  #https://developer.riotgames.com/ log in with league account and get api 

#banned words in chat
Banhammer = ('list','of','words') #change this list to words that you want banned in your chat

#make sure to change the social media commands to fit your needs in the bot.py file!!
