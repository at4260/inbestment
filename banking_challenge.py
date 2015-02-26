""" This file is to deal with adding new users with accounts that have 
challenges (security questions). """

@app.route("/banklogin")
def login_bank():
	return render_template("banking.html")

# standard bank login
@app.route("/banklogin", methods=["POST"])
def access_bank():
	credentials = {}
	username = request.form["usr_name"]
	password = request.form["usr_password"]
	# USERID and PASSWORD are specific to the values of the "name" key
		# for TD Ameritrade using the get_credential_fields function
	credentials["USERID"] = username
	credentials["PASSWORD"] = password
	# 9933 is the TD Ameritrade Institution ID
	r = client.discover_and_add_accounts(9933, **credentials)
	print r
	# shows the <Challenge objects> (might be in a list)
	print r.content
	# shows the text of the challenge objects (the actual 
		# challenge questions)
	print r.content.text
	# shows the dictionary of challengenodeid and challengesession id
	print r.headers
	print r.content.account_nickname, r.content.account_number
	return redirect("/banklogin/challenge")

@app.route("/banklogin/challenge")
def input_challenge():
	return render_template("banking_challenge.html")

@app.route("/banklogin/challenge", methods=["POST"])
def process_challenge():
	# re-asking for login information to have the "r" variable in this 
		# function, workaround for not passing functions at this point
	credentials = {}
	username = request.form["usr_name"]
	password = request.form["usr_password"]
	credentials["USERID"] = username
	credentials["PASSWORD"] = password
	r = client.discover_and_add_accounts(9933, **credentials)
	# access "r"'s dictionary to pull the session and node id
	challenge_session_id = r.headers["challengesessionid"]
	challenge_node_id = r.headers["challengenodeid"]
	# responses HAS to be in a list for XML to parse, could directly
		# put in responses = ["insert_answer"]
	responses = request.form[[challenge]]
	accounts = client.confirm_challenge(9933, challenge_session_id, 
		challenge_node_id, responses)
	print accounts
	print accounts.content
	print accounts.content.account_nickname, accounts.content.account_number
	return redirect("/")
