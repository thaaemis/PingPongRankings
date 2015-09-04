import re,time,os
from datetime import date
import urllib.request

def digest(url,path):
    # Download latest scores
    response = urllib.request.urlopen(url)
    html = response.read()
    data = str(html)[1:-1]
    entries = data.split('\\r\\n')

    outpath = 'latestMatchList.txt'
    def print2(string,cleanfile,out=outpath,prtfile = True):
        with open(out,cleanfile) as f:
            f.write(string)
        return None
           
    for i in range(1,len(entries)):
        matchdata = entries[i].split(',')
        datedata = matchdata[0]
        pl1 = matchdata[1]
        pl2 = matchdata[2]
        win1 = matchdata[3]
        win2 = matchdata[4]

        timeval = time.strptime(datedata,'%m/%d/%Y %H:%M:%S')
        dateval = date(timeval[0],timeval[1],timeval[2])
        
        cleanfile = 'w' if i == 1 else 'a'
        if i < 10:
            spacer = '   '
        elif i < 100:
            spacer = '  '
        else:
            spacer = ' '
        spacer1 = ' '*(12-len(pl1))
        spacer2 = ' '*(3-len(win1))
        spacer3 = ' '*(12-len(pl2))
        spacer4 = ' '*(3-len(win2))

        print2(str(i)+'  '+spacer,cleanfile)
        print2(dateval.isoformat()+'  '+str(pl1)+spacer1 + \
                str(win1)+spacer2+str(pl2)+spacer3+str(win2)+'\n','a')

# saves last applicable player datafile to players.txt in main directory
def getPlayerFile(startdate,path):
    archiveFiles = os.listdir(path+'/Archive')
    datesSaved = []
    for x in archiveFiles:
        if x[-8:] == 'data.txt':
            datestr= x[:10]
            [year, month, day] = datestr.split('-')
            datesSaved.append(date(int(year),int(month),int(day)))
    datesSaved.sort()
    if len(datesSaved) == 0 or startdate < min(datesSaved):
        saveStr = ''
    else:
        recentInds = [ i-1 for i,date in enumerate(datesSaved) if date>=startdate ]
        recentInd = -1 if len(recentInds) == 0 else recentInds[0]
        fileToRetrieve = 'Archive/'+datesSaved[recentInd].isoformat()+'_data.txt'
        with open(path+fileToRetrieve,'r') as f:
            saveStr = f.read()
    with open(path+'players.txt','w') as f:
        f.write(saveStr)
    return None    
    
            

