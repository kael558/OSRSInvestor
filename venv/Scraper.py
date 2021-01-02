'''
api.php?type= (records | currenttop)
[&timeperiod = (day | week | month)]
[&skill= (skill)]
[&players= (name1,name2...) | &compid= (id) | &groupid= (id)]
[&filter= (vh_filter)]
[&pagenum= (page)]
[&count= (players per page)]

api.php?
type=currenttop
&timeperiod=day
&skill=1
&filter==2
&pagenum=3
&count=200



1. skill=
runes - runecrafting, magic,
logs - fletching, woodcutting, firemaking, construction,
seeds - farming, herblore, thieving??
ores - mining, smithing

2. filter=
ironman>0, none

3. pagenum=
1 - 10

api.php?multiquery= [
{"type": "currenttop", "timeperiod": "day", "skill": "runecraft", "filter": "ironman>0", "pagenum":"1", "count": "30"},
{"pagenum":"2"},
{"pagenum":"3"},
{"pagenum":"4"},
{"pagenum":"5"},
{"pagenum":"6"},
{"pagenum":"7"},
{"pagenum":"8"},
{"pagenum":"9"},
{"pagenum":"10"},
{"filter" : "", "pagenum" : "1"},
{"pagenum":"2"},
{"pagenum":"3"},
{"pagenum":"4"},
{"pagenum":"5"},
{"pagenum":"6"},
{"pagenum":"7"},
{"pagenum":"8"},
{"pagenum":"9"},
{"pagenum":"10"},
]


'''

from requests import get
from csv import DictReader
from bs4 import BeautifulSoup as Soup
import json




base_url = "http://www.crystalmathlabs.com/tracker/api.php?multiquery="

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://cssspritegenerator.com',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


skills = ["runecraft", "magic", "fletching", "woodcutting", "firemaking", "construction", "farming", "herblore", "thieving", "mining", "smithing"]


for skill in skills:
    query=[{"type":"currenttop","timeperiod":"day","skill":"","filter":"ironman>0","pagenum":"1","count":"30"},
    {"pagenum":"2"},
    {"pagenum":"3"},
    {"pagenum":"4"},
    {"pagenum":"5"},
    {"pagenum":"6"},
    {"pagenum":"7"},
    {"pagenum":"8"},
    {"pagenum":"9"},
    {"pagenum":"10"},
    {"filter":"","pagenum":"1"},
    {"pagenum":"2"},
    {"pagenum":"3"},
    {"pagenum":"4"},
    {"pagenum":"5"},
    {"pagenum":"6"},
    {"pagenum":"7"},
    {"pagenum":"8"},
    {"pagenum":"9"},
    {"pagenum":"10"},
    ]

    query[0]["skill"] = skill

    print(skill)
    url = str(base_url) + str(json.dumps(query).replace(" ", ""))
    print(url)

    response = get(url, headers=hdr)

    ironmanPlayers = {}
    allPlayers = {}

    pageNum = 1
    readingIronman = True

    if response.text.__contains__("-4"):
        exit(-4)

    for line in response.text.splitlines():
        print(line)
        if line == "":
            continue
        elif line == "~~":
            pageNum += 1
            continue

        if pageNum == 11:
            pageNum = 1
            readingIronman = False

        if readingIronman:
            ironmanPlayers[line.split(",")[0]] = line.split(",")[1]
        else:
            allPlayers[line.split(",")[0]] = line.split(",")[1]

    print(len(allPlayers))
    print(len(ironmanPlayers))

    def subtract(d1, d2):
        res = dict()
        for key in d1:
            if key not in d2:
                res[key] = d1[key]
        return res

    def average(lst):
        return sum(lst)/len(lst)

    vanilla_players = subtract(allPlayers, ironmanPlayers)

    print(len(vanilla_players))
    print(vanilla_players)

    xp_list = [int(i) for i in vanilla_players.values()]

    print(average(xp_list))












