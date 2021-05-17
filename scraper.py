from requests import get
import json
import csv
import time
from datetime import datetime


def log(msg):
    timestamp = time.time()
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
    print(str(date) + " -> " + msg)


# Returns a timestamp floor rounded to the nearest hour
def get_hourly_timestamp():
    timestamp = time.time()
    timestamp -= timestamp % 3600
    timestamp *= 1000
    return int(timestamp)


hdr = {
    'User-Agent': 'prices_for_ml_project @kael',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Referer': 'https://github.com/kael558/OSRSInvestor',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}


def write_to_csv(foldername, datatype, data):
    path = foldername + "/" + foldername + "_"
    with open('C:/Users/Rahel/PycharmProjects/OSRSInvestor/data/{}{}_data.csv'.format(path, datatype), mode='a',
              newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)


def cml_xp_api_scraper():
    pages = 10
    skills = ["magic", "fletching", "woodcutting", "firemaking", "construction", "farming", "herblore", "thieving",
              "mining", "smithing"]
    count = 200

    def subtract(d1, d2):
        res = dict()
        for key in d1:
            if key not in d2:
                res[key] = d1[key]
        return res

    def average(lst):
        return sum(lst) / len(lst)

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
    xp_url = str(base_url) + str(json.dumps(query).replace(" ", ""))

    while True:
        response = get(xp_url, headers=hdr)
        if response:
            break
        log("CML XP API currently unavailable. Retry in 60s -> " + str(response))
        time.sleep(60)

    groupNum = 0
    skillIndex = -1
    ironmanPlayers = {}
    allPlayers = {}
    readingIronman = True
    xp_averages = {}
    for line in response.text.splitlines():
        try:
            if line == "":
                continue
            elif line == "~~":
                groupNum += 1
                if groupNum % (2 * pages) == 0 and groupNum != 0:
                    readingIronman = True
                    vanilla_players = subtract(allPlayers, ironmanPlayers)
                    xp_list = [int(i) for i in vanilla_players.values()]
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
        except Exception as e:
            print(e)
            print(line)
            exit(0)
    write_to_csv('XP', '', [get_hourly_timestamp()] + list(xp_averages.values()))


def fandom_prices_api_scraper():
    # Item IDs
    runes = list(range(554, 567, 1))
    logs = [1511, 1513, 1515, 1517, 1519, 1521]
    seeds = list(range(5096, 5107, 1)) + (list(range(5280, 5317, 1))) + (list(range(5318, 5325, 1)))
    ores = [436, 438, 440, 442, 444, 447, 449, 451]

    def get_item_prices(itemIDList):
        prices = []
        for itemID in itemIDList:
            item_url = 'http://services.runescape.com/m=itemdb_oldschool/api/graph/{}.json'.format(itemID)
            while True:
                r = get(item_url, headers=hdr)
                if r and r.text != "":
                    break
                log("Fandom Prices API currently unavailable for item ID: " + str(itemID) + ". Retry in 20s -> " + str(r))
                time.sleep(20)
            try:
                json_data = json.loads(r.text)
                prices.append(list(json_data["daily"].items())[-1][1])
            except:
                print(itemID)
                print(r)
                exit(0)

        return prices

    timestamp = get_hourly_timestamp()
    runePrices = [timestamp] + get_item_prices(runes)
    logPrices = [timestamp] + get_item_prices(logs)
    seedPrices = [timestamp] + get_item_prices(seeds)
    orePrices = [timestamp] + get_item_prices(ores)

    write_to_csv('Rune', 'fandom', runePrices)
    write_to_csv('Log', 'fandom', logPrices)
    write_to_csv('Seed', 'fandom', seedPrices)
    write_to_csv('Ore', 'fandom', orePrices)


def official_OSRS_prices_api_scraper():
    # Item IDs
    rune_ids = list(map(str, list(range(554, 567, 1))))
    log_ids = list(map(str, [1511, 1513, 1515, 1517, 1519, 1521]))
    seed_ids = list(map(str, list(range(5096, 5107, 1)) + (list(range(5280, 5317, 1))) + (list(range(5318, 5325, 1)))))
    ore_ids = list(map(str, [436, 438, 440, 442, 444, 447, 449, 451]))

    def get_item_if_exists(item_id):
        return json_data[item_id] if item_id in json_data \
            else {'avgHighPrice': 0, 'highPriceVolume': 0, 'avgLowPrice': 0, 'lowPriceVolume': 0}

    # Average between high price & low price weighted with volume
    def datapoint_to_average_price(dp):
        if dp["highPriceVolume"] == 0 and dp["lowPriceVolume"] == 0:
            print("no sales")
            return 0
        if dp["highPriceVolume"] == 0:
            return dp["avgLowPrice"]
        if dp["lowPriceVolume"] == 0:
            return dp["avgHighPrice"]
        total_volume = dp["highPriceVolume"] + dp["lowPriceVolume"]
        return dp["avgHighPrice"] * dp["highPriceVolume"] / total_volume + dp["avgLowPrice"] * dp[
            "lowPriceVolume"] / total_volume

    prices_url = "https://prices.runescape.wiki/api/v1/osrs/1h?"
    while True:
        response = get(prices_url, headers=hdr)
        if response:
            break
        print("Official OSRS Prices API unavailable. Retry in 60s -> " + str(response))
        time.sleep(60)
    try:
        json_data = json.loads(response.text)["data"]
        log_prices = [get_item_if_exists(item_id) for item_id in log_ids]
        ore_prices = [get_item_if_exists(item_id) for item_id in ore_ids]
        rune_prices = [get_item_if_exists(item_id) for item_id in rune_ids]
        seed_prices = [get_item_if_exists(item_id) for item_id in seed_ids]

        # Parsing datapoints
        timestamp = get_hourly_timestamp()
        log_avg_price = [timestamp] + [datapoint_to_average_price(dp) for dp in log_prices]
        ore_avg_price = [timestamp] + [datapoint_to_average_price(dp) for dp in ore_prices]
        rune_avg_price = [timestamp] + [datapoint_to_average_price(dp) for dp in rune_prices]
        seed_avg_price = [timestamp] + [datapoint_to_average_price(dp) for dp in seed_prices]

        log_avg_high_price = [timestamp] + [dp["avgHighPrice"] for dp in log_prices]
        ore_avg_high_price = [timestamp] + [dp["avgHighPrice"] for dp in ore_prices]
        rune_avg_high_price = [timestamp] + [dp["avgHighPrice"] for dp in rune_prices]
        seed_avg_high_price = [timestamp] + [dp["avgHighPrice"] for dp in seed_prices]

        log_high_price_vol = [timestamp] + [dp["highPriceVolume"] for dp in log_prices]
        ore_high_price_vol = [timestamp] + [dp["highPriceVolume"] for dp in ore_prices]
        rune_high_price_vol = [timestamp] + [dp["highPriceVolume"] for dp in rune_prices]
        seed_high_price_vol = [timestamp] + [dp["highPriceVolume"] for dp in seed_prices]

        log_avg_low_price = [timestamp] + [dp["avgLowPrice"] for dp in log_prices]
        ore_avg_low_price = [timestamp] + [dp["avgLowPrice"] for dp in ore_prices]
        rune_avg_low_price = [timestamp] + [dp["avgLowPrice"] for dp in rune_prices]
        seed_avg_low_price = [timestamp] + [dp["avgLowPrice"] for dp in seed_prices]

        log_low_price_vol = [timestamp] + [dp["lowPriceVolume"] for dp in log_prices]
        ore_low_price_vol = [timestamp] + [dp["lowPriceVolume"] for dp in ore_prices]
        rune_low_price_vol = [timestamp] + [dp["lowPriceVolume"] for dp in rune_prices]
        seed_low_price_vol = [timestamp] + [dp["lowPriceVolume"] for dp in seed_prices]

        write_to_csv('Log', "avg_price", log_avg_price)
        write_to_csv('Ore', "avg_price", ore_avg_price)
        write_to_csv('Rune', "avg_price", rune_avg_price)
        write_to_csv('Seed', "avg_price", seed_avg_price)

        write_to_csv('Log', "high_price", log_avg_high_price)
        write_to_csv('Ore', "high_price", ore_avg_high_price)
        write_to_csv('Rune', "high_price", rune_avg_high_price)
        write_to_csv('Seed', "high_price", seed_avg_high_price)

        write_to_csv('Log', "high_vol", log_high_price_vol)
        write_to_csv('Ore', "high_vol", ore_high_price_vol)
        write_to_csv('Rune', "high_vol", rune_high_price_vol)
        write_to_csv('Seed', "high_vol", seed_high_price_vol)

        write_to_csv('Log', "low_price", log_avg_low_price)
        write_to_csv('Ore', "low_price", ore_avg_low_price)
        write_to_csv('Rune', "low_price", rune_avg_low_price)
        write_to_csv('Seed', "low_price", seed_avg_low_price)

        write_to_csv('Log', "low_vol", log_low_price_vol)
        write_to_csv('Ore', "low_vol", ore_low_price_vol)
        write_to_csv('Rune', "low_vol", rune_low_price_vol)
        write_to_csv('Seed', "low_vol", seed_low_price_vol)
    except Exception as e:
        print(e)
        print("Error parsing data")
        exit(0)


cml_xp_api_scraper()
log("Collected XP data.")

fandom_prices_api_scraper()
log("Collected fandom prices data.")

official_OSRS_prices_api_scraper()
log("Collected prices data.")
