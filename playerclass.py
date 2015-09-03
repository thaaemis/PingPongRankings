import time
from datetime import date

class player:
    def __init__(self, name,ind,mean,std,nmatch,lastplayed,nwins=0,nloss=0):
        self.name = str(name)
        self.ind = int(ind)
        self.mean = int(mean)
        self.std = float(std)
        self.nmatch = int(nmatch)
        self.nwins = int(nwins)
        self.nloss = int(nloss)
        self.prev = date.fromordinal(lastplayed)
        self.tmpMean = mean
        self.tmpStd = std
        self.newstats = [0, 0]
        self.match = []

    def __lt__(self,other):
        if self.mean == other.mean:
            return (self.std > other.std)
        return (self.mean < other.mean)
    
    def addmatch(self,oppind,date,W,L):
        matchind = -1
        for i in range(0,len(self.match)):
            if self.match[i].oppind == oppind and self.match[i].date == date:
                matchind = i
        if matchind == -1:
            self.match.append(match(oppind,date))
            matchind = len(self.match)-1
        self.match[matchind].add(W,L)

    def filtermatches(self,startdate,enddate):
        res = []
        for m in self.match:
            if m.date >= startdate and m.date <= enddate:
                res.append(m)
        self.match = res
        return res
    
    def sumMatches(self):
        datesInSet = set()
        for m in self.match:
            datesInSet.add(m.date)
            
        refDate = min(datesInSet)
        summedMatches = []
        oppinds = []
        ## this part needs fixing: if not everyone plays on refDate, there
        ## can be problems--this only shows up if doing weekly calculations
        for m in self.match:
            if m.date == refDate:
                summedMatches.append(match(m.oppind,refDate))
                oppinds.append(m.oppind)
        for m in self.match:
            addIndex = oppinds.index(m.oppind)
            summedMatches[addIndex].add(m.W, m.L)
        self.match = summedMatches
        

    def tmpRank(self,nowMean,nowStd):
        self.tmpMean = nowMean
        self.tmpStd = nowStd
        return [self.tmpMean, self.tmpStd]

    def stats(self):
        return [self.ind, self.mean, self.std, self.nmatch, self.prev]

    def newstats(self,newMean,newStd):
        self.newstats = [newMean,newStd]

    def printnice(self):
        res = ''
        print(self.name,end='')
        res += self.name
        for i in range(len(self.name),13):
            print(' ',end='')
            res += ' '
        print(int(self.mean),end='')
        res += str(int(self.mean))
        for i in range(len(str(int(self.mean))),8):
            print(' ',end='')
            res += ' '
        print(round(self.std),end='')
        res += str(round(self.std))
        for i in range(len(str(round(self.std))),6):
            print(' ',end='')
            res += ' '

        print(self.nwins,end='')
        res += str(round(self.nwins))
        for i in range(len(str(round(self.nwins))),7):
            print(' ',end='')
            res += ' '
        print(self.nloss,end='')
        res += str(round(self.nloss))
        for i in range(len(str(round(self.nloss))),7):
            print(' ',end='')
            res += ' '
        print(str(self.nwins+self.nloss),end='')
        for i in range(len(str(round(self.nwins + self.nloss))),7):
            print(' ',end='')
            res += ' '
        if self.nmatch < 5:
            print('P!',end='')
            res += 'P!'
        print('',end='\n')
        res += '\n'
        return res

class playerlist:
    def __init__(self):
        self.list = []
        self.n = 0

    def add(self,player):
        self.list.append(player)
        self.n += 1

    def find(self,ind):
        try:
            ind = int(ind)
            for pl in self.list:
                if pl.ind == ind:
                    return pl
            return None
        except ValueError:
            for pl in self.list:
                if pl.name == ind:
                    return pl
            return None

    def copynew(self):
        for pl in self.list:
            if pl.newstats != [0,0]:
                pl.mean = pl.newstats[0]
                pl.std = pl.newstats[1]

    def purge(self):
        purgedList = []
        for pl in self.list:
            if pl.nmatch > 0 or pl.nwins + pl.nloss > 0:
                purgedList.append(pl)
        self.list = purgedList

        
class match:
    def __init__(self,oppind,date):
        self.oppind = int(oppind)
        self.date = date
        self.W = 0
        self.L = 0

    def add(self,win,loss):
        self.W += int(win)
        self.L += int(loss)
    

class matchhistory:
    def __init__(self,date):
        self.date = date

    def addmatch(self,opp1,opp2,W,L):
        return None
        
