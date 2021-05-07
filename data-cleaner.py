from datetime import datetime
import csv

# inclusive indicies
def remove_entries(filename, start_index, end_index):
    with open('data/{}_data.csv'.format(filename), 'r') as r, open('data/{}_edited_data.csv'.format(filename), 'w', newline='') as w:
        reader = csv.reader(r, delimiter=',')
        writer = csv.writer(w, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for i, entry in enumerate(reader):
            if i < start_index or i > end_index or i == 0:
                writer.writerow(entry)

#remove_entries('Log', 1, 18)
#remove_entries('Ore', 1, 18)
#remove_entries('Rune', 1, 18)
#remove_entries('Seed', 1, 18)
#remove_entries('XP', 1, 18)

def read_csv(filename):
    with open('data/{}_data.csv'.format(filename), mode='r',newline='') as file:
        reader = csv.reader(file, delimiter=',')
        for i, entry in enumerate(reader):
            if i > 0:
                dt = datetime.fromtimestamp(float(entry[0]))
                print(str(i) + ': ' + dt.strftime('%Y-%m-%d %H:%M:%S.%f'))

read_csv('Seed')