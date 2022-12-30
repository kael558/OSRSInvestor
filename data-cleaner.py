from datetime import datetime
import csv
from requests import get
import time
import json
import os


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
        prev = None
        for i, entry in enumerate(reader):
            if i > 0:
                dt = datetime.fromtimestamp(int(entry[0]))
                if prev is not None:
                    total_seconds = (dt - prev).total_seconds()
                    days = int(divmod(total_seconds, 86400)[0])
                    if days > 1:
                        new_entry = entry.copy()
                        new_entry[0] = str(int(prev.timestamp() + 86400))

                prev = dt


read_csv('Log/Log_avg_price')
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


def forward_fill():
    item_categories = ["Log", "Ore", "Rune", "Seed"]
    file_types = ["avg_price", "fandom", "high_price", "high_vol", "low_price", "low_vol"]

    all_data_files = [item_category + "/" + item_category + "_" + file_type
                      for item_category in item_categories
                      for file_type in file_types]

    data_cleaning_log_file = open('data/data_cleaning_log.txt', 'a')

    for data_file in all_data_files:
        file = 'data/{}_data.csv'.format(data_file)
        upd_file = 'data/{}_updated_data.csv'.format(data_file)
        seconds_in_day = 86400
        with open(file, 'r') as r, \
                open(upd_file, 'w', newline='') as w:
            reader = csv.reader(r, delimiter=',')
            writer = csv.writer(w, delimiter=',')
            prev = None
            for i, entry in enumerate(reader):
                if i > 0:
                    dt = datetime.fromtimestamp(int(entry[0]))
                    if prev is not None:
                        days_in_between = int(divmod((dt - prev).total_seconds(), seconds_in_day)[0])
                        if days_in_between > 1:
                            prev_entry[0] = str(int(prev.timestamp() + seconds_in_day))
                            data_cleaning_log_file.write("Forward Filled - " + data_file + " - "
                                                         + datetime
                                                         .fromtimestamp(int(prev_entry[0])).strftime("%d %b %Y, %H:%M")
                                                         + "\n")
                            writer.writerow(prev_entry)
                    prev_entry = entry
                    prev = dt
                writer.writerow(entry)
        os.remove(file)
        os.rename(upd_file, file)
    data_cleaning_log_file.close()



def replace_all_item_names_with_lower_case_letters():
    item_categories = ["Log", "Ore", "Rune", "Seed"]
    file_types = ["avg_price", "fandom", "high_price", "high_vol", "low_price", "low_vol"]


    all_data_files = [item_category + "/" + item_category + "_" + file_type
                      for item_category in item_categories
                      for file_type in file_types]

    for data_file in all_data_files:
        file = 'data/{}_data.csv'.format(data_file)
        upd_file = 'data/{}_updated_data.csv'.format(data_file)

        with open(file, 'r') as r, \
                open(upd_file, 'w', newline='') as w:
            reader = csv.reader(r, delimiter=',')
            writer = csv.writer(w, delimiter=',')
            for i, entry in enumerate(reader):
                if i == 0:
                    entry = [x.lower() for x in entry]
                writer.writerow(entry)
        os.remove(file)
        os.rename(upd_file, file)




def replace_time_stamps_with_closest_hour(data_file):
    file = 'data/{}_data.csv'.format(data_file)
    upd_file = 'data/{}_updated_data.csv'.format(data_file)

    with open(file, 'r') as r, \
            open(upd_file, 'w', newline='') as w:
        reader = csv.reader(r, delimiter=',')
        writer = csv.writer(w, delimiter=',')
        for i, entry in enumerate(reader):
            if i > 0:
                timestamp = int(float(entry[0]))
                timestamp -= timestamp % 3600
                entry[0] = timestamp
            writer.writerow(entry)
    os.remove(file)
    os.rename(upd_file, file)


def download_file(data_name: str, data_types: list[str]):
    for data_type in data_types:
        key = 'data/' + data_name + '/' + data_name + '_' + data_type + '_data.csv'
        local_file_name = '/tmp/' + data_name + '/' + data_name + '_' + data_type + '_data.csv'
        bucket.download_file(key, local_file_name)


def download_files_to_temp_folder():
    base_path = 'data'
    data_folders = ['Logs', 'Ores', 'Runes', 'Seeds', 'XP']


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


import json
import boto3
import csv
import os


def lambda_handler(event, context):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket('osrs-data-investor')

    data_name = 'XP'
    data_type = 'CML'

    os.mkdir('/tmp/XP')
    key = 'data/' + data_name + '/' + data_name + '_' + data_type + '_data.csv'
    # local_file_name = '/tmp/' + data_name + '/' + data_name + '_' + data_type + '_data.csv'
    local_file_name = '/tmp/XP/test.csv'
    bucket.download_file(key, local_file_name)

    print("Come on bro")
    with open(local_file_name, 'r') as infile:
        reader = csv.reader(infile, delimiter=',')
        for entry in reader:
            print(entry)

    return {
        'statusCode': 200
    }
