""" This file will be to create the app routes and framework of the app. """

from flask import Flask, render_template, redirect, request, flash
from flask import session as f_session
from model import session as m_session
import model
import utils

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
			return redirect("/input")
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
    flash("Your account has been succesfully added. Please log in.")
    return redirect("/login")

@app.route("/input")
def create_inputs():
    return render_template("inputs.html")

@app.route("/results")
def show_results():
	assets = float(request.args.get("assets"))
	income = float(request.args.get("income"))
	comp_401k = request.args.get("401k")
	match_401k = request.args.get("match")
	match_percent = float(request.args.get("match_percent"))
	match_salary = float(request.args.get("salary_percent"))

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

	if comp_401k == "yes":
		if match_401k == "yes":
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

	if comp_401k == "yes":
		if assets < ret401k_needed:
			ret401k_needed = assets
		assets = assets - ret401k_needed
	else:
		ret401k_needed = 0

	investment_needed = assets
	assets = assets - investment_needed

	risk_tolerance = request.args.get("risk_tolerance")
	risk_profile_id = m_session.query(model.RiskProfile).filter_by(name = risk_tolerance).one().id

	# FIXME - user id should be reliant on login info
	new_user_profile = model.UserProfile(user_id=1, income=income, company_401k=comp_401k, company_match=match_401k, match_percent=match_percent, match_salary=match_salary, risk_profile_id=risk_profile_id)
	m_session.add(new_user_profile)
	m_session.commit()

	return render_template("results.html", 
		assets=utils.format_currency(assets), 
		checking=utils.format_currency(checking_needed),
		savings=utils.format_currency(savings_needed), 
		match=utils.format_currency(match_needed),
		ira=utils.format_currency(ira_needed),
		ret401k=utils.format_currency(ret401k_needed), 
		investment=utils.format_currency(investment_needed))

@app.route("/investments")
def show_investments():
	# FIXME - user id should be reliant on login info
	risk_profile_id = m_session.query(model.UserProfile).filter_by(id = 4).one().risk_profile_id
	risk_prof = m_session.query(model.RiskProfile).filter_by(id = risk_profile_id).one()
	risk_prof_name = risk_prof.name

	ticker_dict = {}
	for ticker in risk_prof.allocation:
		ticker_name = m_session.query(model.Ticker).get(ticker.ticker_id).name
		weight = ticker.ticker_weight_percent
		ticker_dict[ticker_name] = weight

	return render_template("investments.html", risk_prof=risk_prof_name, ticker_dict=ticker_dict)

if __name__ == "__main__":
    app.run(debug = True)
