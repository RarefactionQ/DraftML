import requests
import pprint
import dota2api
from bs4 import BeautifulSoup
import json

API_KEY_FILE = "apikey.txt"
OUTPUT_FILE = "rawmatches.txt"
NUM_MATCHES = 1

def get_raw_matches():
	f = open(API_KEY_FILE, 'r')
	api = dota2api.Initialise(f.read())
	matches = api.get_match_history_by_seq_num(matches_requested=NUM_MATCHES)
	# soup = json.loads(str(matches))
	pp = pprint.PrettyPrinter(depth=6)
	pp.pprint(matches)
    # for match in matches:
    #     if match[]

# radiant_win

get_raw_matches()