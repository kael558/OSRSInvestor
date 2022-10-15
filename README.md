### Project Outline
Old-School Runescape (OSRS) is a RPG based game where players may level up their skills by gaining experience (XP) and items at the same time. 
The game also contains a Grand Exchange (GE) that allows players to sell and buy items. 

The goal of this project is to use use multivariate time series analysis to predict future prices based on daily XP gained and previous item prices.

For example, a player chopping logs will gain experience and logs. They have gained woodcutting XP and then may sell the logs. This will increase the supply and lower the price. If the woodcutting XP gained is significant, then this would be a good time to buy logs.

The data is collected from 3 sources:
- XP data from [Crystal Math Labs (CML)](http://www.crystalmathlabs.com/tracker/). CML is an unofficial website where players independently sign up for their XP to be tracked.
- prices from [OSRS's official Prices API (OOPA)](https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices).
- prices from [fandoms' API (FA)](https://runescape.fandom.com/wiki/Application_programming_interface). Unofficial data collected for comparison against official prices.

There are problems with such an analysis:
 - Players may wait variable amounts of time before selling their obtained items.
 - Hardcore players may drop their items instead of selling.
 - Bots that harvest vast amounts of items (thereby lowering prices) will be untracked by the XP tracker.

The solutions to these problems are:
 - Observing if there is a time period that players wait.
 - Identifying particular skills where botting and hardcore players are less impactful.

### Acknowledgements
[Chronic Coder's GE Prediction Repo](https://github.com/chriskok/GEPrediction-OSRS) for the baseline of this project.

### Configuration
**Packages**  
Download packages from requirements.txt to your environment with:
```
pip install -r requirements.txt
```
**Jupyter notebooks**  
Run the following command in the main directory
```
jupyter notebooks
```
**Scraper**  
Scrape your own data with:
```
python scraper.py
```
Just comment the lines at the  bottom of 
[scraper.py](https://github.com/kael558/OSRSInvestor/blob/master/scraper.py) if you don't want to scrape from any source.

Run a [scraper.bat](https://github.com/kael558/OSRSInvestor/blob/master/scraper.bat) with windows scheduler. 

### File Manifest
**data folder** - Explanation of each file and the source of data. Prices for logs, ores, runes, seeds and XP data.
 * avg_price from (OOPA) - high and low price weighted with volume
 * fandom_data (FA) - latest item price from fandom api
 * high_price (OOPA) - avg instant buy price over an hour
 * high_vol (OOPA)- the volume of instant buys over an hour
 * low_price (OOPA) - avg instant sell price over an hour
 * low_vol (OOPA)- the volume of instant sell over an hour
 * xp_data (CML) - the xp gained by non-ironman accounts in a skill from the earliest data point and latest data point
   for a period of 24 hours. N.B. the player needs to actively click Update to create a data point.


### To do
* Automate scraper with [AWS Lambda](https://medium.com/@haldis444/use-lambda-to-append-daily-data-to-csv-file-in-s3-2c2813bc33d0)
* Switch to [Temple OSRS for XP](https://templeosrs.com/)
