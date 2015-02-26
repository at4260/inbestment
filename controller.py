""" This file will be to create the app routes and framework of the app. """

from flask import Flask, render_template, redirect, request, flash
from flask import session as f_session
from model import session as m_session
import model
import utils
import accounts

app = Flask(__name__)
app.secret_key = 'thisisasecretkey'

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
			# deals with edge case where user has logged in before
				# but has not provided any inputs
			if user.income == None:
				flash ("We do not have any financial data on you. \
					Please input now.")
				return redirect("/input")
			else:
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
	password =request.form["password"]

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


# FIXME- need to link to rest of app, incorporate account logic
	# into "inputs"
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
	
	print account.account_nickname
	print account.balance_amount

	return redirect("/input")

@app.route("/profile")
def show_existing_inputs():
	""" This shows the user's current saved inputs and allows them 
	to either move on or edit it. """
	email = f_session["email"]
	user = m_session.query(model.User).filter_by(email = 
		email).first()
	risk_prof = m_session.query(model.RiskProfile).filter_by(id = 
		user.risk_profile_id).first()
	return render_template("profile_inputs.html", 
		income=utils.format_currency(user.income), 
		company_401k=user.company_401k, 
		company_match=user.company_match, 
		match_percent=utils.format_percentage(user.match_percent), 
		match_salary=utils.format_percentage(user.match_salary), 
		risk_profile=risk_prof.name)

@app.route("/input")
def create_inputs():
	""" This allows the user to enter their financial inputs. """
	return render_template("inputs.html")

@app.route("/results", methods=["POST"])
def show_results():
	""" This route relies on pulling inputs from user input 
	(as a post request) and calculating results. """
	assets = float(request.form["assets"])
	income = float(request.form["income"])
	comp_401k = request.form["401k"]
	match_401k = request.form["match"]
	match_percent = float(request.form["match_percent"])
	match_salary = float(request.form["salary_percent"])

	# unpacking the list from the calculate_results function
	checking_needed, savings_needed, match_needed, ira_needed, \
	ret401k_needed, investment_needed = utils.calculate_results(assets, 
		income, comp_401k, match_401k, match_percent, match_salary)

	risk_tolerance = request.form["risk_tolerance"]
	risk_profile_id = m_session.query(model.RiskProfile).filter_by(name = 
		risk_tolerance).one().id

	# find user id using f_session and then update the database with the 
		# user's financial inputs
	email = f_session["email"]
	user = m_session.query(model.User).filter_by(email = email).first()
	update_user = m_session.query(model.User).filter_by(id = 
		user.id).update({model.User.income: income, model.User.company_401k: 
		comp_401k, model.User.company_match: match_401k, 
		model.User.match_percent: match_percent, model.User.match_salary: 
		match_salary, model.User.risk_profile_id:risk_profile_id})
	m_session.commit()

    # checks that user's assets are getting updated each time they change
    	# their input, and not getting added to the database
	# assumes that all assets will be in checkings
	user_assets = m_session.query(model.UserBanking).filter_by(user_id = 
		user.id).first()
	if user_assets != None:
		update_assets = m_session.query(model.UserBanking).filter_by(user_id =
		user.id).update({model.UserBanking.checking_amt: assets})
	else:
		new_account = model.UserBanking(user_id=user.id, checking_amt=assets)
		m_session.add(new_account)
	m_session.commit()

	return render_template("results.html", 
		checking=utils.format_currency(checking_needed),
		savings=utils.format_currency(savings_needed), 
		match=utils.format_currency(match_needed),
		ira=utils.format_currency(ira_needed),
		ret401k=utils.format_currency(ret401k_needed), 
		investment=utils.format_currency(investment_needed))

@app.route("/results")
def show_existing_results():
	""" This route relies on pulling inputs from the database, rather
	than user input (post request) and calculating results. """
	email = f_session["email"]
	user = m_session.query(model.User).filter_by(email = email).one()
	user_assets = m_session.query(model.UserBanking).filter_by(
		user_id = user.id).one()

	assets = user_assets.checking_amt
	income = user.income
	comp_401k = user.company_401k
	match_401k = user.company_match
	match_percent = user.match_percent
	match_salary = user.match_salary

	# unpacking the list from the calculate_results function
	checking_needed, savings_needed, match_needed, ira_needed, \
	ret401k_needed, investment_needed = utils.calculate_results(assets, 
		income, comp_401k, match_401k, match_percent, match_salary)

	return render_template("results.html", 
		checking=utils.format_currency(checking_needed),
		savings=utils.format_currency(savings_needed), 
		match=utils.format_currency(match_needed),
		ira=utils.format_currency(ira_needed),
		ret401k=utils.format_currency(ret401k_needed), 
		investment=utils.format_currency(investment_needed))

@app.route("/investments")
def show_investments():
	email = f_session["email"]
	user_risk_id = m_session.query(model.User).filter_by(email = 
		email).one().risk_profile_id
	
	risk_prof = m_session.query(model.RiskProfile).filter_by(id = 
		user_risk_id).one()

	ticker_dict = {}
	for ticker in risk_prof.allocation:
		ticker_name = m_session.query(model.Ticker).get(ticker.ticker_id).name
		weight = ticker.ticker_weight_percent
		ticker_dict[ticker_name] = weight

	return render_template("investments.html", risk_prof=risk_prof.name, 
		ticker_dict=ticker_dict)

if __name__ == "__main__":
    app.run(debug = True)
