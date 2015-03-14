""" This file will be to create the app routes and framework of the app. """

import accounts
import json
import model
import requests
import seed
import utils

from flask import Flask, render_template, redirect, request, flash, g
from flask import session as f_session
from model import session as m_session
from passlib.hash import pbkdf2_sha512


app = Flask(__name__)
app.secret_key = 'thisisasecretkey'

@app.before_request
def before_request():
	if "email" in f_session:
		g.status = "Log Out"
		g.logged_in = True
		g.email = f_session["email"]
		g.user = m_session.query(model.User).filter_by(email=g.email).first()
		if g.user.income != None and g.user.company_401k != None and \
			g.user.company_match != None and g.user.match_percent != \
			None and g.user.match_salary != None and g.user.risk_profile_id \
			!= None:
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
	if g.logged_in == True:
		flash ("You are already logged in.")
		return redirect("/")
	else:
		return render_template("login.html")

@app.route("/login", methods=["POST"])
def process_login():
	email = request.form["email"]
	password = request.form["password"]

	user = m_session.query(model.User).filter_by(email=email).first()
	
	if user != None:
		hashed_password = user.password
		verify_password = pbkdf2_sha512.verify(password, hashed_password)
		if email == user.email and verify_password == True:
			f_session["email"] = email
			flash ("Login successful.")
			return redirect("/profile")
		else:
			flash ("Incorrect username or password. Try again.")
			return redirect("/login")
	else:
		flash ("Please create an account first.")
		return redirect("/create")

@app.route("/create")
def create_acct():
	if g.logged_in == True:
		flash ("You are already logged in.")
		return redirect("/")
	else:
		return render_template("create_acct.html")

@app.route("/create", methods=["POST"])
def process_acct():
	email = request.form["email"]
	password = request.form["password"]
	hashed_password = pbkdf2_sha512.encrypt(password, salt=b'64', 
		rounds=100000, salt_size=16)

	# Checks that user isn't creating a duplicate account
	user = m_session.query(model.User).filter_by(email=email).first()
	if user != None:
		flash ("That account already exists. Please log in.")
		return redirect("/login")
	else:
	    new_user_acct = model.User(email=email, password=hashed_password)
	    m_session.add(new_user_acct)
	    m_session.commit()
	    flash("Your account has been succesfully added.")
	    f_session["email"] = email
	    return redirect("/input/banking")

@app.route("/banklogin")
def login_bank():
	if g.logged_in == True:
		return render_template("banking.html")
	else:
		return redirect("/login")

@app.route("/banklogin", methods=["POST"])
def access_bank():
	"""
	Allows login to banking institutions using Intuit API and
	Python library aggcat. Calls functions in accounts.py.

	Assumes that all account assets will be savings accounts.
	"""
	institution = str(request.form["institution"])
	username = request.form["user_name"]
	password = request.form["user_password"]

	user_fields = accounts.get_credential_fields(accounts.create_client(),
		institution)
	credentials = {}
	credentials[user_fields["username"]] = username
	credentials[user_fields["password"]] = password

	try:
		account = accounts.discover_add_account(accounts.create_client(), 
			institution, credentials)
		account_data = account.content
		
		# Checks the HTTP error code if account needs further authentication
		if account.status_code in [200, 201]:
			savings_balance = account_data.balance_amount

			# Checks that user's assets are getting updated each time they change
			# their input, and not getting added to the database.
			user_assets = m_session.query(model.UserBanking).filter_by(
				user_id=g.user.id).first()
			if user_assets != None:
				update_assets = m_session.query(model.UserBanking).filter_by(
					user_id=g.user.id).update({model.UserBanking.savings_amt: 
					savings_balance})
			else:
				new_account = model.UserBanking(user_id=g.user.id, 
					savings_amt=savings_balance)
				m_session.add(new_account)
			m_session.commit()
			flash ("%s account XXXX%s with $%s has been added to your assets." %(
				account_data.account_nickname, account_data.account_number[-4:],
				account_data.balance_amount))
			return redirect("/input/assets")	
		else:
			return redirect("/banklogin/challenge")	
	except:
		flash ("There was an error accessing your account. Please try again.")
		return redirect("/banklogin")
	
@app.route("/banklogin/challenge")
def input_challenge():
	if g.logged_in == True:
		return render_template("banking_challenge.html")
	else:
		return redirect("/login")

@app.route("/banklogin/challenge", methods=["POST"])
def process_challenge():
	"""
	Authenticates access to banking institutions if there is a challenge
	response with HTTP code 401. 
	"""	
	try:
		institution = str(request.form["institution"])
		username = request.form["user_name"]
		password = request.form["user_password"]
		# Responses must be in a list for XML to parse
		responses = request.form[[challenge]]

		user_fields = accounts.get_credential_fields(accounts.create_client(),
			institution)
		credentials = {}
		credentials[user_fields["username"]] = username
		credentials[user_fields["password"]] = password
		
		account = accounts.discover_and_add_accounts(accounts.create_client(), 
			institution, credentials)
		# Access "account" dictionary to pull the session and node id
		challenge_session_id = account.headers["challengesessionid"]
		challenge_node_id = account.headers["challengenodeid"]

		confirmed_account = accounts.confirm_challenge(create_client(), 
			institution, challenge_session_id, challenge_node_id,
			responses)
		
		print accounts.content.account_nickname, accounts.content.account_number
		savings_balance = confirmed_account.balance_amount

		user_assets = m_session.query(model.UserBanking).filter_by(
			user_id=g.user.id).first()
		if user_assets != None:
			update_assets = m_session.query(model.UserBanking).filter_by(
				user_id=g.user.id).update({model.UserBanking.savings_amt: 
				savings_balance})
		else:
			new_account = model.UserBanking(user_id=g.user.id, 
				savings_amt=savings_balance)
			m_session.add(new_account)
		m_session.commit()
		flash ("%s account XXXX%s with $%s has been added to your assets." %(
			confirmed_account.content.account_nickname, 
			confirmed_account.content.account_number[-4:],
			confirmed_account.content.balance_amount))
		return redirect("/input/assets")
	except:
		flash ("There was an error authenticating your account. Please \
			try again.")
		return redirect("/banklogin/challenge")

@app.route("/input/banking")
def add_bank():
	"""
	This allows the user to add their external bank accounts.
	"""
	if g.logged_in == True:
		return render_template("input_banking.html")
	else:
		return redirect("/login")

@app.route("/input/assets")
def input_assets():
	"""
	This allows the user to enter and edit their financial assets. 
	"""
	if g.logged_in == True:
		if g.inputs == True:
			assets = m_session.query(model.UserBanking).filter_by(
				user_id = g.user.id).first().checking_amt
 		else:
			assets = 0
		return render_template("input_assets.html",
			assets=assets)
	else:
		return redirect("/login")

@app.route("/input/assets", methods=["POST"])
def save_assets():
	""" 
	Pulls assets from user input (as a post request), save to 
	database, and routes to next question (/results will perform
	the calculations).
	"""
	assets = float(request.form["assets"])

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

	return redirect("/input/income")

@app.route("/input/income")
def input_income():
	"""
	This allows the user to enter and edit their income. 
	"""
	if g.logged_in == True:
		if g.inputs == True:
			income = m_session.query(model.User).filter_by(id = 
				g.user.id).first().income
 		else:
			income = 0
		return render_template("input_income.html",
			income=income)
	else:
		return redirect("/login")

@app.route("/input/income", methods=["POST"])
def save_income():
	""" 
	Pulls income from user input (as a post request), save to 
	database, and routes to next question (/results will perform
	the calculations).
	"""
	income = float(request.form["income"])

    # Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.income: income})
	m_session.commit()

	return redirect("/input/comp_401k")

@app.route("/input/comp_401k")
def input_comp_401k():
	"""
	This allows the user to enter and edit if their company has a 401k. 
	"""
	if g.logged_in == True:
		if g.inputs == True:
			comp_401k = m_session.query(model.User).filter_by(id = 
				g.user.id).first().company_401k
 		else:
			comp_401k = 0
		return render_template("input_comp_401k.html",
			comp_401k=comp_401k)
	else:
		return redirect("/login")

@app.route("/input/comp_401k", methods=["POST"])
def save_comp_401k():
	""" 
	Pulls company 401k from user input (as a post request), save to 
	database, and routes to next question (/results will perform
	the calculations).
	"""
	comp_401k = request.form["401k"]

    # Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.company_401k: comp_401k})
	m_session.commit()

	return redirect("/input/match_401k")

@app.route("/input/match_401k")
def input_match_401k():
	"""
	This allows the user to enter and edit if their company has a 401k
	match. 
	"""
	if g.logged_in == True:
		# If user selects that they do not have a company 401k, skip
		# all 401k-related questions.
		comp_401k = m_session.query(model.User).filter_by(id = 
			g.user.id).first().company_401k
		if comp_401k == "Yes":
			if g.inputs == True:
				match_401k = m_session.query(model.User).filter_by(id = 
					g.user.id).first().company_match
	 		else:
				match_401k = 0
			return render_template("input_match_401k.html",
				match_401k=match_401k)
		else:
			match_401k = "No"
			match_percent = match_salary = 0
			update_user = m_session.query(model.User).filter_by(id = 
				g.user.id).update({model.User.company_match: match_401k, 
				model.User.match_percent: match_percent, 
				model.User.match_salary: match_salary})
			m_session.commit()
			return redirect("/input/risk_tolerance")
	else:
		return redirect("/login")

@app.route("/input/match_401k", methods=["POST"])
def save_match_401k():
	""" 
	Pulls company 401k match from user input (as a post request), save  
	to database, and routes to next question (/results will perform
	the calculations).
	"""
	match_401k = request.form["match"]

    # Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.company_match: match_401k})
	m_session.commit()

	return redirect("/input/match_percent")

@app.route("/input/match_percent")
def input_match_percent():
	"""
	This allows the user to enter and edit the match percent of their
	401k match.
	"""
	if g.logged_in == True:
		# If user selects that they do not have a 401k match, skip
		# all 401k match-related questions.
		match_401k = m_session.query(model.User).filter_by(id = 
			g.user.id).first().company_match
		if match_401k == "Yes":
			if g.inputs == True:
				match_percent = m_session.query(model.User).filter_by(id = 
					g.user.id).first().match_percent
	 		else:
				match_percent = 0
			return render_template("input_match_percent.html",
				match_percent=match_percent)
		else:
			match_percent = match_salary = 0
			update_user = m_session.query(model.User).filter_by(id = 
				g.user.id).update({model.User.match_percent: 
				match_percent, model.User.match_salary: match_salary})
			m_session.commit()
			return redirect ("/input/risk_tolerance")
	else:
		return redirect("/login")

@app.route("/input/match_percent", methods=["POST"])
def save_match_percent():
	""" 
	Pulls match percent from user input (as a post request), save  
	to database, and routes to next question (/results will perform
	the calculations).
	"""
	match_percent = float(request.form["match_percent"])

    # Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.match_percent: match_percent})
	m_session.commit()

	return redirect("/input/match_salary")

@app.route("/input/match_salary")
def input_match_salary():
	"""
	This allows the user to enter and edit the max salary percent match.
	"""
	if g.logged_in == True:
		# If user selects that they do not have a 401k match, skip
		# all 401k match-related questions.
		match_401k = m_session.query(model.User).filter_by(id = 
			g.user.id).first().company_match
		if match_401k == "Yes":
			if g.inputs == True:
				match_salary = m_session.query(model.User).filter_by(id = 
					g.user.id).first().match_salary
	 		else:
				match_salary = 0
			return render_template("input_match_salary.html",
				match_salary=match_salary)
		else:
			match_percent = match_salary = 0
			update_user = m_session.query(model.User).filter_by(id = 
				g.user.id).update({model.User.match_percent: 
				match_percent, model.User.match_salary: match_salary})
			m_session.commit()
			return redirect ("/input/risk_tolerance")
	else:
		return redirect("/login")

@app.route("/input/match_salary", methods=["POST"])
def save_match_salary():
	""" 
	Pulls max salary percent match from user input (as a post request), 
	save to database, and routes to next question (/results will perform
	the calculations).
	"""
	match_salary = float(request.form["salary_percent"])

    # Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.match_salary: match_salary})
	m_session.commit()

	return redirect("/input/risk_tolerance")

@app.route("/input/risk_tolerance")
def input_risk_tolerance():
	"""
	This allows the user to enter and edit their risk tolerance.
	"""
	if g.logged_in == True:
		if g.inputs == True:
			risk_tolerance_id = m_session.query(model.User).filter_by(id = 
				g.user.id).first().risk_profile_id
			risk_tolerance = m_session.query(model.RiskProfile).filter_by(
				id = risk_tolerance_id).first().name
 		else:
			risk_tolerance = 0
		return render_template("input_risk_tolerance.html",
			risk_tolerance=risk_tolerance)
	else:
		return redirect("/login")

@app.route("/input/risk_tolerance", methods=["POST"])
def save_risk_tolerance():
	""" 
	Pulls risk tolerance from user input (as a post request), 
	save to database, and routes to next question (/results will perform
	the calculations).
	"""
	risk_tolerance = request.form["risk_tolerance"]
	risk_profile_id = m_session.query(model.RiskProfile).filter_by(name = 
		risk_tolerance).one().id

    # Find user id using f_session and then update the database with the 
	# user's financial inputs
	update_user = m_session.query(model.User).filter_by(id = 
		g.user.id).update({model.User.risk_profile_id: risk_profile_id})
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
			flash ("Our financial data on you is incomplete. \
					Please input now.")
			return redirect("/input/banking")	
	else:
		return redirect("/login")

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
			flash ("Our financial data on you is incomplete. \
					Please input now.")
			return redirect("/input/banking")	
	else:
		return redirect("/login")		

@app.route("/investments", methods=["GET", "POST"])
def show_investments():
	""" 
	This shows the user's investment summary based on their risk profile
	input. 

	GET request - summary includes a pie graph showing portfolio 
	allocation and line graph showing both total portfolio performance 
	and individual fund performance. 

	POST request - Allows the user to enter in a ticker as a comparison 
	point. Checks ticker against Stocks-GOOG.csv file to find ticker url, 
	make QUANDL	API call, seed database, and plot data on line graph.
	"""
	if g.logged_in == True:
		if g.inputs == True:			
			# Risk_prof is <Risk Profile ID=2 Name=Moderate>
			risk_prof = m_session.query(model.RiskProfile).filter_by(id = 
				g.user.risk_profile_id).first()

			chart_ticker_data = utils.generate_allocation_piechart(risk_prof)
			dates = utils.generate_performance_linegraph(risk_prof)[0]
			total_performance = utils.generate_performance_linegraph(risk_prof)[1]

			prof_ticker_data = utils.save_prof_tickers(risk_prof)
			ticker_query_1 = utils.generate_individual_ticker_linegraph(prof_ticker_data[0][0])
			ticker_query_2 = utils.generate_individual_ticker_linegraph(prof_ticker_data[0][1])
			ticker_query_3 = utils.generate_individual_ticker_linegraph(prof_ticker_data[0][2])
			ticker_query_4 = utils.generate_individual_ticker_linegraph(prof_ticker_data[0][3])
			ticker_query_5 = utils.generate_individual_ticker_linegraph(prof_ticker_data[0][4])

			if request.method == "GET":
				return render_template("investments.html", 
					risk_prof=risk_prof.name, 
					dates=json.dumps(dates),
					total_performance=json.dumps(total_performance),
					chart_ticker_data=json.dumps(chart_ticker_data),
					prof_ticker_data=json.dumps(prof_ticker_data),
					ticker_query_1=json.dumps(ticker_query_1),
					ticker_query_2=json.dumps(ticker_query_2),
					ticker_query_3=json.dumps(ticker_query_3),
					ticker_query_4=json.dumps(ticker_query_4),
					ticker_query_5=json.dumps(ticker_query_5))

			else:
				compare_ticker = request.form["compare_ticker"]
				compare_ticker = compare_ticker.upper()

				# Makes API call to seed database
				filename = "seed_data/Stocks-GOOG.csv"
				ticker_identifier_list = seed.find_ticker([compare_ticker], filename)

				# Checks if ticker is in "Stocks-GOOG.csv"
				if ticker_identifier_list != []:
					check_ticker = m_session.query(model.Ticker).filter_by(
						symbol=compare_ticker).first()
					# Checks if ticker data already exists in the database. If it doesn't,
					# make API call and seed database.
					if check_ticker is None:
						ticker_url_list = seed.build_ticker_url(ticker_identifier_list)
						seed.load_ticker_data(ticker_url_list, m_session)
						utils.calc_percent_change_compare(compare_ticker, m_session)
					
					# Generates data in list to plot on line graph
					compare_ticker_id = model.session.query(model.Ticker).filter_by(symbol=
						compare_ticker).first().id
					compare_ticker_query = utils.generate_individual_ticker_linegraph(
						compare_ticker_id)

					return render_template("investments_compare.html", 
						risk_prof=risk_prof.name, 
						dates=json.dumps(dates),
						total_performance=json.dumps(total_performance),
						chart_ticker_data=json.dumps(chart_ticker_data),
						prof_ticker_data=json.dumps(prof_ticker_data),
						ticker_query_1=json.dumps(ticker_query_1),
						ticker_query_2=json.dumps(ticker_query_2),
						ticker_query_3=json.dumps(ticker_query_3),
						ticker_query_4=json.dumps(ticker_query_4),
						ticker_query_5=json.dumps(ticker_query_5),
						compare_ticker_name=json.dumps([compare_ticker]),
						compare_ticker_query=json.dumps(compare_ticker_query))
				else:
					flash ("Sorry, that ticker does not exist in our database.")
					return redirect("/investments")
		else:
			flash ("Our financial data on you is incomplete. \
					Please input now.")
			return redirect("/input/banking")	
	else:
		return redirect("/login")

@app.route("/logout")
def process_logout():
	f_session.clear()
	flash("You are succesfully logged out.")
	return redirect("/")

@app.route("/about")
def show_about():
	return render_template("about.html")

if __name__ == "__main__":
    app.run(debug = True)
