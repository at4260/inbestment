""" This file will be to create the app routes and framework of the app. """

from flask import Flask, render_template, redirect, request, flash, g
from flask import session as f_session
from model import session as m_session
import model
import utils
import accounts
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'thisisasecretkey'

@app.before_request
def before_request():
	if "email" in f_session:
		g.status = "Log Out"
		g.logged_in = True
		g.email = f_session["email"]
		g.user = m_session.query(model.User).filter_by(email = g.email).first()
		if g.user.income != None:
			g.inputs = True
		else:
			g.inputs = False
	else:
		g.status = "Log In"
		g.logged_in = False

@app.route("/")
def home_page():
    return render_template("home.html")

@app.route("/login")
def show_login():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
	email = request.form["email"]
	password = request.form["password"]

	user = m_session.query(model.User).filter_by(email = email).first()

	if user != None:
		if email == user.email and password == user.password:
			f_session["email"] = email
			flash ("Login successful.")
			return redirect("/profile")
		else:
			flash ("Incorrect password. Try again.")
			return redirect("/login")
	else:
		flash ("Please create an account first.")
		return redirect("/create")

@app.route("/create")
def create_acct():
    return render_template("create_acct.html")

@app.route("/create", methods=["POST"])
def process_acct():
	email = request.form["email"]
	password = request.form["password"]

	user = m_session.query(model.User).filter_by(email = email).first()

    # checks that user isn't creating a duplicate account
	if user != None:
		flash ("That account already exists. Please log in.")
		return redirect("/login")
	else:
	    new_user_acct = model.User(email=email, password=password)
	    m_session.add(new_user_acct)
	    m_session.commit()
	    flash("Your account has been succesfully added.")
	    f_session["email"] = email
	    return redirect("/input")

@app.route("/banklogin")
def login_bank():
	return render_template("banking.html")

@app.route("/banklogin", methods=["POST"])
def access_bank():
	credentials = {}
	username = request.form["usr_name"]
	password = request.form["usr_password"]
	credentials["USERID"] = username
	credentials["PASSWORD"] = password
	# FIXME - if returns http error code, flash account does not exist or
	# password is incorrect.
	account = accounts.discover_add_account(accounts.create_client(), 
		credentials)
	# assumes all accounts are savings accounts
	savings_balance = account.balance_amount

	email = f_session["email"]
	user = m_session.query(model.User).filter_by(email = email).first()
	# checks that user's assets are getting updated each time they change
    	# their input, and not getting added to the database
	user_assets = m_session.query(model.UserBanking).filter_by(user_id = 
		user.id).first()
	if user_assets != None:
		update_assets = m_session.query(model.UserBanking).filter_by(user_id = 
			user.id).update({model.UserBanking.savings_amt: savings_balance})
	else:
		new_account = model.UserBanking(user_id=user.id, 
			savings_amt=savings_balance)
		m_session.add(new_account)
	m_session.commit()
	
	# print account.account_nickname
	# print account.balance_amount

	return redirect("/input")

@app.route("/profile")
def show_existing_inputs():
	""" 
	This shows the user's current saved inputs and allows them 
	to either move on or edit it. 
	"""
	if g.logged_in == True:
		if g.inputs == True:
			user_assets = m_session.query(model.UserBanking).filter_by(user_id = 
				g.user.id).first()
			total_assets = user_assets.checking_amt + user_assets.savings_amt + \
				user_assets.IRA_amt + user_assets.comp401k_amt + \
				user_assets.investment_amt
			risk_prof = m_session.query(model.RiskProfile).filter_by(id = 
				g.user.risk_profile_id).first()
			return render_template("profile_inputs.html", 
				assets=utils.format_currency(total_assets),
				income=utils.format_currency(g.user.income), 
				company_401k=g.user.company_401k, 
				company_match=g.user.company_match, 
				match_percent=utils.format_percentage(g.user.match_percent), 
				match_salary=utils.format_percentage(g.user.match_salary), 
				risk_profile=risk_prof.name)
		else:
			flash ("We do not have any financial data on you. \
					Please input now.")
			return redirect("/input")	
	else:
		return redirect("/login")

@app.route("/input")
def create_inputs():
	""" 
	This allows the user to enter and edit their financial inputs. 
	"""
	if g.logged_in == True:
		if g.inputs == True:
			assets = m_session.query(model.UserBanking).filter_by(
				user_id = g.user.id).first().checking_amt
			income = m_session.query(model.User).filter_by(id = 
				g.user.id).first().income
			comp_401k = m_session.query(model.User).filter_by(id = 
				g.user.id).first().company_401k
			match_401k = m_session.query(model.User).filter_by(id = 
				g.user.id).first().company_match
			match_percent = m_session.query(model.User).filter_by(id = 
				g.user.id).first().match_percent
			match_salary = m_session.query(model.User).filter_by(id = 
				g.user.id).first().match_salary

			risk_tolerance_id = m_session.query(model.User).filter_by(id = 
				g.user.id).first().risk_profile_id
			risk_tolerance = m_session.query(model.RiskProfile).filter_by(
				id = risk_tolerance_id).first().name
 		else:
			assets = income = comp_401k = match_401k = match_percent = \
			match_salary = risk_tolerance = 0
		return render_template("inputs.html",
			assets=assets,
			income=income,
			comp_401k=comp_401k,
			match_401k=match_401k,
			match_percent=match_percent,
			match_salary=match_salary,
			risk_tolerance=risk_tolerance)
	else:
		return redirect("/login")

@app.route("/input", methods=["POST"])
def show_results():
	""" 
	This route relies on pulling inputs from user input 
	(as a post request), saving to database, and routes to /results
	to perform the calculations.
	"""
	assets = float(request.form["assets"])
	income = float(request.form["income"])
	comp_401k = request.form["401k"]
	match_401k = request.form["match"]
	match_percent = float(request.form["match_percent"])
	match_salary = float(request.form["salary_percent"])

	risk_tolerance = request.form["risk_tolerance"]
	risk_profile_id = m_session.query(model.RiskProfile).filter_by(name = 
		risk_tolerance).one().id

	# Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.income: income, model.User.company_401k: 
		comp_401k, model.User.company_match: match_401k, 
		model.User.match_percent: match_percent, model.User.match_salary: 
		match_salary, model.User.risk_profile_id: risk_profile_id})
	m_session.commit()

    # Checks that user's assets are getting updated each time they change
    # their input, and not getting added to the database.
	# Assumes that all assets will be in checkings
	user_assets = m_session.query(model.UserBanking).filter_by(user_id = 
		g.user.id).first()
	if user_assets != None:
		update_assets = m_session.query(model.UserBanking).filter_by(user_id =
		g.user.id).update({model.UserBanking.checking_amt: assets})
	else:
		new_account = model.UserBanking(user_id=g.user.id, checking_amt=assets,
			savings_amt=0, IRA_amt=0, comp401k_amt=0, investment_amt=0)
		m_session.add(new_account)
	m_session.commit()

	return redirect("/results")

@app.route("/results")
def show_existing_results():
	""" 
	This route accesses saved data from the database and 
	calculates the results. 
	"""
	if g.logged_in == True:
		if g.inputs == True:
			user_assets = m_session.query(model.UserBanking).filter_by(
				user_id = g.user.id).one()

			assets = user_assets.checking_amt + user_assets.savings_amt + \
				user_assets.IRA_amt + user_assets.comp401k_amt + \
				user_assets.investment_amt
			income = g.user.income
			comp_401k = g.user.company_401k
			match_401k = g.user.company_match
			match_percent = g.user.match_percent
			match_salary = g.user.match_salary

			results = utils.calc_financial_results(assets, income, comp_401k, 
				match_401k, match_percent, match_salary)
			max_results = utils.calc_max_financials(income, comp_401k, 
				match_401k, match_percent, match_salary)

			return render_template("results.html",
				checking=utils.format_currency(results["checking"]),
				savings=utils.format_currency(results["savings"]), 
				match=utils.format_currency(results["match"]),
				ira=utils.format_currency(results["ira"]),
				ret401k=utils.format_currency(results["ret401k"]), 
				investment=utils.format_currency(results["investment"]),
				results=json.dumps(results),
				max_results=json.dumps(max_results))
		else:
			flash ("We do not have any financial data on you. \
					Please input now.")
			return redirect("/input")	
	else:
		return redirect("/login")

@app.route("/investments")
def show_investments():
	if g.logged_in == True:
		if g.inputs == True:
			# Risk_prof is <Risk Profile ID=2 Name=Moderate>
			risk_prof = m_session.query(model.RiskProfile).filter_by(id = 
				g.user.risk_profile_id).one()

			ticker_dict = {}

			prof_ticker_id_list = []
			
			chart_ticker_dict = {}
			stock_data = {}
			bond_data = {}

			# Risk_prof.allocation is list of
			# <Risk Profile ID=2 Ticker ID=1 Ticker Weight=25>.			
			for prof_ticker in risk_prof.allocation:
				# Individual_ticker is using the ticker relationship
				# to get the object <Ticker ID=6 Symbol=VWO 
				# Name=Vanguard FTSE Emerging Markets ETF (VWO)>.
				individual_ticker = prof_ticker.ticker
				ticker_name = individual_ticker.name
				weight = prof_ticker.ticker_weight_percent
				ticker_dict[ticker_name] = weight

				prof_ticker_id_list.append(prof_ticker.ticker_id)
				
				if individual_ticker.category == "Stocks":
					stock_data[ticker_name] = weight
					chart_ticker_dict["Stocks"] = stock_data
				else:
					bond_data[ticker_name] = weight
					chart_ticker_dict["Bonds"] = bond_data

			dates = []
			total_performance = []

			# Marking the date of the most recent data point-
			# this date will be the same for all tickers.
			final_date = m_session.query(model.Price).filter_by(id=1).first().date
			
			# This is the start date for all funds.
			first_date = datetime.strptime("2007-04-10", "%Y-%m-%d").date()

			# Deals with 2007-04-10 case where percent change is None
			# Str- changes datetime to a JSON serializable object
			dates.append(str(first_date))
			total_performance.append(0)
			
			days_value = 0
			incrementing_date = first_date + timedelta(days=days_value)			
			
			while incrementing_date < final_date:
				days_value = days_value + 1	
				incrementing_date = first_date + timedelta(days=days_value)
				# Checks for all Price instances that are part of the profile 
				# allocation and meets the date requirement.
				matched_ticker_prices = m_session.query(model.Price).filter(
					model.Price.date==incrementing_date, model.Price.ticker_id
					.in_(prof_ticker_id_list)).all()
				dates.append(str(incrementing_date))
											

				matched_total_performance = 0
				for matched_ticker_price in matched_ticker_prices:
					matched_ticker_percent_change = matched_ticker_price.percent_change
					matched_ticker_name = matched_ticker_price.ticker.name
					# Converts integer value to percent
					matched_weight_percent = round(float(ticker_dict[
						matched_ticker_name])/100, 4)
					matched_ticker_performance = matched_ticker_percent_change \
						* matched_weight_percent
					matched_total_performance = matched_total_performance \
						+ matched_ticker_performance
				total_performance.append(round(matched_total_performance, 3))
				
			# FIXME - print each individual component fund, use dict
			# # ex: {'lst_300': [], 'lst_75': [], 'lst_100': [], 'lst_2': [], 'lst_4': []}
			# fund_number = 1
			# for prof_ticker in risk_prof.allocation:
			# 	solo_ticker_id = prof_ticker.ticker_id
			# 	solo_ticker = m_session.query(model.Price).filter_by(
			# 		ticker_id=solo_ticker_id).all()
			# 	dates_number_1 = []
			# 	print performance_number_list
			# 	fund_number = fund_number + 1

			# 	for value in ticker_7:
			# 		date = str(value.date)
			# 		percent_price = value.percent_change
			# 		dates.append(date)
			# 		percent_prices.append(percent_price)
			# 	dates.reverse()
			# 	percent_prices.reverse()



			return render_template("investments.html", 
				risk_prof=risk_prof.name, 
				dates=json.dumps(dates), 
				total_performance=json.dumps(total_performance),
				chart_ticker_dict=json.dumps(chart_ticker_dict))
		else:
			flash ("We do not have any financial data on you. \
					Please input now.")
			return redirect("/input")	
	else:
		return redirect("/login")

@app.route("/logout")
def process_logout():
	f_session.clear()
	flash("You are succesfully logged out.")
	return redirect("/")

if __name__ == "__main__":
    app.run(debug = True)
