""" Pulls QUANDL API data. """

# FIXME: successfully, pulls the data I want from the JSON file, need to 
# directly session.commit it to the database (unscrubbed data) 

import json, urllib

# FIXME: need to input real tickers in ticker list
ticker_list = ["MX_FB", "MX_COST"]
ticker_url_list = []

def build_ticker_url(ticker_list):
	""" Queries the url using the desired ticker and token"""
	for ticker in ticker_list:
		url = "https://www.quandl.com/api/v1/datasets/YAHOO/"
		token = open("tokens.txt").read()
		ticker_url = url + ticker + ".json?auth_token=" + token
		ticker_url_list.append(ticker_url)
	return ticker_url_list


ticker_name_dict = {}

def get_ticker_names(ticker_url_list):
	for ticker_url in ticker_url_list:	
		u = urllib.urlopen(ticker_url)
		data = u.read()
		newdata = json.loads(data)

		# FIXME- "code" pulls the url query, not the actual symbol
		ticker_symbol = newdata["code"]
		ticker_name = newdata["name"]
		ticker_name_dict[ticker_symbol] = ticker_name
	return ticker_name_dict
		

ticker_prices_dict = {}
ticker_prices_masterdict = {}

def get_ticker_prices(ticker_url_list):
	for ticker_url in ticker_url_list:	
		u = urllib.urlopen(ticker_url)
		data = u.read()
		newdata = json.loads(data)

		ticker_symbol = newdata["code"]
		# prices pulls a list of lists (consisting of date, open, high, low, close, volume. adjusted close)
		prices = newdata["data"]

		# itierate over the list of lists to pull out date and close price
		for price in prices:
			date = price[0]
			close_price = price[4]
			ticker_prices_dict[date] = close_price
		ticker_prices_masterdict[ticker_symbol] = ticker_prices_dict
    	return ticker_prices_masterdict

def main():
	print get_ticker_names(build_ticker_url(ticker_list))

if __name__ == "__main__":
	main()
	