from requests import get
import json
import csv
import time
from datetime import datetime, timezone


def log(msg):
    '''
    Prints a message with a timestamp attached to it
    :param msg: the message to be printed
    '''
    timestamp = time.time()
    date = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M')
    print(str(date) + " -> " + msg)


def get_hourly_timestamp():
    '''
    :return: a timestamp rounded to the nearest hour
    '''
    timestamp = time.time()
    timestamp -= timestamp % 3600
    return int(timestamp)


hdr = {
    'User-Agent': 'prices_for_ml_project @Kael558#4332'
}


def write_to_csv(foldername, datatype, data):
    '''
    :param foldername: the folder to print to (e.g. Ore, Seed)
    :param datatype: the type of data to save (e.g. fandom, high_price)
    :param data: the data to save in a list
    '''
    path = foldername + "/" + foldername + "_"
    with open('C:/Users/Rahel/PycharmProjects/OSRSInvestor/data/{}{}_data.csv'.format(path, datatype), mode='a',
              newline='') as file:
        writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)



def cml_xp_api_scraper():
    '''
    Getting the top 200 players daily xp in each skill for both ironmen and no filter.
    Subtracting the ironmen xp from the no filter xp to get xp for non-ironmen players
    Writing the data to the xp file
    '''
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
              "count": str(count)}]

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
        try:
            for line in response.text.splitlines():
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
            log("Error parsing CML data. Retry in 60s  -> " + str(e))
            time.sleep(60)
            continue
        break
    write_to_csv('XP', 'CML', [get_hourly_timestamp()] + list(xp_averages.values()))


def cml_xp_api_scraper_v2():
    '''
    Queries the total daily xp gained in each skill for no filter and ironmen
    Subtracts the ironmen xp from no filter xp to get the xp gained by non-ironmen players
    Write to file
    '''
    skills = ["runecrafting", "magic", "fletching", "woodcutting", "firemaking", "construction", "farming", "herblore",
              "thieving",
              "mining", "smithing"]

    allQuery = list(map(lambda s: {"skill": s}, skills))
    allQuery[0]["type"] = "totalgains"
    allQuery[0]["timeperiod"] = "day"
    ironmanQuery = list(map(lambda s: {"skill": s}, skills))
    ironmanQuery[0]["filter"] = "ironman>0"
    query = allQuery + ironmanQuery

    base_url = "https://www.crystalmathlabs.com/tracker/api.php?multiquery="
    xp_url = base_url + str(query).replace('\'', '"').replace(" ", "")
    while True:
        while True:
            response = get(xp_url, headers=hdr)
            if response:
                break
            log("CML XP API currently unavailable. Retry in 60s -> " + str(response))
            time.sleep(60)

        try:
            xp_totals = list(map(int, response.text.strip().replace("\n", "").split("~~")[:-1]))
            xp_filtered = [xp_totals[i] - xp_totals[i + len(skills)] for i in range(len(skills))]
            write_to_csv('XP', 'CML', [get_hourly_timestamp()] + list(xp_filtered))
        except Exception as e:
            log("Error parsing CML data. Retry in 60s  -> " + str(e))
            time.sleep(60)
            continue
        break

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
                while True:
                    r = get(item_url, headers=hdr)
                    if r and r.text != "":
                        break
                    log("Fandom Prices API currently unavailable for item ID: " + str(itemID) + ". Retry in 20s -> " + str(r))
                    time.sleep(20)
                try:
                    json_data = json.loads(r.text)
                    prices.append(list(json_data["daily"].items())[-1][1])
                except Exception as e:
                    log("Error parsing Fandom data for item ID: " + str(itemID) + ". Retry in 60s  -> " + str(e))
                    time.sleep(60)
                    continue
                break

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


def official_OSRS_prices_api_historical_scraper():
    """
    INSTANT BUY - high (people selling that item)
    person A sells item.
    person B buys item.

    INSTANT SELL - low (people buying that item)
    person A buys item.
    person B sells item.

    instant-buy = high
    instant-sell = low
    :return:
    """
    # Item names
    item_names = {'Body rune', 'Lava rune', 'Soul rune', 'Cosmic rune', 'Law rune', 'Nature rune', 'Mind rune',
                  'Chaos rune', 'Blood rune', 'Death rune', 'Feather', 'Bow string', 'Headless arrow', 'Yew logs',
                    'Magic logs', 'Maple logs', 'Willow logs', 'Redwood logs', 'Teak logs', 'Steel nails', 'Oak plank',
                    'Teak plank', 'Mahogany plank', 'Magic seed', 'Dragonfruit tree seed', 'Mahogany seed', 'Redwood tree seed',
                    'Limpwurt root', 'Snape grass', 'Mort myre fungus', 'Torstol', 'Potato cactus', 'Crushed nest',
                    'Volcanic ash', 'Blood shard', 'Enhanced crystal teleport seed', 'Iron ore',  'Iron bar',
                    'Steel bar', 'Mithril bar', 'Adamantite bar', 'Runite bar', 'Gold bar'}
    item_names = {'Redwood tree seed'}
    while True:
        url = 'https://prices.runescape.wiki/api/v1/osrs/mapping'
        response = get(url, headers=hdr)
        if response:
            break
        print("OSRS Wiki API currently unavailable. Retry in 60s -> " + str(response))
        time.sleep(60)
    all_items = json.loads(response.text)
    name_to_id = {o['name']:o['id'] for o in all_items if o['name'] in item_names}

    for item_name in item_names:
        if item_name not in name_to_id:
            print("Item not found: " + item_name)
            continue
        item_id = name_to_id[item_name]

        with open(f"C:/Users/Rahel/PycharmProjects/OSRSInvestor/data/Items/{item_name}.csv", mode='a',
                  newline='') as file:
            url = f'https://prices.runescape.wiki/api/v1/osrs/timeseries?timestep=6h&id={item_id}'
            writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            writer.writerow(['timestamp', 'avgHighPrice', 'avgLowPrice', 'highPriceVolume', 'lowPriceVolume'])
            while True:
                response = get(url, headers=hdr)
                if response:
                    break
                print("Prices API currently unavailable. Retry in 60s -> " + str(response))
                time.sleep(60)

            try:
                json_data = json.loads(response.text)["data"]
                #print(json_data)
                for datapoint in json_data:
                    dt_object = datetime.fromtimestamp(datapoint["timestamp"], tz=timezone.utc)
                    #print(dt_object)
                    if dt_object.hour == 12:
                        row = [int(datapoint["timestamp"]), datapoint["avgHighPrice"],
                               datapoint["avgLowPrice"], datapoint["highPriceVolume"], datapoint["lowPriceVolume"]]
                        writer.writerow(row)
            except Exception as e:
                print(f"Error parsing prices for item: {id}. Retry in 60s  -> " + str(e))
            file.close()


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
        while True:
            response = get(prices_url, headers=hdr)
            if response:
                break
            log("Official OSRS Prices API unavailable. Retry in 60s -> " + str(response))
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
            log("Error parsing official OSRS data. Retry in 60s  -> " + str(e))
            time.sleep(60)
            continue
        break


if __name__ == "__main__":
    '''cml_xp_api_scraper_v2()
    log("Collected XP data.")

    fandom_prices_api_scraper()
    log("Collected fandom prices data.")

    official_OSRS_prices_api_scraper()
    log("Collected prices data.")'''

    official_OSRS_prices_api_historical_scraper()
    log("Collected prices data.")
