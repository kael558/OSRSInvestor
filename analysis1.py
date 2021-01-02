import inline as inline
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

'''
runes - runecrafting, magic,
logs - fletching, woodcutting, firemaking, construction,
seeds - farming, herblore, thieving??
ores - mining, smithing
'''

df = pd.read_csv('data/Rune_data.csv')
df.set_index('timestamp')
df.head()

print(df.describe())
print(df.shape)