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
	account = accounts.discover_add_account(accounts.create_client(), credentials)
	# assumes all accounts are checking accounts
	checking_balance = account.balance_amount

	email = f_session["email"]
	user_id = m_session.query(model.User).filter_by(email = 
		email).first().id
	new_account = model.UserBanking(user_id=user_id, 
		checking_amt=checking_balance)
	m_session.add(new_account)
	m_session.commit()
	
	# print account.account_nickname
	# print account.account_number
	# print account.balance_amount
	# print account.current_balance

	return redirect("/input")

@app.route("/profile")
def show_existing_inputs():
	""" This shows the user's current saved inputs and allows them 
	to either move on or edit it. """
	email = f_session["email"]
	user = m_session.query(model.User).filter_by(email = 
		email).first()
	risk_prof = m_session.query(model.RiskProfile).filter_by(id = 
		user.risk_profile_id).one().name
	return render_template("profile_inputs.html", 
		income=utils.format_currency(user.income), 
		company_401k=user.company_401k, 
		company_match=user.company_match, 
		match_percent=user.match_percent, 
		match_salary=user.match_salary, 
		risk_profile=risk_prof)

@app.route("/input")
def create_inputs():
	""" This allows the user to enter their financial inputs. """
	return render_template("inputs.html")

@app.route("/results")
def show_results():
	assets = float(request.args.get("assets"))
	income = float(request.args.get("income"))
	comp_401k = request.args.get("401k")
	match_401k = request.args.get("match")
	match_percent = float(request.args.get("match_percent"))
	match_salary = float(request.args.get("salary_percent"))

	# unpacking the list from the calculate_results function
	checking_needed, savings_needed, match_needed, ira_needed, \
	ret401k_needed, investment_needed = utils.calculate_results(assets, 
		income, comp_401k, match_401k, match_percent, match_salary)

	risk_tolerance = request.args.get("risk_tolerance")
	risk_profile_id = m_session.query(model.RiskProfile).filter_by(name = 
		risk_tolerance).one().id

	# find user id using f_session and then update the database with the 
	# user's financial inputs
	email = f_session["email"]
	user = m_session.query(model.User).filter_by(email = email).one()
	update_user = m_session.query(model.User).filter_by(id = 
		user.id).update({model.User.income: income, model.User.company_401k: 
		comp_401k, model.User.company_match: match_401k, 
		model.User.match_percent: match_percent, model.User.match_salary: 
		match_salary, model.User.risk_profile_id:risk_profile_id})
	m_session.commit()

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
