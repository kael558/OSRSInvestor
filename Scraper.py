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


timestamp = time.time()

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
            # print(str(skillIndex) + ": " + str(len(vanilla_players)))
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


def create_list(*args):
    lst = []
    for each in args:
        lst.extend(each)
    return lst


runes = list(range(554, 567, 1))  # Runes
logs = [1511, 1513, 1515, 1517, 1519, 1521]
seeds = create_list(list(range(5096, 5107, 1)), list(range(5280, 5317, 1)), list(range(5318, 5325, 1)))
ores = [436, 438, 440, 442, 444, 447, 449, 451]

itemIDList = create_list(runes, logs, seeds, ores)

timestamp = time.time()

runePrices = [timestamp]
logPrices = [timestamp]
seedPrices = [timestamp]
orePrices = [timestamp]

for itemID in itemIDList:
    url = 'http://services.runescape.com/m=itemdb_oldschool/api/graph/{}.json'.format(itemID)
    r = get(url, headers=hdr)
    json_data = json.loads(r.text)
    price = list(json_data["daily"].items())[-1][1]

    if itemID in runes:
        runePrices.append(price)
    elif itemID in logs:
        logPrices.append(price)
    elif itemID in seeds:
        seedPrices.append(price)
    elif itemID in ores:
        orePrices.append(price)


def write_to_csv(filename, data):
    with open('data/{}_data.csv'.format(filename), mode='a', newline='') as GE_data:
        GE_writer = csv.writer(GE_data, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        GE_writer.writerow(data)


write_to_csv('Rune', runePrices)
write_to_csv('Log', logPrices)
write_to_csv('Seed', seedPrices)
write_to_csv('Ore', orePrices)
write_to_csv('XP', [timestamp] + list(xp_averages.values()))

