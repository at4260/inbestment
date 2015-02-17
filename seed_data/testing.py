ticker_dict = ["MX_FB", "MX_COST"]

FB_url = "https://www.quandl.com/api/v1/datasets/YAHOO/"

token = open("../tokens.txt").read()
url = FB_url + ticker_dict[0] + ".json?auth_token=" + token
print url