import requests
import pprint
from bs4 import BeautifulSoup

winner = "Null"

r = requests.get("http://www.datdota.com/match.php?q=2068547220&p=draft")
soup = BeautifulSoup(r.content, 'html.parser')


useful = False
for next in soup.find_all("td"):
	print next
	s = next.get_text()
	if useful == False:
		if s == "DIRE":
			winner = "DIRE"
		if s == "RADIANT":
			winner = "RADIANT"
	if s == "1":
		useful = True

print winner


# <th>Winner</th><th>Round</th><th>Game</th><th>Time</th><th>Score</th></tr>
# </thead> <tbody> <tr><td>1817107757</td><td>09/24/15</td><td>
# <a href="team.php?q=1118&amp;team=MFF">MFF</a></td><td>
# <a href="team.php?q=1412&amp;team=HR">HR</a></td><td>DIRE</td><td>
# Group Stage</td><td>2</td><td>50.32</td><td>20 - 30</td></tr></tbody> 
# </table> <br> </br></div></div></div>
