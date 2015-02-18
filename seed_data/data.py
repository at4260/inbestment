""" Pulls QUANDL API data and populates database. """

# FIXME: successfully, pulls the data I want from the JSON file, need to 
# directly session.commit it to the database (unscrubbed data) 

import json, urllib

def build_ticker_url(ticker):
	""" Queries the url using the desired ticker and token"""
	url = "https://www.quandl.com/api/v1/datasets/YAHOO/"
	token = open("../tokens.txt").read()
	ticker_url = url + ticker + ".json?auth_token=" + token
	return ticker_url


def get_ticker_data(ticker_url):	
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

def get_tickers():
	"""	This returns a static list of tickers.
	In the future this should read the list of existing tickers from the database. """
	return ["MX_FB", "MX_COST"]

def main():
	for ticker in get_tickers():
		return get_ticker_data(build_ticker_url(ticker))

if __name__ == "__main__":
	main()
	