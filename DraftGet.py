import requests
import pprint
from datetime import date, timedelta
from bs4 import BeautifulSoup

MATCH_DRAFT_STARTDATE = date(2016,1,20)
MATCH_DRAFT_ENDDATE = date.today()
DERP = 0

def getMatchNum():
	urls = []
	match_numbers = []
	day = MATCH_DRAFT_ENDDATE
	while day >= MATCH_DRAFT_STARTDATE:
		iso_date = day.isoformat().split("-") # YYYY - MM - DD
		urls.append("http://www.datdota.com/match_finder.php?hero=&player=&side=0&patch=0&season=0&event=&team=&prize=0&region=0&team_opp=&in_wins=0&match_time=0&item=&hero2=&hero3=&day_after="+iso_date[2]+"&month_after="+iso_date[1]+"&year_after="+iso_date[0]+"&day_before="+iso_date[2]+"&month_before="+iso_date[1]+"&year_before="+iso_date[0])
		day = day - timedelta(days = 1)
	print len(urls)
	for url in urls:
		matches = requests.get(url)
		new_soup = BeautifulSoup(matches.content, 'html.parser')
		for next in new_soup.find_all("a"):
			mnumber = str(next.get_text())
			if mnumber.isdigit():
				match_numbers.append(mnumber)
	return match_numbers

def get500Matches():
	matches = requests.get("http://www.datdota.com/matches.php")
	new_soup = BeautifulSoup(matches.content, 'html.parser')
	match_numbers = []
	for next in new_soup.find_all("a"):
		# print next.get_text()
		mnumber = str(next.get_text())
		if mnumber.isdigit():
			match_numbers.append(mnumber)
	return match_numbers

def writeMatch(matchnum):
	global DERP
	if matchnum < 10000: #throwing out malformed game ids
		return
	winner = "Unknown"
	r = requests.get("http://www.datdota.com/match.php?q="+matchnum+"&p=draft")
	soup = BeautifulSoup(r.content, 'html.parser')
	useful = False
	for next in soup.find_all("td"):
		s = next.get_text()
		if useful == False:
			if s == "DIRE":
				winner = "Dire"
				f.write("0,")
			if s == "RADIANT":
				winner = "Radiant"
				f.write("1,")
		if useful == False and s == "Ban":
			useful = True
			f.write("1,")
		if useful:
			# print s
			if s != "":
				if "\n" in s:
					continue
				if "Unknown".lower() in s.lower():
					DERP+=1
					print str(DERP)
					f.write("derp "+str(DERP)+",")
					continue
				f.write(s+",")

	f.write("\n")

f = open('draft.txt', 'r+')
# match_numbers = get500Matches()
match_numbers = getMatchNum()
print len(match_numbers)
for matchnum in match_numbers:
	print matchnum
	if matchnum > 10000:
		writeMatch(matchnum)




