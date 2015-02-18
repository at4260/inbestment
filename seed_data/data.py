""" Pulls QUANDL API data and populates database. """

# FIXME: successfully, pulls the data I want from the JSON file, need to 
# directly session.commit it to the database (unscrubbed data) 

import json, urllib

ticker_list = ["MX_FB", "MX_COST"]
ticker_url_list = []

def build_ticker_url(ticker_list):
	""" Queries the url using the desired ticker and token"""
	for ticker in ticker_list:
		url = "https://www.quandl.com/api/v1/datasets/YAHOO/"
		token = open("../tokens.txt").read()
		ticker_url = url + ticker + ".json?auth_token=" + token
		ticker_url_list.append(ticker_url)
	return ticker_url_list


def get_ticker_data(ticker_url_list):
	for ticker_url in ticker_url_list:	
		u = urllib.urlopen(ticker_url)
		data = u.read()
		newdata = json.loads(data)

		# FIXME- "code" pulls the url query, not the actual symbol
		ticker_symbol = newdata["code"]
		ticker_name = newdata["name"]
		print ticker_symbol
		print ticker_name

		# prices pulls a list of lists (consisting of date, open, high, low, close, volume. adjusted close)
		prices = newdata["data"]

		# itierate over the list of lists to pull out the individual list of date data
		for price in prices:
		    print price[0], ":", price[4]

def main():
	get_ticker_data(build_ticker_url(ticker_list))

if __name__ == "__main__":
	main()
	