import requests
import re
from bs4 import BeautifulSoup
from collections import defaultdict
import json
import time
import random
from datetime import datetime

start_pg = "http://www.austadiums.com/stadiums"

venue_dict = defaultdict()

r = requests.get(start_pg).text  # response body as bytes so need get text first
soup = BeautifulSoup(r, "lxml")

hdr_row = soup.find("a", href=re.compile("sort=name")).parent.parent.parent.parent

# print("total siblings: {}".format(len(hdr_row.find_next_siblings("tr"))))
for tr_sib in hdr_row.find_next_siblings("tr"):
#	print("found {} tds".format(len(tr_sib.find_all("td"))))
	for i, td in enumerate(tr_sib.find_all("td")):
		if i == 0:
			name = td.text.strip().lower()
			url = "/".join([start_pg, td.find("a")["href"]])
		elif i == 1:
			sta = td.text.strip().lower()
		elif i == 2:
			city = td.text.strip().lower()
		elif i == 3:
			capac = td.text.strip().lower()
		elif i == 4:
			when_upd = td.text.strip().lower()
	# put these into dict
	venue_dict[name] = {
		"url": url,
		"state": sta,
		"city": city,
		"capacity": capac,
		"when_upd": when_upd
	}
# start visiting venue pages
shuff_ven_list = list(venue_dict.keys())
random.shuffle(shuff_ven_list)

print("collecting data for {} sports venues...".format(len(shuff_ven_list)), end="")

for venue_name in shuff_ven_list:

	print("venue=",venue_name)

	r = requests.get(venue_dict[venue_name]["url"]).text
	v_soup = BeautifulSoup(r, "lxml")

	# find the summary table
	v_rbl = v_soup.find("table", id="table7")

	for i, row in enumerate(v_rbl.find_all("tr")):
		for j, td in enumerate(row.find_all("td")):
			if i == 0:  # location
				if j == 1:
					try:
						locat = td.text.strip().lower()
					except:
						locat = None
					#print("location=",locat)
				elif j == 3:
					try:
						addr = td.text.strip().lower()
					except:
						addr = None
					#print("addr=",addr)
			elif i == 1:  # capacity
				if j == 3:
					try:
						seats = td.text.strip().lower()
					except:
						seats = None
					#print("seats=",seats)
			elif i == 3:  # lights
				if j == 1:
					try:
						lights = td.text.strip().lower()
					except:
						lights = None
					#print("lights? ",lights)
				elif j == 3:
					try:
						roof = td.text.strip().lower()
					except:
						roof = None
					#print("roof=",roof)
			elif i == 4:  # screen
				if j == 1:
					try:
						screen = td.text.strip().lower()
					except:
						screen = None
					#print("screen? ",screen)
				elif j == 3:
					try:
						dimens = td.text.strip().lower()
					except:
						dimens = None
					#print("dim=",dimens)
			elif i == 5:
				if j == 1:
					try:
						built = td.text.strip().lower()
					except:
						built = None
					#print("built? ",built)
				elif j == 3:
					try:
						redev = td.text.strip().lower()
					except:
						redev = None
					#print("redev=",redev)
			elif i == 6:
				if j == 1:
					try:
						names = td.text.strip().lower()
					except:
						names = None
					#print("names? ",names)
				elif j == 3:
					try:
						ticketer = td.text.strip().lower()
					except:
						ticketer = None
					#print("ticketer=",ticketer)
			elif i == 7:
				if j == 1:
					try:
						sprts = td.text.strip().lower()
					except:
						sprts = None
					#print("sprts? ",sprts)
				elif j == 3:
					try:
						timz = td.text.strip().lower()
					except:
						timz = None
					#print("timz=",timz)

	venue_dict[venue_name].update({
		"location": locat,
		"address": addr,
		"seats": {"number": seats.split("(")[0].strip() if seats else None,
					"pct_of_capacity": seats.split("%")[0].split("(")[1] if seats else None
					},
		"lights": lights,
		"screen": screen,
		"year_built": built,
		"year_redeveloped": redev,
		"other_names": names,
		"ticketed_by": ticketer,
		"sports": sprts,
		"home_teams": timz
		})

	time.sleep(random.randint(1,4))

print("ok")

t_now = datetime.now()
timestamp = "_{:02.0f}H{:02.0f}M".format(t_now.hour, t_now.minute)

json.dump(venue_dict, open("aus_sports_venue_data" + timestamp + ".json", "w"), sort_keys=False, indent=4)





#pprint.pprint(venue_dict)
