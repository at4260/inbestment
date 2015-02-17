# Purpose: pulling API data into multiple data sets
# data set options: CSV, XML, JSON
# combine all stock ticker price data into one file and save into seed_date

# TO DO: successfully, pulls the data I want from the JSON file, need to save that data.. can either 1) directly session.commit it to the database (unscrubbed data) or 2) form a giant data file to then pull and scrub through for inputting into database?
import json, urllib

ticker_dict = ["MX_FB", "MX_COST"]

# queries the url using the desired ticker and token
url = "https://www.quandl.com/api/v1/datasets/YAHOO/"
token = open("../tokens.txt").read()
ticker_url = url + ticker_dict[0] + ".json?auth_token=" + token

# load the JSON data as a dictionary
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