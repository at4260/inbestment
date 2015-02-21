""" This file will be to create the app routes and framework of the app. """

from flask import Flask, render_template, redirect, request, flash
from flask import session as f_session
from model import session as m_session
import model

app = Flask(__name__)
app.secret_key = 'thisisasecretkey'

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/input")
def create_inputs():
    return render_template("inputs.html")

def format_currency(value):
	return "${:,.2f}".format(value)

@app.route("/results")
def show_results():
	assets = float(request.args.get("assets"))
	income = float(request.args.get("income"))
	monthly_expenses = (income * (0.28 + 0.36 + 0.10)) / 12
	checking_needed = monthly_expenses * 1
	savings_needed = monthly_expenses * 3
	
	comp_401k = request.args.get("401k")
	match_401k = request.args.get("match")
	match_percent = float(request.args.get("match_percent"))
	match_salary = float(request.args.get("salary_percent"))
	if match_401k == "yes":
		max_match = income * match_percent * match_salary
		max_401k = 18000 - max_match
	else:
		if comp_401k == "yes":
			max_match = 0
			max_401k = 18000
		else:
			max_match = 0
			max_401k = 0
	ira_needed = 5500   
	investment_acct = assets - checking_needed - savings_needed - max_match - max_401k - ira_needed
	if investment_acct >= 0:
		investment_needed = investment_acct
	else:
		investment_needed = 0
	
	risk_tolerance = request.args.get("risk_tolerance")

	# FIXME add
	# new_user_profile = model.UserProfile(user_id= , income=income, company_401k=comp_401k, company_match=match_401k)

	return render_template("results.html", checking=format_currency(checking_needed), savings=format_currency(savings_needed), max_match=format_currency(max_match), max_401k=format_currency(max_401k), ira=format_currency(ira_needed), investment=format_currency(investment_needed))

@app.route("/investments")
def show_investments():
	conservative = m_session.query(model.RiskProfile).get(1)
	conservative_name = conservative.name
	ticker_dict = {}
	for ticker in conservative.allocation:
		ticker_name = m_session.query(model.Ticker).get(ticker.ticker_id).name
		weight = ticker.ticker_weight_percent
		ticker_dict[ticker_name] = weight

	print ticker_dict

	return render_template("investments.html", conservative=conservative_name, ticker_dict=ticker_dict)

if __name__ == "__main__":
    app.run(debug = True)
