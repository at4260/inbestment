def format_currency(value):
	return "${:,.2f}".format(value)

def format_percentage(value):
	return "{0:.0f}%".format(value * 100)

def calculate_results(assets, income, comp_401k, match_401k, match_percent, 
	match_salary):
	monthly_expenses = (income * (0.28 + 0.36 + 0.10)) / 12
	checking_needed = monthly_expenses * 1
	savings_needed = monthly_expenses * 3

	if assets < checking_needed:
		checking_needed = assets
	assets = assets - checking_needed

	if assets < savings_needed:
		savings_needed = assets
	assets = assets - savings_needed

	match_needed = income * match_percent * match_salary

	if comp_401k == "Yes":
		if match_401k == "Yes":
			if assets < match_needed:
				match_needed = assets
			assets = assets - match_needed
		else:
			match_needed = 0
	else:
		match_needed = 0

	ret401k_needed = 18000 - match_needed
	ira_needed = 5500   

	if assets < ira_needed:
		ira_needed = assets
	assets = assets - ira_needed

	if comp_401k == "Yes":
		if assets < ret401k_needed:
			ret401k_needed = assets
		assets = assets - ret401k_needed
	else:
		ret401k_needed = 0

	investment_needed = assets
	assets = assets - investment_needed

	results_list = []
	# appending mutliple items to a list at one time
	results_list.extend([checking_needed, savings_needed, match_needed, 
		ira_needed, ret401k_needed, investment_needed])
	return results_list
