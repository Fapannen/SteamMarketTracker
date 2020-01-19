import requests
import time

debug = False

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
----------------------------------------------------
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
----------------------------------------------------
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
                initEntries.append(searchEntry)
            
    return initEntries

def findEntryByName(namee, entries):
    for entry in entries:
        if entry.name == namee:
            return entry

def keepTracking(items, entries):
    i = 0
    
    while True:
        if debug:
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
                        print("Value at item " + clone.name + " has changed!")
                        print("Previous price: " + str(clone.price))
                        print("New price: " + str(cmpPrice))
                        print("Price DECREASED") if clone.price > cmpPrice else print("Price INCREASED")
                        clone.price = cmpPrice
                        print("Value updated...")
                        print("-" * 50)
                        print()
        i += 1

def main():
    print("Welcome to Steam Market Item Tracker")
    print("Please enter name of the desired item. If you want to track more items, split them by '|' ")
    print("ie. 'Huntsman Blue|Ak Vulcan|AWP Hyper Beast' ")
    print()
    items = input('Name of searched Item - ')
    track = items.split('|')
    entries = getInitialEntries(track)
    for entry in entries:
        entry.printInfo()
        
    keepTracking(track, entries)

main()
