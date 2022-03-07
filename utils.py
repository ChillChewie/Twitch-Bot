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
from requests.structures import CaseInsensitiveDict
import json

#send chats
def chat(sock, msg):
    sock.send("PRIVMSG #{} :{}\r\n".format(cfg.CHAN, msg).encode("utf-8"))
    
#Ban user
def ban(sock, user):
    chat(sock, ".ban {}".format(user))
    
#timeout user
def timeout(sock, user):
    chat(sock, ".timeout {}".format(user))

#clear message from user
def clearmsg(sock, message):
    chat(sock, ".delete {}".format(message))

# returns rank lol
def rank(s,user):
    try:
        url = "https://na1.api.riotgames.com/lol/summoner/v4/summoners/by-name/" +str(user)+"?api_key="+cfg.leagueAPI
        response = requests.get(url)
        JSON = response.json()
        ID = JSON['id']
        ID = str(ID)
        League="https://na1.api.riotgames.com/lol/league/v4/entries/by-summoner/"+ID+"?api_key="+cfg.leagueAPI
        responseL = requests.get(League)
        JSONL = responseL.json()
        
        try:
            queue0 = JSONL[0]['queueType']
        except:
            utils.chat(s,str(user)+" is not ranked")
            
        for i in range(0,len(JSONL)):
            try:
                queue = JSONL[i]['queueType']
            except:
                pass
                
            if queue:
                queue = JSONL[i]['queueType']
                teir = JSONL[i]['tier']
                teir = str(teir)
                rank = JSONL[i]['rank']
                rank = str(rank)
                LP = JSONL[i]['leaguePoints']
                LP = str(LP)
                solorank = teir +" "+ rank +" "+ LP+"LP"
                utils.chat(s,str(user)+"'s " +str(queue) +" rank is: "+solorank)
    except:
        utils.chat(s,str(user)+" is not a summoner name")        
# returns followage 
def followage(s,username):
    try:
        #get username ID
        url = "https://api.twitch.tv/helix/users?login="+str(username)
        headers = CaseInsensitiveDict()
        headers["Client-Id"] = str(cfg.clientid)
        headers["Authorization"] = "Bearer " + str(cfg.accesstoken)
        response = requests.get(url, headers=headers)
        JSON = response.json()
        userID = JSON['data'][0]['id']
        

        #get channel ID
        url = "https://api.twitch.tv/helix/users?login="+str(cfg.CHAN)
        headers = CaseInsensitiveDict()
        headers["Client-Id"] = str(cfg.clientid)
        headers["Authorization"] = "Bearer " + str(cfg.accesstoken)
        response = requests.get(url, headers=headers)
        JSON = response.json()
        channelID = JSON['data'][0]['id']

        #get user follow date
        url = 'https://api.twitch.tv/helix/users/follows?to_id='+str(channelID)
        response = requests.get(url, headers=headers)
        JSON = response.json()
        followers = int(JSON['total'])
        print(followers)
        try:
            for x in range(0, followers):
                if userID in JSON['data'][x]['from_id']:
                    created = str(JSON['data'][x]['followed_at'])
                    created = created[0:created.index("T")]
                    d1 = datetime.datetime.now().date()
                    month = created[5:6]
                    if int(month) < 10:
                        month = created[6]
                    d2 = datetime.date(int(created[:4]), int(month), int(created[8:]))
                    follow = abs(d1-d2).days
                    utils.chat(s, username + " has been following "+str(cfg.CHAN)+" for "+str(follow)+" Days, Since: "+str(created))
        except:
            pass
    except:
        utils.chat(s, username + " is not following "+str(cfg.CHAN)+" :(")

def uptime(s):
    try:
        url = "https://api.twitch.tv/helix/streams?user_login="+cfg.CHAN
        headers = CaseInsensitiveDict()
        headers["Client-Id"] = str(cfg.clientid)
        headers["Authorization"] = "Bearer " + str(cfg.accesstoken)
        response = requests.get(url, headers=headers)
        JSON = response.json()
        created = JSON["data"][0]["started_at"]
        d1 = datetime.datetime.utcnow()
        d1 = str(d1)
        d1 = d1[0:d1.index(".")]
        d2 = created[0:created.index("Z")]
        d2 = d2.replace("T"," ")
        d3 = d2
        month = d2[5:6]
        if int(month) < 10:
            month = d2[6]
        d2 = datetime.datetime(int(d2[:4]), int(month), int(d2[8:10]), int(d2[11:13]), int(d2[14:16]), int(d2[17:]))
        month = d1[5:6]
        if int(month) < 10:
            month = d1[6]
        d1 = datetime.datetime(int(d1[:4]), int(month), int(d1[8:10]), int(d1[11:13]), int(d1[14:16]), int(d1[17:]))
        uptime = (d1-d2)
        uptime = str(uptime)
        if int(uptime[0]) == 0:
            utils.chat(s, str(cfg.CHAN)+" has been live for "+str(uptime[2:4])+" mins")
        else:
            utils.chat(s, str(cfg.CHAN)+" has been live for "+str(uptime[0])+"hrs "+str(uptime[2:4])+"mins")
    except:
        utils.chat(s,str(cfg.CHAN)+" is not live :(")
