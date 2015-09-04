import time,math,sys,re
from datetime import date,timedelta
from playerclass import player,playerlist,match
#import matplotlib.pyplot as plt
from digestleague import digest, getPlayerFile

pingpongpath = 'C:/Users/bkraus/Documents/GitHub/PingPongRankings/'
def main(startdate,enddate,writevar=False,path=pingpongpath):

    # digest() retrieves .csv from google with latest matches
    # !!!       modify URL as noted in setup.txt         !!!!
    url = 'https://docs.google.com/spreadsheets/d/1bSgLACFSFCHh0e82Qb-u-Z2vGrAqhX586QGEAbdW3Ys/pub?gid=98643558&single=true&output=csv'
    digest(url,pingpongpath)

    # only calculate for matches on or before rundate
    rundate = enddate

    # basic definitions: 
    # establish gaussian, probability, and (0,3600) basis

    basis = range(0,3610,10)

    def gaussval(x,mu,sigma):
        if sigma == 0:
            sigma = 0.001
        return 1/(sigma*math.sqrt(2*3.14159))*math.exp(-0.5*(x-mu)**2/sigma**2)

    def gaussian(mu,sigma,x=basis):
        res = []
        for val in x:
            res.append(gaussval(val,mu,sigma)*10)
        return res
            
    def prob(diff):
        alpha = 0.0148540595817432
        return (1+math.exp(alpha*diff))**-1

    # T for temporal delay, update for the main ranking algorithm
    def T(x,d):
        return gaussval(x,0,d*70/math.sqrt(365))

    def update(law,opplaw,match):
        newlaw = [0]*361
        for p in basis:
            for q in basis:
                newlaw[int(p/10)] += prob(q-p)**match.W * \
                                    prob(p-q)**match.L * \
                                    law[int(p/10)] * \
                                    opplaw[int(q/10)]
        # normalize
        norm = sum(newlaw)
        result = [x / norm for x in newlaw]
        return result

    # Define path and filenames for reference / saving
    playerfile = 'players.txt'
    with open(path+playerfile,'r') as f:
        data = f.read()

    # all players kept in playerlist object
    players = playerlist()

    # process players from players.txt, append new player objects to list
    numplayers = data.count('\n')
    for i in range(0,numplayers):
        newstr = data[0:data.find('\n')]
        data = data[data.find('\n')+1:]
        attrib = newstr.split(' ')
        nwins = attrib[5]
        nloss = attrib[6]
        prev = attrib[7].split('-')
        prev = date(int(prev[0]),int(prev[1]),int(prev[2]))
        prev = prev.toordinal()
        players.add(player(attrib[0],attrib[1],attrib[2],attrib[3],
                           attrib[4],prev,nwins,nloss))

    # digest() put new matches into matchfile, now interpret
    # them and attach them to players' associated matchlist
    matchfile = 'latestMatchList.txt'
    usedata = ''
    remdata = ''
    datebasket = set()

    with open(path+matchfile,'r') as f:
        data = f.read()

    with open(path+matchfile,'r') as f:
        for newstr in f:
            attrib = re.split(' +',newstr)
            nowdate = attrib[1]
            nowdate = time.strptime(nowdate,'%Y-%m-%d')
            nowdate = date(nowdate[0],nowdate[1],nowdate[2])
            datebasket.add(nowdate)
            
            pl1 = players.find(attrib[2])
            pl2 = players.find(attrib[4])
            
            # create new player if pl1, pl2 not in list already
            if pl1 == None:    
                players.add(player(attrib[2],players.n+1,1400,450,0,nowdate.toordinal(),0,0))
                pl1 = players.find(attrib[2])
            if pl2 == None:
                players.add(player(attrib[4],players.n+1,1400,450,0,nowdate.toordinal(),0,0))
                pl2 = players.find(attrib[4])
        
            # add matches now that all players exist
            pl1.addmatch(pl2.ind,nowdate,attrib[3],attrib[5])
            pl2.addmatch(pl1.ind,nowdate,attrib[5],attrib[3])

            usedata += newstr

##    if writevar:
##        with open(path+'/Archive/'+rundate.isoformat()+'_matches.txt','w') as f:
##            f.write(usedata)

    for plind in range(1,players.n+1):
        pl = players.find(plind)
        #filter matches based on calculation window
        if pl != None:
            lastMatchOn = max([x.date for x in pl.match])
            firstMatchOn = min([x.date for x in pl.match])
            pl.filtermatches(startdate,enddate)
            if len(pl.match) > 0:
                pl.sumMatches()

    # Establish initial laws for today's players
    for plind in range(1,players.n+1):
        pl = players.find(plind)
    
        if pl != None and len(pl.match)>0: #did player play today?
            # set up temporal delay and new rankings
            if [pl.mean,pl.std] != [1400,450]:
                delay = rundate - pl.prev 
                d = delay.days
                F = gaussian(pl.mean,pl.std)
                B = [0]*361
                for x in basis:
                    for y in range(-3600,-x+10,10):
                        B[0] += T(y,d)*F[int(x/10)]
                    for y in range(3600-x,3610,10):
                        B[360] += T(y,d)*F[int(x/10)]
                    for r in range(1,360):
                        B[r] += T(r*10-x,d)*F[int(x/10)]
                pl.law1 = B
            else:
                pl.law1 = gaussian(pl.mean,pl.std)

    # Iterate to get new ratings for each player
    for plind in range(1,players.n+1):
        pl = players.find(plind)
        try:
            pl.law2 = pl.law1
            print(pl.name,'played:')
            for match in pl.match: # 1st level
                opp = players.find(match.oppind)
                opp.law2 = opp.law1
                for match2 in players.find(opp.name).match: # 2nd level
                    opp2 = players.find(match2.oppind)
                    if opp2 != pl:
                        opp.law2 = update(opp.law2,opp2.law1,match2)
                pl.law2 = update(pl.law2,opp.law2,match)
                pl.nmatch += match.W + match.L
                pl.nwins += match.W
                pl.nloss += match.L
                pl.prev = max(match.date,pl.prev)
                print('----  ',opp.name,', won ',match.W,', lost ',
                      match.L,', on ',match.date,sep='')
                        
            newmean = basis[pl.law2.index(max(pl.law2))]
            newstd = (math.sqrt(2*3.1415927)*max(pl.law2))**-1*10
            pl.newstats = [newmean,round(newstd)]
            # plt.plot(basis,pl.law1,'r',basis,pl.law2,'g',basis,gaussian(newmean,newstd))
            # plt.show()
            print('--  ',pl.name,': Went from (',pl.mean,',',int(pl.std),
                  ') to (',pl.newstats[0],',',pl.newstats[1],')\n',sep='')
            
        except AttributeError:
            try:
                print(pl.name,'didn\'t play this time \n')
            except AttributeError:
                print('skipped')

    # this copies calculated mean/std to main player stats and sorts
    # list by mean ranking
    players.copynew()
    players.list.sort(reverse=True)

    players.purge()
    
    print('#    Name         Rank    Err   W      L      Total  Provisional? \n')
    # file output to archive, players.txt for next time
    pltxt = ''
    for i in range(0,len(players.list)):
        print(i+1,'  ',end='')
        pltxt += str(i+1)+'  '
        if i+1 <= 9:
            print(' ',end='')
            pltxt += ' '
        pltxt += players.list[i].printnice()

    if writevar:
        with open(path+'/Archive/'+rundate.isoformat()+'_players.txt','w') as f:
            f.write(pltxt)
            
        with open(path+'players.txt','w') as f:
            for pl in players.list:
                f.write(pl.name + ' ')
                f.write(str(pl.ind) + ' ')
                f.write(str(pl.mean) + ' ')
                f.write(str(round(pl.std)) + ' ')
                f.write(str(pl.nmatch) + ' ')
                f.write(str(pl.nwins) + ' ')
                f.write(str(pl.nloss) + ' ')
                f.write(pl.prev.isoformat()+'\n')

        with open(path+'/Archive/'+rundate.isoformat()+'_data.txt','w') as f:
            for pl in players.list:
                f.write(pl.name + ' ')
                f.write(str(pl.ind) + ' ')
                f.write(str(pl.mean) + ' ')
                f.write(str(round(pl.std)) + ' ')
                f.write(str(pl.nmatch) + ' ')
                f.write(str(pl.nwins) + ' ')
                f.write(str(pl.nloss) + ' ')
                f.write(pl.prev.isoformat()+'\n')

def init():
    startdate = input('Calculate scores from start date: [mm dd YY]   ')
    if startdate != '':
        while True:    
            try:
                startdate = startdate.split(' ')    
                startMonth, startDay, startYear = [int(x) for x in startdate]
                startdate = date(2000 + startYear, startMonth, startDay)
                break
            except ValueError:
                startdate = input("Input must be 'mm dd YY' format to continue   ")
    else:
        startdate = date(2015,7,20)
    
    enddate = input('Use matches before (NOT INCLUDING) end date: [mm dd YY]   ')
    if enddate != '':
        while True:
            try:    
                enddate = enddate.split(' ')    
                endMonth, endDay, endYear = [int(x) for x in enddate]
                enddate = date(2000 + endYear, endMonth, endDay)
                break
            except ValueError:
                enddate = input("Input must be 'mm dd YY' format to continue   ")
    else:
        enddate = date.today()    

    rewrite = input('Rewrite all archive files? y/n:   ')
    if rewrite != '':
        while True:    
            if rewrite == 'y' or rewrite == 'Y' or rewrite == 'yes' or rewrite == '1':
                rewrite = True
                break
            elif rewrite == 'n' or rewrite == 'N' or rewrite == 'no' or rewrite == '0':
                rewrite = False
                break
            else:
                rewrite = input("Enter 'y' or 'n': rewrite all archive files?  ")
    else:
        rewrite = True

    print(rewrite)
##    daysInTournament = input('How many days constitute a tournament? (7, 1, ...)   ')
##    if daysInTournament != '':
##        while True:
##            try:
##                daysInTournament = abs(int(daysInTournament))
##                if daysInTournament == 0:
##                    daysinTournament = 1
##                break
##            except ValueError:
##                daysInTournament = input('Input an integer.   ')
##    else:
##            daysInTournament = 7

    daysInTournament = 1
    getPlayerFile(startdate,pingpongpath)

    for i in range(startdate.toordinal(),enddate.toordinal(),daysInTournament):
        tmpStart = i
        tmpEnd = i + daysInTournament - 1
        main(date.fromordinal(tmpStart), date.fromordinal(tmpEnd), rewrite)
    
        
    


init()
