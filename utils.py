from model import session as m_session
import model
from datetime import datetime, timedelta
import time

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

	Returns a dictionary with ticker id as key and weight
	as the value.
	"""
	prof_ticker_data = {}
	for prof_ticker in risk_prof.allocation:
		prof_ticker_data[prof_ticker.ticker_id] = \
			prof_ticker.ticker_weight_percent
	return prof_ticker_data

def calc_first_date():
	"""
	This is the start date for all funds.
	"""
	first_date = datetime.strptime("2007-04-10", "%Y-%m-%d").date()
	return first_date

def calc_final_date():
	"""
	This is the final or most recent date for all funds.
	This date is the same for all of the tickers.
	"""
	final_date = m_session.query(model.Price).filter_by(id=1).first().date
	return final_date

def generate_performance_dates_linegraph(prof_ticker_data):
	"""
	Pulls all of the dates for the line graph showing performance.

	Keeping the dates and performance values in separate lists
	because a dictionary cannot keep the dates in order.
	"""
	dates = []
	first_date = calc_first_date()
	final_date = calc_final_date()

	# Deals with 2007-04-10 case where percent change is None
	# Str- changes datetime to a JSON serializable object
	dates.append(str(first_date))
	
	days_value = 0
	incrementing_date = first_date		
	
	while incrementing_date < final_date:
		days_value = days_value + 1	
		incrementing_date = first_date + timedelta(days=days_value)
		dates.append(str(incrementing_date))

	return dates

def generate_performance_total_linegraph(prof_ticker_data):
	"""
	Pulls the performance data for the line graph showing 
	performance.

	Keeping the dates and performance values in separate lists
	because a dictionary cannot keep the dates in order.

	Queries the database for all price data	matching a specific date. 
	The data gets accumulated into a total using each ticker's 
	weighting in the user's risk profile allocation.
	"""
	beginning = time.time()
	total_performance = []
	first_date = calc_first_date()
	final_date = calc_final_date()

	# Deals with 2007-04-10 case where percent change is None
	total_performance.append(0)
	
	days_value = 0
	incrementing_date = first_date		
	
	while incrementing_date < final_date:
		days_value = days_value + 1	
		incrementing_date = first_date + timedelta(days=days_value)
		# Checks for all Price instances that are part of the profile 
		# allocation and meets the date requirement.		
		matched_ticker_prices = m_session.query(model.Price).filter(
			model.Price.date==incrementing_date, model.Price.ticker_id
			.in_(prof_ticker_data.keys())).all()
		print time.time() - beginning

		matched_total_performance = 0
		for matched_ticker_price in matched_ticker_prices:
			matched_ticker_percent_change = matched_ticker_price.percent_change
			matched_ticker_id = matched_ticker_price.ticker_id
			matched_weighting = round(float(prof_ticker_data
				[matched_ticker_id])/100, 4)
			matched_ticker_performance = matched_ticker_percent_change \
				* matched_weighting
			matched_total_performance = matched_total_performance \
				+ matched_ticker_performance
		total_performance.append(round(matched_total_performance, 3))

	return total_performance


