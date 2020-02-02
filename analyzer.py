file = "log.txt"

class AnalyzeNode:
    def __init__(self, date, price):
        self.date = date
        self.price = price

    def printInfo(self):
        print(self.date)
        print(self.price)
        print()

def printNodeList(nodelist):
    for node in nodelist:
        node.printInfo()

def processFile(filepath, delim):
    entries = {}
    with open(filepath, 'r') as log:
        for line in log.readlines():
            content = line.split(delim)
            name = content[0]
            date = content[1]
            price = float(content[2])
            node = AnalyzeNode(date, price)
            if name not in entries:
                entries[name] = [node]
            else:
                entries[name].append(node)
    return entries

def summary(entries):
    for entry in entries:
        print(entry + " has got " + str(len(entries[entry])) + " records.")

def analyze():
    entries = processFile(file, "#")
    summary(entries)
    
analyze()
