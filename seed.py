"""
Autoloads database with Quandl API data, risk profiles, profile
allocations, fake user profiles and banking information.
"""

import csv
import json
import model
import requests

from datetime import datetime, timedelta
from model import session as m_session
from sqlalchemy.sql import text

ticker_list = ["VV", "VB", "VEU", "BIV", "BSV", "VWO", "BND"]


def find_ticker(ticker_list, file_name):
	"""
	Searches through csv file to find ticker and corresponding
	ticker url identifier.
	"""
	ticker_identifier_list = []
	filename = open(file_name)
	for line in filename:
		data = line.strip().split(",")
		for ticker in ticker_list:
			if ticker == data[0]:
				ticker_identifier_list.append(data[1])
	return ticker_identifier_list


def build_ticker_url(ticker_identifier_list):
	"""
	Queries the url using the desired ticker identifier and token.

	Trims the data set by start date. All values are being benchmarked
	against 4/10/2007, which is the latest inception date for all of
	the funds for apples-to-apples since-inception comparison.
	"""
	ticker_url_list = []
	for ticker_identifier in ticker_identifier_list:
		url = "https://www.quandl.com/api/v1/datasets/"
		token = open("quandl_tokens.txt").read()
		ticker_url = url + ticker_identifier + \
			".json?trim_start=2007-04-10&auth_token=" + token
		ticker_url_list.append(ticker_url)
	return ticker_url_list


def load_ticker_data(ticker_url_list, session):
	"""
	This function loads the tickers table and the daily close prices
	for the prices table.

	Both pull data from the Quandl API as a JSON object.
	"""
	for ticker_url in ticker_url_list:
		u = requests.get(ticker_url)
		data = u.text
		newdata = json.loads(data)

		ticker_symbol = (newdata["code"].split("_"))[1]
		ticker_name = newdata["name"]
		ticker_description = newdata["description"]

		stock = "stock"
		bond = "bond"
		if stock in ticker_description:
			ticker_category = "Stocks"
		elif bond in ticker_description:
			ticker_category = "Bonds"
		else:
			ticker_category = ""

		# Create new instance of the Ticker class called new_ticker
		new_ticker = model.Ticker(symbol=ticker_symbol, 
					name=ticker_name, category=ticker_category)
		# Add each instance to session
		session.add(new_ticker)
		session.commit()

		# Prices pulls a list of lists (consisting of date, open, high,
		# low, close, volume. adjusted close).
		prices = newdata["data"]

		for price in prices:
			date = price[0]
			date_format = datetime.strptime(date, "%Y-%m-%d")
			date_format = date_format.date()
			close_price = price[4]
			new_ticker_price = model.Price(ticker_id=new_ticker.id, 
						date=date_format, close_price=close_price)
			session.add(new_ticker_price)

	# commit after all instances are added
	session.commit()


def calc_percent_change_all(ticker_list, session):
	"""
	This function calculates the percent change since 4/10/2007 for all
	loaded tickers and saves that value to the new_change column in the
	database.

	All values are being benchmarked against 4/10/2007, which is the latest
	inception date for all of the funds for apples-to-apples since-inception
	comparison.
	"""
	ticker_id = 0

	for ticker_data in range(len(ticker_list)):
		ticker_id = ticker_id + 1
		ticker = m_session.query(model.Price).filter_by(
					ticker_id=ticker_id).all()	

		old_close_price = m_session.query(model.Price).filter_by(
					date="2007-04-10", ticker_id=ticker_id).first().close_price
		new_index = 0

		for daily_ticker_price in ticker:
			new_close_price = ticker[new_index].close_price
			difference = round((new_close_price - old_close_price) / 
						old_close_price, 4)
			ticker[new_index].percent_change = difference
			new_index = new_index + 1
	session.commit()


def load_risk_profs(session):
	filename = open("./seed_data/risk_profiles.csv")
	for line in filename:
		name = line.strip()
		new_risk_profile = model.RiskProfile(name=name)
		session.add(new_risk_profile)
	session.commit()


def load_prof_allocs(session):
	filename = open("./seed_data/profile_allocations.csv")
	for line in filename:
		data = line.strip().split(",")
		risk_profile_id = data[0]
		symbol = data[1]
		ticker_weighting = data[2]

		ticker_id = m_session.query(model.Ticker).filter_by(
					symbol=symbol).first().id

		new_profile_allocation = model.ProfileAllocation(
					risk_profile_id=risk_profile_id, ticker_id=ticker_id,
					ticker_weight_percent=ticker_weighting)
		session.add(new_profile_allocation)
	session.commit()


def main(session):
	# load_ticker_data(build_ticker_url(find_ticker(ticker_list,
	# 			"seed_data/ETFs-GOOG.csv")), m_session)
	# load_ticker_category(m_session)
	calc_percent_change_all(ticker_list, m_session)
	# load_risk_profs(m_session)
	# load_prof_allocs(m_session)

if __name__ == "__main__":
	main(m_session)
