-- Ping Pong Algorithm Instructions --
Brian Kraus, September 2015

This code is not perfect, but it does rank ping-pong players by ability in
a satisfactory manner. To run the code:

	1  set path of Ping Pong folder in line 4 of pingpong.py: "pingpongpath = ..."
	2  create folder Archive: ping/pong/path/..../Archive/
	3  install python3.4
	4  go to the command line
	5  travel to the PingPong directory: >> cd file/structure/
	6  enter >> python3.4 pingpong.py
	7  follow instructions to calculate rankings.

This code should be portable enough to work, though you may have to download
a few Python libraries to get it to run. 

You will have to set up an online interface to enter scores:

-- Option 1 -- Instructions for creation of google form:

go to drive.google.com , log in to google account and navigate to
"Create Form"
You should make a form for people to enter scores into. Order of questions
should lead to columns in spreadsheet: (Timestamp) Player Opponent Wins Losses
Navigate to File -> Publish to the web, and choose "Entire Document, .csv"
Publish to obtain link directly to .CSV download.

Finally, open "pingpong.py", and find line 12: "url = '....'"
Replace "..." with "yourformURL.csv"

-- Option 2 -- Manual entry

Type the matches yourself into the file 'latestMatchList.txt'. For example:

	match_index    date(yyyy-mm-dd)    Player1   Wins1    Player2    Wins2
	1              2015-08-07          Brian     3        Gabe       1

You will have to comment out line 12 in "pingpong.py": " # digest(url) "
