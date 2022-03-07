# bot.py
# The code for our bot

import cfg
import utils
import socket
import re
import time, _thread
import http
import urllib
import requests
from time import sleep
from urllib.parse import urlencode
from requests import Session
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, InvalidURL, ConnectionError
import json
import datetime
import timestring
import time
import timestring


def main():
    # Networking functions for Twitch connections
    s = socket.socket()
    s.connect((cfg.HOST, cfg.PORT))
    s.send("PASS {}\r\n".format(cfg.PASS).encode("utf-8"))
    s.send("NICK {}\r\n".format(cfg.NICK).encode("utf-8"))
    s.send("JOIN #{}\r\n".format(cfg.CHAN).encode("utf-8"))

    CHAT_MSG = re.compile(r"^:\w+!\w+@\w+\.tmi\.twitch\.tv PRIVMSG #\w+ :")
    utils.chat(s, "Hi everyone!")
    future = time.time() + 300
    messagecnt = 0
    while True:
        #keeps bot in IRC channel
        response = s.recv(1024).decode("utf-8")
        if response == "PING :tmi.twitch.tv\r\n":
            s.send("PONG :tmi.twitch.tv\r\n".encode("utf-8"))
            print("PONG")
        else:
            messagecnt += 1
            # grabs username and message from chat
            username = re.search(r"\w+", response).group(0)
            message = CHAT_MSG.sub("", response)
            print(response)
            # reads message and parses for command or banned words
            # checks for banned words and timesouts/bans users
            
            if message.strip() in cfg.Banhammer:
                if username in cfg.Banned:   
                    if cfg.Banned[username] >= 3:  # if third offense, ban
                        utils.ban(s, username)
                        utils.clearmsg(s, message)
                        utils.chat(s,"@"+username+" I have warned you, now you are banned")
                    if cfg.Banned[username] < 3:   # gives users 2 timeouts before banning 
                        utils.timeout(s, username)
                        utils.clearmsg(s, message)
                        utils.chat(s,"@"+username+" Please do not say that, you are timeouted for 600 secs.")
                elif username not in cfg.Banned:   # 1st and only warning before timeout/ban
                    cfg.Banned[username] = 1
                    utils.clearmsg(s, message)
                    utils.chat(s,"@"+username+" Please do not say that, next time you will get a timeout")
                cfg.Banned[username] += 1
                
            #returns time
            elif message.strip() == "!time":
                dt = datetime.datetime.now().time()
                timenow = str(dt)
                timenow = timenow[:5] #change for timezone
                utils.chat(s, "The time for "+str(cfg.CHAN)+" is " + str(timenow))
                

            # uses link to check if following and for how long
            elif message.strip() == "!followage":
                utils.followage(s,username)
                    
            #show how long stream has been going    
            elif message.strip() == "!uptime":
                utils.uptime(s)
                
            #returns solo/duo rank lol
            elif "!rank" in message:
                user = message.strip()[6:]
                if user == "":
                    user = cfg.CHAN
                utils.rank(s,user)
                
            # Step 5 #social media, change to fit your needs
            #returns op.gg link
            elif message.strip() == "!opgg":
                utils.chat(s, "http://na.op.gg/summoner/userName=ChillChewie")
            #returns twitter
            elif message.strip() == "!twitter":
                utils.chat(s, "https://twitter.com/ChillChewie69")
            #returns website
            elif message.strip() == "!website":
                utils.chat(s, "Check out my website! https://www.chillchewie.com")
            #returns YT
            elif message.strip() == "!youtube":
                utils.chat(s, "Subscribe to my youtube! https://www.youtube.com/channel/UCeww7jldHCVcb9PHaP2lxSg")
            #return social links
            elif message.strip() == "!social":
                utils.chat(s, "Follow ChillChewie on all social media. YT: https://www.youtube.com/channel/UCeww7jldHCVcb9PHaP2lxSg TW: https://twitter.com/ChillChewie69 WS: https://www.chillchewie.com")
            #returns link to all commands
            elif message.strip() == "!commands":
                utils.chat(s, "https://www.chillchewie.com/commands")
            #returns link to sub to channel
            elif message.strip() == "!sub":
                utils.chat(s, "Please consider subscribing! With Amazon Prime you can sub to your favorite channel for free! - https://www.twitch.tv/subs/chillchewie")
            #returns link to tip streamer
            elif message.strip() == "!tips":
                utils.chat(s, "All donations are appreciated! - https://streamlabs.com/ChillChewie")
            # quits the program if brodcaster - this is used to stop the bot from running
            elif message.strip() == "!quit" and username == cfg.CHAN:
                break
            elif "!" in message.strip()[0]:
                utils.chat(s, "That is not a command. Please use !commands for the commands.")
            
            #waits until 3 chats and 10 mins have passed to send spam
            if messagecnt > 10 and time.time() > future:
                utils.chat(s,"If you like my stream please follow! My goal is 100 followers! " +
                           "Also, consider subscribing! With Amazon Prime you can sub to your favorite channel for free!")
                future = time.time() + 300
                messagecnt = 0
        sleep(1/cfg.RATE)
    utils.chat(s, "Bye everyone :)");
if __name__ == "__main__":
    main()
