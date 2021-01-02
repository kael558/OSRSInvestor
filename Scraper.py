from requests import get
import json
import csv
import time

pages = 10
skills = ["magic", "fletching", "woodcutting", "firemaking", "construction", "farming", "herblore", "thieving",
          "mining", "smithing"]
count = 200


def append_page_nums(query):
    for i in range(2, pages + 1):
        query.append({"pagenum": str(i)})
    return query


query = [{"type": "currenttop", "timeperiod": "day", "skill": "runecrafting", "filter": "ironman>0", "pagenum": "1",
          "count": ""}]
query[0]["count"] = str(count)


for skill in skills:
    query = append_page_nums(query)

    query.append({"filter": "", "pagenum": "1"})
    query = append_page_nums(query)

    query.append({"skill": skill, "filter": "ironman>0", "pagenum": "1"})

query = append_page_nums(query)
query.append({"filter": "", "pagenum": "1"})
query = append_page_nums(query)

base_url = "http://www.crystalmathlabs.com/tracker/api.php?multiquery="

hdr = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://cssspritegenerator.com',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}

url = str(base_url) + str(json.dumps(query).replace(" ", ""))

print(url)

response = get(url, headers=hdr)

if response.text.__contains__("-4"):
    print("API currently unavailable")
    exit(-4)


def subtract(d1, d2):
    res = dict()
    for key in d1:
        if key not in d2:
            res[key] = d1[key]
    return res


def average(lst):
    return sum(lst) / len(lst)


groupNum = 0
skillIndex = -1

ironmanPlayers = {}
allPlayers = {}

readingIronman = True

xp_averages = {}

for line in response.text.splitlines():
    if line == "":
        continue
    elif line == "~~":
        groupNum += 1
        if groupNum % (2 * pages) == 0 and groupNum != 0:
            readingIronman = True
            vanilla_players = subtract(allPlayers, ironmanPlayers)
            xp_list = [int(i) for i in vanilla_players.values()]
            #print(str(skillIndex) + ": " + str(len(vanilla_players)))
            if skillIndex == -1:
                xp_averages["runecrafting"] = average(xp_list)
            else:
                xp_averages[skills[skillIndex]] = average(xp_list)
            ironmanPlayers.clear()
            allPlayers.clear()
            skillIndex += 1
        elif groupNum % pages == 0 and groupNum != 0:
            readingIronman = False
        continue

    if readingIronman:
        ironmanPlayers[line.split(",")[0]] = line.split(",")[1]
    else:
        allPlayers[line.split(",")[0]] = line.split(",")[1]

#print(xp_averages)
timestamp = time.time()


























with open('data/XP_data.csv', mode='a', newline='') as XP_data:
    XP_writer = csv.writer(XP_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
    values = [timestamp]
    values.extend(xp_averages.values())
    XP_writer.writerow(values)  # write field names
