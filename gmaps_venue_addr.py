import googlemaps
import pandas as pd
import json
from datetime import datetime
import time

gmaps = googlemaps.Client(key='AIzaSyCsJnOb6VESNe9C-BXpkbrLppPA2ygCJMg')

venue_data = json.load(open("aus_sports_venue_data_15H49M.json","r"))

print("total venues: {}\nworking...".format(len(venue_data)))

def find_venue_details(venue_description_string):

	try:
		top_search_res = gmaps.geocode(venue_description_string)[0]  # take the top search result only
	except:  # if got not response at all
		print("failed!")
		return (None, {'lat': None, 'lng': None}, None)
	# if the response is not empty
	if top_search_res:

		try:
			address = top_search_res["formatted_address"]
		except:
			address = None
		try:
			coordinates = top_search_res["geometry"]["location"]
		except:
			coordinates = {'lat': None, 'lng': None}
		try:
			place_id = top_search_res["place_id"]
		except:
			place_id = None
	else:
		address = place_id = None
		coordinates = {'lat': None, 'lng': None}

	time.sleep(1)

	return (address, coordinates, place_id)

def clean_string(st):

	return("".join([ch for ch in st if (ch.isalnum() or (ch == " "))]))

if __name__ == "__main__":

	for i, v in enumerate(venue_data):

		if venue_data[v]["location"]:
			lok = venue_data[v]["location"]
		else:
			lok = ""
		search_string = clean_string(v + " " + lok)
		address, coordinates, place_id = find_venue_details(search_string)

		# update the dictionary
		venue_data[v].update({
			"gmaps_address": address.lower() if address else None,
			"coordinates": coordinates,
			"gmaps_id": place_id
			})
		print("venue {}/{}...".format(i+1, len(venue_data)))

	print("ok")
	t_now = datetime.now()
	timestamp = "_{:02.0f}H{:02.0f}M".format(t_now.hour, t_now.minute)
	json.dump(venue_data, open("aus_sports_venue_data" + timestamp + ".json", "w"), sort_keys=False, indent=4)

