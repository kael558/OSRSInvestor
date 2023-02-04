import json
import boto3
import csv
from requests import get
import time

s3 = boto3.resource('s3')
bucket = s3.Bucket('osrs-data-investor')

hdr = {
    'User-Agent': 'prices_for_ml_project @Kael558#4332'
}

def get_hourly_timestamp():
    '''
    :return: a timestamp rounded to the nearest hour
    '''
    timestamp = time.time()
    timestamp -= timestamp % 3600
    return int(timestamp)


def download_bucket_files_to_local():
    def download_file(data_name: str, data_type: str):
        key = 'data/' + data_name + '_' + data_type + '.csv'
        local_file_name = '/tmp/' + data_name + '_' + data_type + '.csv'

        bucket.download_file(key, local_file_name)

    download_file('XP', 'Data')

    item_categories = ['Log', 'Ore', 'Rune', 'Seed']
    for item_category in item_categories:
        download_file(item_category, 'Prices')


def cml_xp_api_scraper():
    '''
    Queries the total daily xp gained in each skill for no filter and ironmen
    Subtracts the ironmen xp from no filter xp to get the xp gained by non-ironmen players
    Write to file
    '''
    skills = ["runecrafting", "magic", "fletching", "woodcutting", "firemaking", "construction", "farming", "herblore",
              "thieving", "mining", "smithing"]

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
            print("CML XP API currently unavailable. Retry in 60s -> " + str(response))
            time.sleep(60)

        try:
            xp_totals = list(map(int, response.text.strip().replace("\n", "").split("~~")[:-1]))
            xp_filtered = [xp_totals[i] - xp_totals[i + len(skills)] for i in range(len(skills))]
            entry = [get_hourly_timestamp()] + list(xp_filtered)
        except Exception as e:
            print("Error parsing CML data. Retry in 60s  -> " + str(e))
            time.sleep(60)
            continue
        break

    return entry



def append_entry_to_local_file(data_name: str, data_type: str, entry: list):
    '''
    Writes an entry into a csv file with the name from data name and data type
    :param data_name: the name of the data (e.g. Ore, Seed)
    :param data_type: the type of data to save (e.g. price, XP,)
    :param entry: the data to save
    '''
    local_file_name = '/tmp/' + data_name + '_' + data_type + '.csv'
    with open(local_file_name, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        writer.writerow(entry)


def upload_local_files_to_bucket():
    def upload_file(data_name: str, data_type: str):
        key = 'data/' + data_name + '_' + data_type + '.csv'
        local_file_name = '/tmp/' + data_name + '_' + data_type + '.csv'

        bucket.upload_file(local_file_name, key)

    upload_file('XP', 'Data')

    item_categories = ['Log', 'Ore', 'Rune', 'Seed']
    for item_category in item_categories:
        upload_file(item_category, 'Prices')


def lambda_handler(event, context):
    try:
        # Download files
        download_bucket_files_to_local()

        # Scrape data
        xp_data = cml_xp_api_scraper()

        # Append data to local files
        append_entry_to_local_file('XP', 'Data', xp_data)

        # Upload local files to bucket
        upload_local_files_to_bucket()
    except Exception as e:
        return {
            'statusCode': 500,
            'error': e,
        }

    return {
        'statusCode': 200
    }