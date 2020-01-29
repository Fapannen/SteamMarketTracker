import requests
import time
import datetime
from win10toast import ToastNotifier

DEBUG = True
LOG = True
LOG_DELIM = "#"
NOTIFICATIONS = False
APPID = 730 # Make sure only CSGO Items are accepted

"""
PARSERS
"""
def parseQuery(s):
    s.replace(" ",'+')
    return s

def parsePriceHelper(s):
    ret = ""
    for i in range(len(s)):
        if s[i] == '>':
            for j in range(len(s) - i):
                if s[i+j] == '<':
                    return ret
                elif s[i+j] == '>':
                    continue
                else:
                    ret += s[i+j]

def parsePrice(s):
    temp = parsePriceHelper(s)
    if ',' in temp:
        multiplier = float(temp.split(",")[0][-1])
        mult = multiplier * 1000
        price = float(temp.split(",")[1].split(" ")[0])
        return float(mult + price)
    return float(temp.split(" ")[0].replace('$', ""))
"""
-----------------------------------------------------------------------------------
"""

class SearchEntry:
    def __init__(self):
        self.name = ""
        self.price = None
        self.currency = "USD"
        self.median = None
        self.trend = None
        self.delimeter = "| "

    def printInfo(self):
        print("-" * 50)
        print(self.delimeter + "Name : " + self.name)
        print(self.delimeter + "Price : " + str(self.price))
        print(self.delimeter + "Currency : " + str(self.currency))
        print(self.delimeter + "Median : " + str(self.median))
        print(self.delimeter + "Trend: " + str(self.trend))
        print("-" * 50)
        print()

"""
----------------------------------------------------------------------------------
"""

def getUrlContent(item):
    URL = 'https://steamcommunity.com/market/search?q=' + parseQuery(item)
    r = requests.get(URL)
    return r.text

def getInitialEntries(items):
    initEntries = []
    for item in items:
        content = getUrlContent(item)
        for line in content.split("market_listing_row market_recent_listing_row market_listing_searchresult"):
            name = line.split("data-hash-name=")
            if len(name) > 1:
                searchEntry = SearchEntry()
                parsed_name = name[1].split(")")[0] + ")"
                searchEntry.name = str(parsed_name.replace('"', "").replace(">", ""))
                price = parsePrice(line.split("data-currency=")[1])
                searchEntry.price = price
                itemAppId = (name[0].split("data-appid=")[1].replace(" ", ""))
                if int(itemAppId.replace('"', '')) == APPID: # If from desired game
                    initEntries.append(searchEntry)
                
                
    return initEntries

def findEntryByName(namee, entries):
    for entry in entries:
        if entry.name == namee:
            return entry

def getItemsToTrack():
    items = []
    while True:
        param = input("Track this item: ")
        if param == '':
            break
        else:
            items.append(param)
    return items

def printEntries(ent):
    for entry in ent:
        entry.printInfo()

def keepTracking(items, entries, notify):
    i = 0
    if notify:
    	nManager = ToastNotifier()

    while True:
        if DEBUG:
            print("Debug keepTracking iterations : " + str(i))
        
        for item in items:
            time.sleep(60) # Steam delay
            content = getUrlContent(item)
            
            for line in content.split("market_listing_row market_recent_listing_row market_listing_searchresult"):
                name = line.split("data-hash-name=")
                if len(name) > 1:
                    parsed_name = name[1].split(")")[0] + ")"
                    cmpName = str(parsed_name.replace('"', "").replace(">", ""))
                    cmpPrice = parsePrice(line.split("data-currency=")[1])
                    clone = findEntryByName(cmpName, entries)
                    if clone.price != cmpPrice:
                        oldPrice = clone.price
                        print("Value at item " + clone.name + " has changed!")
                        print("Previous price: " + str(clone.price))
                        print("New price: " + str(cmpPrice))
                        print("Price DECREASED") if clone.price > cmpPrice else print("Price INCREASED")
                        clone.price = cmpPrice
                        print("Value updated...")
                        print("-" * 50)
                        print()

                        if notify:
                        	nManager.show_toast(cmpName, "New Price: " + str(cmpPrice) + " | Previous Price : " + str(oldPrice), threaded=True,
                                                    icon_path=None, duration=10)

                        if LOG:
                            with open("log.txt", 'a') as logfile:
                                name = clone.name
                                if '★' in name:
                                    name = name.replace("★ ", "") # Encoding conflicts

                                txt = name + LOG_DELIM + str(datetime.datetime.now()) + LOG_DELIM + str(clone.price) + "\n"
                                if DEBUG:
                                    print("Writing to logfile: " +txt)
                                logfile.write(txt)
        i += 1

def main():
    print("Welcome to Steam Market Item Tracker")
    print("Enter items you want to be tracked. Press Enter with blank input to end giving parameters and start tracking")
    print()
    it = getItemsToTrack()
    entries = getInitialEntries(it)
    printEntries(entries) 
    keepTracking(it, entries, NOTIFICATIONS)

main()
