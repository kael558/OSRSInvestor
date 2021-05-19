### Project Outline
Using [Crystal Math Labs (CML)](http://www.crystalmathlabs.com/tracker/) xp tracker 
and [OSRS's official Prices API](https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices)
we will conquer the ever volatile GE and make that dough.

### Acknowledgements
[Chronic Coder's GE Prediction Repo](https://github.com/chriskok/GEPrediction-OSRS) 
for the baseline of this project

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
It currently collects XP data, [prices from fandoms' API](https://runescape.fandom.com/wiki/Application_programming_interface)
(FA), and prices from OSRS's official Prices API (OOPA). 

I'm collecting data from fandoms' API just to see how accurate it  is compared to OOPA.

Just comment the lines at the  bottom of 
[scraper.py](https://github.com/kael558/OSRSInvestor/blob/master/scraper.py) if you don't want to scrape from any source.

Run a [scraper.bat](https://github.com/kael558/OSRSInvestor/blob/master/scraper.bat) with windows scheduler 
if you're using windows. 

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
* CML has a total gains endpoint that isn't listed in the API documentation. |
Make scraper.py much simpler by just querying that. For e.g. (https://www.crystalmathlabs.com/tracker/api.php?type=totalgains&skill=attack)
* Scrape boss KC data from all non-ironman tracked accounts. No boss KC aggregrate endpoint. Not even sure where 
  the player specific boss KC endpoint is.
