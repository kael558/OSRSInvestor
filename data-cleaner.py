from datetime import datetime
import csv
from requests import get
import time
import json


# inclusive indicies
def remove_entries(filename, start_index, end_index):
    with open('data/{}_data.csv'.format(filename), 'r') as r, open('data/{}_edited_data.csv'.format(filename), 'w',
                                                                   newline='') as w:
        reader = csv.reader(r, delimiter=',')
        writer = csv.writer(w, delimiter=',')
        for i, entry in enumerate(reader):
            if i < start_index or i > end_index or i == 0:
                writer.writerow(entry)


# remove_entries('Log', 1, 18)
# remove_entries('Ore', 1, 18)
# remove_entries('Rune', 1, 18)
# remove_entries('Seed', 1, 18)
# remove_entries('XP', 1, 18)

def read_csv(filename):
    with open('data/{}_data.csv'.format(filename), mode='r', newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for i, entry in enumerate(reader):
            if i > 0:
                print(int(float(entry[0])))

                # dt = datetime.fromtimestamp(float(entry[0]))
                # print(str(i) + ': ' + dt.strftime('%Y-%m-%d %H:%M:%S.%f'))


'''
Replace existing prices data (obtained from fandom api) with official osrs wiki prices data 
'''
def fix_old_prices():
    hdr = {
        'User-Agent': 'one time verifying prices i have from fandom api @kael',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Referer': 'https://github.com/kael558/OSRSInvestor',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}

    # Item IDs
    rune_ids = list(map(str, list(range(554, 567, 1))))
    log_ids = list(map(str, [1511, 1513, 1515, 1517, 1519, 1521]))
    seed_ids = list(map(str, list(range(5096, 5107, 1)) + (list(range(5280, 5317, 1))) + (list(range(5318, 5325, 1)))))
    ore_ids = list(map(str, [436, 438, 440, 442, 444, 447, 449, 451]))

    # Too many nested blocks so these are coming out of the 'with'
    xp = open('data/{}_data.csv'.format('XP/XP'), mode='r', newline='')
    log_avg_file = open('data/{}_avg_price_data.csv'.format('Log/Log'), 'w', newline='')
    ore_avg_file = open('data/{}_avg_price_data.csv'.format('Ore/Ore'), 'w', newline='')
    rune_avg_file = open('data/{}_avg_price_data.csv'.format('Rune/Rune'), 'w', newline='')
    with open('data/{}_avg_price_data.csv'.format('Seed/Seed'), 'w', newline='') as seed_avg_file, \
            open('data/{}_high_price_data.csv'.format('Log/Log'), 'w', newline='') as log_high_price_file, \
            open('data/{}_high_price_data.csv'.format('Ore/Ore'), 'w', newline='') as ore_high_price_file, \
            open('data/{}_high_price_data.csv'.format('Rune/Rune'), 'w', newline='') as rune_high_price_file, \
            open('data/{}_high_price_data.csv'.format('Seed/Seed'), 'w', newline='') as seed_high_price_file, \
            open('data/{}_high_vol_data.csv'.format('Log/Log'), 'w', newline='') as log_high_vol_file, \
            open('data/{}_high_vol_data.csv'.format('Ore/Ore'), 'w', newline='') as ore_high_vol_file, \
            open('data/{}_high_vol_data.csv'.format('Rune/Rune'), 'w', newline='') as rune_high_vol_file, \
            open('data/{}_high_vol_data.csv'.format('Seed/Seed'), 'w', newline='') as seed_high_vol_file, \
            open('data/{}_low_price_data.csv'.format('Log/Log'), 'w', newline='') as log_low_price_file, \
            open('data/{}_low_price_data.csv'.format('Ore/Ore'), 'w', newline='') as ore_low_price_file, \
            open('data/{}_low_price_data.csv'.format('Rune/Rune'), 'w', newline='') as rune_low_price_file, \
            open('data/{}_low_price_data.csv'.format('Seed/Seed'), 'w', newline='') as seed_low_price_file, \
            open('data/{}_low_vol_data.csv'.format('Log/Log'), 'w', newline='') as log_low_vol_file, \
            open('data/{}_low_vol_data.csv'.format('Ore/Ore'), 'w', newline='') as ore_low_vol_file, \
            open('data/{}_low_vol_data.csv'.format('Rune/Rune'), 'w', newline='') as rune_low_vol_file, \
            open('data/{}_low_vol_data.csv'.format('Seed/Seed'), 'w', newline='') as seed_low_vol_file:

        time_reader = csv.reader(xp, delimiter=',')
        log_avg_writer = csv.writer(log_avg_file, delimiter=',')
        ore_avg_writer = csv.writer(ore_avg_file, delimiter=',')
        rune_avg_writer = csv.writer(rune_avg_file, delimiter=',')
        seed_avg_writer = csv.writer(seed_avg_file, delimiter=',')

        log_high_price_writer = csv.writer(log_high_price_file, delimiter=',')
        ore_high_price_writer = csv.writer(ore_high_price_file, delimiter=',')
        rune_high_price_writer = csv.writer(rune_high_price_file, delimiter=',')
        seed_high_price_writer = csv.writer(seed_high_price_file, delimiter=',')
        log_high_vol_writer = csv.writer(log_high_vol_file, delimiter=',')
        ore_high_vol_writer = csv.writer(ore_high_vol_file, delimiter=',')
        rune_high_vol_writer = csv.writer(rune_high_vol_file, delimiter=',')
        seed_high_vol_writer = csv.writer(seed_high_vol_file, delimiter=',')

        log_low_price_writer = csv.writer(log_low_price_file, delimiter=',')
        ore_low_price_writer = csv.writer(ore_low_price_file, delimiter=',')
        rune_low_price_writer = csv.writer(rune_low_price_file, delimiter=',')
        seed_low_price_writer = csv.writer(seed_low_price_file, delimiter=',')
        log_low_vol_writer = csv.writer(log_low_vol_file, delimiter=',')
        ore_low_vol_writer = csv.writer(ore_low_vol_file, delimiter=',')
        rune_low_vol_writer = csv.writer(rune_low_vol_file, delimiter=',')
        seed_low_vol_writer = csv.writer(seed_low_vol_file, delimiter=',')

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

        for i, entry in enumerate(time_reader):
            if i > 0:
                timestamp = int(float(entry[0]))
                timestamp -= timestamp % 3600

                url = "https://prices.runescape.wiki/api/v1/osrs/1h?timestamp={}".format(timestamp)
                print(str(i) + ': ' + url)
                while True:
                    response = get(url, headers=hdr)
                    if response:
                        break
                    print("API unavailable. Retry in 60s -> " + str(response))
                    time.sleep(60)
                try:
                    json_data = json.loads(response.text)["data"]
                    log_prices = [get_item_if_exists(item_id) for item_id in log_ids]
                    ore_prices = [get_item_if_exists(item_id) for item_id in ore_ids]
                    rune_prices = [get_item_if_exists(item_id) for item_id in rune_ids]
                    seed_prices = [get_item_if_exists(item_id) for item_id in seed_ids]
                except Exception as e:
                    print(e)
                    print("Error parsing data")
                    exit(0)

                # Parsing datapoints
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

                # CSV Writing
                log_avg_writer.writerow(log_avg_price)
                ore_avg_writer.writerow(ore_avg_price)
                rune_avg_writer.writerow(rune_avg_price)
                seed_avg_writer.writerow(seed_avg_price)

                log_high_price_writer.writerow(log_avg_high_price)
                ore_high_price_writer.writerow(ore_avg_high_price)
                rune_high_price_writer.writerow(rune_avg_high_price)
                seed_high_price_writer.writerow(seed_avg_high_price)

                log_high_vol_writer.writerow(log_high_price_vol)
                ore_high_vol_writer.writerow(ore_high_price_vol)
                rune_high_vol_writer.writerow(rune_high_price_vol)
                seed_high_vol_writer.writerow(seed_high_price_vol)

                log_low_price_writer.writerow(log_avg_low_price)
                ore_low_price_writer.writerow(ore_avg_low_price)
                rune_low_price_writer.writerow(rune_avg_low_price)
                seed_low_price_writer.writerow(seed_avg_low_price)

                log_low_vol_writer.writerow(log_low_price_vol)
                ore_low_vol_writer.writerow(ore_low_price_vol)
                rune_low_vol_writer.writerow(rune_low_price_vol)
                seed_low_vol_writer.writerow(seed_low_price_vol)



def replace_time_stamps_with_closest_hour(filename):
    with open('data/{}_data.csv'.format(filename), 'r') as r, \
            open('data/{}_fixed_timestamps_data.csv'.format(filename), 'w', newline='') as w:

        reader = csv.reader(r, delimiter=',')
        writer = csv.writer(w, delimiter=',')
        for i, entry in enumerate(reader):
            if i > 0:
                timestamp = int(float(entry[0]))
                timestamp -= timestamp % 3600
                entry[0] = timestamp
            writer.writerow(entry)



# replace_time_stamps_with_closest_hour('XP/XP')