## Project Outline
Old-School Runescape (OSRS) is a RPG based game where players may level up their skills by gaining 
experience (XP) and items at the same time. The game also contains a Grand Exchange (GE) that allows 
players to sell and buy items at a price of their choosing. 

The goal of this project is to use multivariate time series analysis to predict future prices based on 
daily XP gained and previous item prices.

For example, a player chopping logs will gain experience and logs. 
They have gained woodcutting XP and then may sell the logs. 
This will increase the supply and lower the price. 
So if the woodcutting XP gained is significant, then this would be a good time to buy logs.

### Data
The data is collected from 3 sources:
- XP data from [Crystal Math Labs (CML)](http://www.crystalmathlabs.com/tracker/). CML is an unofficial website where players independently sign up for their XP to be tracked.
- prices from [OSRS's official Prices API (OOPA)](https://oldschool.runescape.wiki/w/RuneScape:Real-time_Prices).
- prices from [fandoms' API (FA)](https://runescape.fandom.com/wiki/Application_programming_interface). Unofficial data collected for comparison against official prices.

### Problems & Solutions
There are problems with such an analysis:
 - Players may wait variable amounts of time before selling their obtained items.
 - Hardcore players may drop their items instead of selling (as they do not have access to the GE).
 - Bots that harvest and sell vast amounts of items (thereby lowering prices) will be untracked by the XP tracker.

Some potential solutions to these problems are:
 - Determining if there is a time period that players wait.
 - Identifying particular skills where botting and hardcore players are less impactful.

## Acknowledgements
[Chronic Coder's GE Prediction Repo](https://github.com/chriskok/GEPrediction-OSRS) for the baseline of this project.

## Configuration
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

Alternatively, you can run the scraper daily with the lambda-scraper.py file using AWS.
Here is a [post](https://www.linkedin.com/posts/rahelgunaratne_scraping-aws-cloud-activity-6991068904793980928-qH22?utm_source=share&utm_medium=member_desktop) that can help you set it up.

## File Manifest
 * data folder - All the data to be used in the project.
 * Items folder (OOPA) - Contains all the items that have been scraped in 24h intervals since 20th Sept 2022.
 * XP_Data (CML) - the xp gained by non-ironman accounts in a skill from the earliest data point and latest data point
   for a period of 24 hours. N.B. the player needs to actively click Update to create a data point.


## To do
* Change to cmd line arguments for running the scraper
* Collect more data
* Time series analysis
