import json
import requests
import sqlite3
import time
import urllib2



#def main():
    #print "lul"
    #gameID_to_match("WMC2TMNT1", "290059", "8a91e4d6956af1cb")



def urlopen_with_retry(url):
    return urllib2.urlopen(url)

def gameID_to_match(region, gameId, gameHash):
    
    data = getJSONReply("https://acs.leagueoflegends.com/v1/stats/game/" + str(region) + "/" + str(gameId) + "?gameHash=" + str(gameHash), False)
    patch = data["gameVersion"]
    gameType = data["gameType"]
    duration = data["gameDuration"]
    date = data["gameCreation"]
    ##TODO: fix this later
    team1 = "SOLOQ"
    team2 = "SOLOQ"
    tier = "TOURNAMENT"
    is_test = 0
    

    if data["teams"][0]["firstBlood"]:
        first_blood = 100
    else:
        first_blood = 200
    
    if data["teams"][0]["win"] == "Win":
        win = 100
    else:
        win = 200
    
    ##get champion pick info
    champs1 = []
    champs2 = []
    for p in data["participants"]:
        if p["teamId"] == 100:
            champs1.append(p["championId"])
        else:
            champs2.append(p["championId"])

    json_champs1 = json.dumps(champs1)
    json_champs2 = json.dumps(champs2)
    conn = sqlite3.connect('data/LolEsports.sqlite')
    c = conn.cursor()
    c.execute("CREATE TABLE IF NOT EXISTS Matches (gameID, gameHash, team1, team2, champs1, champs2, first_blood, duration, win, gametype, region, patch, tier, date, is_test);")
    c.execute("INSERT INTO Matches VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);", (gameId, gameHash, team1, team2, json_champs1, json_champs2, first_blood, duration, win, gameType, region, patch, tier, date, is_test))
    conn.commit()
    c.close()
    conn.close()

def getJSONReply(url, rate_limit = True):
    response = urlopen_with_retry(url)
    if rate_limit:
        Rate_Limiter(response)
    html = response.read();
    data = json.loads(html);
    return data;

def Rate_Limiter(response):
    #Gets data from league API headers, contains limit and how much youve used
    curAppCount = response.info().getheader('X-App-Rate-Limit-Count')
    curAppLimit = response.info().getheader('X-App-Rate-Limit')
    x = curAppCount.split(',')
    RequestsPerSecond = x[1].split(':')
    RequestsPerMinute = x[0].split(':')
    x = curAppLimit.split(',')
    MaxRequestsPerSecond = x[1].split(':')
    MaxRequestsPerMinute = x[0].split(':')

    if(int(RequestsPerMinute[0])>(int(MaxRequestsPerMinute[0])-2)):
        print "Rate too high, pausing for 30 secs"
        time.sleep(30)

    if(int(RequestsPerSecond[0])>(int(MaxRequestsPerSecond[0])-2)):
        print "Rate too high, pausing for 5 secs"
        time.sleep(5)


#main()