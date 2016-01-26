import requests
import pprint
from bs4 import BeautifulSoup

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

pp = pprint.PrettyPrinter(indent=4)
matches = requests.get("http://www.datdota.com/matches.php")
# print r.text
# print "*************"
# print r.json()
# s = pp.pprint(r.content)

f = open('draft.txt', 'r+')
# f.write(r.content)

new_soup = BeautifulSoup(matches.content, 'html.parser')
# pp.pprint(new_soup)

# print(soup.prettify())
# print "*********************"
# pp.pprint(soup.find_all("td"))

# <td>1</td>, <- Position
# <td>Ban</td>, <- Pick/Ban
# <td><img alt="rubick" src="images/small_heroes/rubick.png"/></td>, <- nothing
# <td><a href="hero.php?q=Rubick">Rubick</a></td>, <- Hero again
# <td><a href="team.php?q=1971&amp;team=PRIES 2">PRIES 2</a></td>, <- Team
# <td>Radiant</td> <- Side


# http://www.datdota.com/match_finder.php?hero=&player=&side=0&patch=14&season=0&event=&team=&prize=0&region=0&team_opp=&in_wins=0&match_time=0&item=&hero2=&hero3=&day_after=&month_after=&year_after=&day_before=&month_before=&year_before=
# http://www.datdota.com/match_finder.php?hero=&player=&side=0&patch=14&season=0&event=&team=&prize=0&region=0&team_opp=&in_wins=0&match_time=0&item=&hero2=&hero3=&day_after=01&month_after=01&year_after=2016&day_before=10&month_before=01&year_before=2016


match_numbers = []
for next in new_soup.find_all("a"):
	# print next.get_text()
	mnumber = str(next.get_text())
	if mnumber.isdigit():
		match_numbers.append(mnumber)

print len(match_numbers)
for matchnum in match_numbers:
	print matchnum
	writeMatch(matchnum)


