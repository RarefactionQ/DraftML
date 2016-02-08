import requests
import pprint
from datetime import date, timedelta
from bs4 import BeautifulSoup

MATCH_DRAFT_STARTDATE = date(2015,1,1)
MATCH_DRAFT_ENDDATE = date.today()

# def getMatchNum():

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
				f.write(s+",")

	f.write("\n")

f = open('draft.txt', 'r+')
match_numbers = get500Matches()
# match_numbers = getMatchNum()
for matchnum in match_numbers:
	print matchnum
	writeMatch(matchnum)




