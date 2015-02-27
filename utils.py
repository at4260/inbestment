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
