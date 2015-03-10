""" Holds all of the utility functions that are called in controller.py. """

import csv
import json 
import urllib 
import model
import time

from datetime import datetime
from model import session as m_session
from sqlalchemy.sql import text

def format_currency(value):
	return "${:,.2f}".format(value)

def format_percentage(value):
	return "{0:.0f}%".format(value * 100)

def calc_monthly_expense(income):
	""" 
	Calculate the user's monthly expense based on income.

	All budgets are expressed in decimals.
	"""
	housing_budget = 0.28
	misc_budget = 0.36
	cushion_budget = 0.10
	monthly_expenses = (income * (housing_budget + misc_budget + 
		cushion_budget)) / 12
	return monthly_expenses

def calc_max_checking(income):
	"""
	Calculates how much is needed in checking account based on 
	monthly expense.

	Checking needed is 1 month worth of monthly expenses.
	"""
	RATIO = 1
	return calc_monthly_expense(income) * RATIO

def calc_max_savings(income):
	"""
	Calculates how much is needed in savings account based on 
	monthly expense.

	Savings needed is 3 months worth of monthly expenses.
	"""
	RATIO = 3
	return calc_monthly_expense(income) * RATIO

def calc_user_checking(assets, income):
	"""
	Calculates how much the user will be able to put into 
	checking account based on assets.

	If assets less than max checking amount, still put all of
	the assets towards the account. Otherwise, put only up
	to the max checking amount.
	"""
	checking_needed = calc_max_checking(income)
	if assets <= checking_needed:
		return assets
	else: 
		return checking_needed

def calc_user_savings(assets, income):
	"""
	Calculates how much the user will be able to put into 
	savings	account based on assets.

	If assets less than max savings amount, still put all of
	the assets towards the account. Otherwise, put only up
	to the max savings amount.
	"""
	savings_needed = calc_max_savings(income)
	if assets <= savings_needed:
		return assets
	else: 
		return savings_needed

def calc_max_match(match_percent, match_salary, income):
	"""
	Calculates the max 401k match the user can contribute.

	"""
	match_needed = match_percent * match_salary * income
	return match_needed

def calc_user_match(assets, match_needed, comp_401k, match_401k):
	"""
	Calculates how much the user will be able to put into
	the 401k match based on assets.

	The match only applies if the user has a company 401k
	and the company offers a 401k match. If both of these
	scenarios are not met, then the user will not have a
	401k match.
	"""
	if comp_401k == "Yes" and match_401k == "Yes":
		if assets <= match_needed:
			return assets
		else:
			return match_needed	
	return 0

def calc_user_ira(assets):
	"""
	Calculates how much the user will put into their IRA 
	based on assets.

	IRS limits for the IRA is 5,500 per year.
	"""
	IRA = 5500
	if assets <= IRA:
		return assets
	else:
		return IRA

def calc_user_401k(assets, match_percent, match_salary, income, 
	comp_401k, match_401k):
	"""
	Calculates how much the user will put into their 401k 
	based on assets.

	IRS limits for the 401k is 18,000 per year minus any
	applicable 401k match contributions. 
	"""
	match_needed = calc_max_match(match_percent, match_salary, income)
	user_match = calc_user_match(assets, match_needed, comp_401k, 
		match_401k)

	max_401k = 18000 - user_match
	if comp_401k == "Yes":
		if assets <= max_401k:
			return assets
		else:
			return max_401k
	return 0

def calc_financial_results(assets, income, comp_401k, match_401k, 
	match_percent, match_salary):
	"""
	Calculates how much the user will be able to put into each type
	of account based on assets. 

	Calls all of the functions defined above. Returns a "results"
	dictionary with all of the accounts and amounts.
	"""
	results = {}
	# Setting all values to 0 in case a variable never gets updated 
	# (due to lack of assets).
	results["checking"] = 0
	results["savings"] = 0
	results["match"] = 0
	results["ira"] = 0
	results["ret401k"] = 0
 	results["investment"] = 0

 	monthly_expense = calc_monthly_expense(income)

 	results["checking"] = calc_user_checking(assets, income)
 	assets = assets - results["checking"]

 	results["savings"] = calc_user_savings(assets, income)
 	assets = assets - results["savings"]

 	match_needed = calc_max_match(match_percent, match_salary, income)
 	results["match"] = calc_user_match(assets, match_needed, 
 		comp_401k, match_401k)
 	assets = assets- results["match"]

 	results["ira"] = calc_user_ira(assets)
 	assets = assets - results["ira"]

 	results["ret401k"] = calc_user_401k(assets, match_percent, 
 		match_salary, income, comp_401k, match_401k)
 	assets = assets - results["ret401k"]

	results["investment"] = assets
	
	return results

def calc_max_financials(income, comp_401k, match_401k, 
	match_percent, match_salary):
	"""
	Calculates how much the user should be putting into each type
	of account.

	Calls all of the MAX functions defined above. Returns a "max_
	results" dictionary with all of the accounts and max amounts
	to feed onto the "results" page for semi-circle donut graphs.
	"""
	max_results = {}
 	monthly_expense = calc_monthly_expense(income)
 	max_results["checking"] = calc_max_checking(income)
	max_results["savings"] = calc_max_savings(income)
	max_results["ira"] = 5500

	if comp_401k == "Yes":
		if match_401k == "Yes":
			max_results["match"] = calc_max_match(match_percent, 
				match_salary, income)
		 	max_results["ret401k"] = 18000 - max_results["match"]
		else:
			max_results["match"] = 0
			max_results["ret401k"] = 18000
	else:
		max_results["match"] = 0
		max_results["ret401k"] = 0

	max_results["investment"] = 0
	
	return max_results

def generate_allocation_piechart(risk_prof):
	"""
	Queries for the ticker names and weights based on the
	user's risk profile and the profile's allocation.

	Returns a dictionary of dictionaries with "Stocks" and
	"Bonds" as the key with a value of ticker name as key
	and weight as value.
	"""
	chart_ticker_data = {}
	stock_data = {}
	bond_data = {}
	# Risk_prof.allocation is list of
	# <Risk Profile ID=2 Ticker ID=1 Ticker Weight=25>.			
	for prof_ticker in risk_prof.allocation:
		# Ticker_description is using the ticker relationship
		# to get the object <Ticker ID=6 Symbol=VWO 
		# Name=Vanguard FTSE Emerging Markets ETF (VWO)>.
		ticker_description = prof_ticker.ticker
		ticker_name = ticker_description.name
		ticker_weight = prof_ticker.ticker_weight_percent
		
		# Creates a stocks and bonds dictionary within the
		# chart_ticker_data dictionary.
		if ticker_description.category == "Stocks":
			stock_data[ticker_name] = ticker_weight
			chart_ticker_data["Stocks"] = stock_data
		else:
			bond_data[ticker_name] = ticker_weight
			chart_ticker_data["Bonds"] = bond_data

	return chart_ticker_data

def save_prof_tickers(risk_prof):
	"""
	Queries for the tickers that make up the user's selected
	risk profile allocation.
	"""
	prof_ticker_ids = []
	prof_ticker_names = []
	for prof_ticker in risk_prof.allocation:
		prof_ticker_ids.append(prof_ticker.ticker_id)
		prof_ticker_names.append(prof_ticker.ticker.name)

	prof_ticker_data = []
	prof_ticker_data.append(prof_ticker_ids)
	prof_ticker_data.append(prof_ticker_names)

	return prof_ticker_data

def generate_performance_linegraph(risk_prof):
	"""
	Pulls the performance data for the line graph showing 
	total performance.

	Queries the database for all price data	matching a specific date. 
	The data gets accumulated into a total using each ticker's 
	weighting in the user's risk profile allocation.
	"""
	connection = model.engine.connect()
	linegraph_sql_query = """ 
	SELECT date, sum(percent_change * prof_allocs.ticker_weight_percent)
	FROM prices 
	JOIN prof_allocs on (prices.ticker_id = prof_allocs.ticker_id)  
	WHERE prof_allocs.risk_profile_id == :sql_risk_prof
	AND prices.date > "2007-04-10"
	GROUP by prices.date
	ORDER by prices.date
	"""
	total_performance_result = connection.execute(text(linegraph_sql_query), sql_risk_prof 
		= risk_prof.id)
	
	dates = []
	total_performance = []

	for row in total_performance_result:
		dates.append(row[0])
		total_performance.append(row[1]/100)

	total_linegraph = []
	total_linegraph.append(dates)
	total_linegraph.append(total_performance)

	return total_linegraph

def generate_individual_ticker_linegraph(ticker_id):
	"""
	Pulls the performance data for the line graph showing
	individual fund performance.
	"""
	connection = model.engine.connect()
	linegraph_sql_query = """ 
	SELECT percent_change
	FROM prices 
	WHERE prices.ticker_id == :sql_ticker_id
	AND prices.date > "2007-04-10"
	ORDER by prices.date
	"""
	individual_performance_result = connection.execute(text(linegraph_sql_query), sql_ticker_id
		= ticker_id)
	
	individual_performance = []

	for row in individual_performance_result:
		individual_performance.append(row[0])

	return individual_performance

def find_ticker(compare_ticker, file_name):
	"""Searches through csv file to find ticker and corresponding 
	ticker url identifier.
	"""
	ticker_identifier_list = []
	filename = open(file_name)
	for line in filename:
		data = line.strip().split(",")
		if compare_ticker == data[0]:
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
	beginning = time.time()
	for ticker_url in ticker_url_list:	
		u = urllib.urlopen(ticker_url)
		print "@@@", time.time() - beginning
		data = u.read()
		print "###", time.time() - beginning
		newdata = json.loads(data)

		ticker_symbol = (newdata["code"].split("_"))[1]
		ticker_name = newdata["name"]
		new_ticker = model.Ticker(symbol=ticker_symbol, name=ticker_name)
		session.add(new_ticker)
		session.commit()
		
		prices = newdata["data"]
		for price in prices:
			date = price[0]
			date_format = datetime.strptime(date, "%Y-%m-%d")
			date_format = date_format.date()
			close_price = price[4]
			new_ticker_price = model.Price(ticker_id=new_ticker.id, date=date_format, 
				close_price=close_price)
			session.add(new_ticker_price)

	session.commit()

def calc_percent_change(compare_ticker, session):
	"""
	This function calculates the percent change since 4/10/2007 and saves
	that value to the new_change column in the database.

	All values are being benchmarked against 4/10/2007, which is the latest
	inception date for all of the funds for apples-to-apples since-inception
	comparison.
	"""
	ticker_id = model.session.query(model.Ticker).filter_by(symbol=
			compare_ticker).first().id
	ticker = model.session.query(model.Price).filter_by(ticker_id=
		ticker_id).all()

	new_index = 0
	old_close_price = model.session.query(model.Price).filter_by(date=
			"2007-04-10", ticker_id=ticker_id).first().close_price
	old_date = datetime.strptime("2007-04-10", "%Y-%m-%d").date()

	while ticker[new_index].date > old_date:
		new_close_price = ticker[new_index].close_price
		difference = round((new_close_price - old_close_price)/
			old_close_price, 4)
		new_change_id = ticker[new_index].id
		new_change = model.session.query(model.Price).filter_by(id=
			new_change_id).update({model.Price.percent_change: difference}) 
		new_index = new_index + 1
	session.commit()
