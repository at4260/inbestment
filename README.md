<img src="static/img/inbestment2.png" width="40%" height="40%">
=======

Putting all of your money under the mattress is never a good choice. The goal of Inbestment is to help individuals easily come up with a financial plan and determine the amount and type of accounts they should fund first. Using the Intuit Customer Account Data API, users are able to import real banking account information to their profiles. Inbestment uses relational database modeling and large datasets to provide a recommended investment portfolio based on risk tolerance and graphically present performance over time. Users can also compare other stock's performance to their portfolio.

Setting Up
--------

Technology Stack
--------
<h5>APIs</h5>
Intuit API, Quandl API

<h5>Back-end</h5>
Python, SQL, SQLAlchemy, Flask, Flask-Login, Flask-WTF, Python Passlib, Python Aggcat (client for Intuit API), Python unittest

<h5>Front-end</h5>
Jinja, Highcharts, Javascript, JQuery, HTML, CSS

File Structure
--------
<h5>Main Files</h5>
- __controller.py__: Main entry point and controls application routing
- __utils.py__: Utility functions for calculating large operations outside of __controller.py__
- __model.py__: Creates the local database model
- __seed.py__: Seeds the local database and allows use of Quandl API
- __accounts.py__: Allows use of Intuit API

Features
--------
<h5>Survey and Profile</h5>
- Allows user to add real banking information through the use of the Intuit Customer Account Data API and the Python aggcat client
	- Passes the institution id for select institutions and passes that into the API call to pull account data (account number and balance amount)
	- Created a route to authenticate challenge scenarios
		- If an account is being validated for the first time, the API may come back with the bank's challenge question to force additional user validation
- User can easily get results based on a maximum of seven questions
	- Values are updated to the database after each question allowing for a responsive survey (ex: if user answers that there is no 401k account, then disable and skip all-401K related questions)
	- Previously entered data will be re-shown within the survey input fields to allow quick changes
- Profile saves all user inputs and allows the user to easily edit any question
- Included "Help" tooltips to assist the user in answering some of the questions

<h5>Results</h5>
- Calculates both the target amount to fund each type of account and checks that against what the user can afford based on inputs.
- Creates a flow through a priority hierarchy of accounts
	- 1. Checking - one month worth of living expenses
	- 2. Savings- three months worth of living expenses
	- 3. 401K match - (if applicable), calculated based on user inputted percent match and percent of salary to match
	- 4. IRA - maximum $5,500 IRS contribution
	- 5. 401K - (if applicable), maximum $18,000 IRS contribution less 401K match
	- 6. Brokerage - remaining assets
- Included "Help" modal to assist the user in interpreting their financial results

<h5>Investments</h5>
- Seeded the database with stock tickers and daily close prices using the Quandl API that returns a JSON object
	- Used raw SQL query to calculate the percent change for each individual date's close price compared to the inception's close price
	- See "Technical Choices" on calculating portfolio performance
- Used Highcharts (Javascript and jQuery) to pass the JSON data objects
- Parsed Quandl API JSON object for "stock" or "bond" to give the ticker a classification
- Implemented ability for user to input a ticker for comparison
	- Checks a .csv file for the ticker's url identifier
	- Calls the Quandl API to return the pricing information
	- Seeds the database with the ticker's information while calculating the percent change
	- Future requests for that ticker will pull straight from the database, rather than making another API call

<h5>Data Modelling</h5>
- Created a detailed data model with many relationships
- Employed raw SQL and SQLAlchemy to query the database across relationships

<h5>Security</h5>
- Encrypted and verified user passwords through hashing and salting
- Used Python Passlib and PBKDF2_SHA512 hash algorithm

<h5>Data Validation and Testing</h5>
- Checked back-end data validity using Flask-WTF and front-end using HTML fields, so the user is not able to input non-integers for assets and income or invalid email and password
- All routes use Flask-g to ensure the following scenarios:
	- A user who is not logged in will be directed to the login page
	- A user who is logged in but has not completed the survey will be directed to completing the survey before accessing any other route
- Wrote unit tests and Flask integration tests
	- Unit tests check that the results calculation is working properly depending on various user inputs
	- Flask integration tests ensures that all routes are working no matter if user is logged in or not or finished completing the survey

<h5>Maintainable Code</h5>
- Checked .py files in PEP8 style guide for formatting consistency
- Larger functions used by controller.py are separated into a separate file utils.py
- Strong workflow and bug tracking using Git to create issues and hunking commits with detailed messages

Technical Choices
--------
<h5>Calculating Total Portfolio Performance</h5>
In order to show total portfolio performance, I needed to query the database for the user's risk profile, pull the the portfolio of stock tickers and weightings associated with the risk profile, and then aggregate all of the tickers' prices for each daily data point.

However, because stock prices are relative, I could not simiply add the daily prices for each ticker together. I initially decided to normalize the data by calculating a daily percent change from the day before, but this resulted in an undynamic line graph. Then, I decided to still calculate a daily percent change, but since inception. This resulted in a more dynamic and interesting line graph; however, I could no longer compare apples-to-apples between stock tickers. (This is because a stock ticker that has 10% growth since inception of 10 years ago cannot be accurately compared to another stock ticker that has 20% growth since inception of 5 years ago.)

Another option I considered would be to annualize the returns, but I would lose some fidelity when displaying the data in a line graph with less data points. I decided to take the latest inception date of all of my stock tickers in the risk tolerance portfolios (4/10/2007) and mark that as the since inception date for all percent changes to be calculated off of. While not optimal, this allowed me to accurately compare performance across stock tickers.

At this point, I could now aggregate the percent change of the stock tickers for each daily data point. Since each stock ticker comprises a different weighting in the portfolio, I used a weighted average to calculate the aggregate percent change.

As an example, for the "Conservative" risk profile and one day's data point:

| Stock Ticker  | Portfolio Weighting | Percent Change (since inception)  |
| :------------ | :------------------ | :-------------------------------  |
| VV            | 25%		      | 0.01		    		  |
| VB            | 20%		      | 0.02				  |
| VEU           |  5%		      | 0.03				  |
| BIV           | 40%		      | 0.04				  |
| BSV           | 10%		      | 0.05				  |

```One day's aggregated performance (weighted average) = ``` <br>
```(0.25 * 0.01) + (0.20 * 0.02) + (0.05 * 0.03) + (0.40 * 0.04) + (0.10 * 0.05)```

My original query was a nested loop using SQLAlchemy that resulted in the line graph taking 18+ seconds to generate:
```
while incrementing_date < final_date:
	days_value = days_value + 1	
	incrementing_date = first_date + timedelta(days=days_value)
	# Checks for all Price instances that are part of the profile 
	# allocation and meets the date requirement.		
	matched_ticker_prices = m_session.query(model.Price).filter(
		model.Price.date==incrementing_date, model.Price.ticker_id
		.in_(prof_ticker_data.keys())).all()

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
```

By changing to a raw SQL query, I was able to have a much more powerful query that resulted in an instanteous response:
```
linegraph_sql_query = """
    SELECT date, sum(percent_change * prof_allocs.ticker_weight_percent)
    FROM prices
    JOIN prof_allocs on (prices.ticker_id = prof_allocs.ticker_id)
    WHERE prof_allocs.risk_profile_id == :sql_risk_prof
    AND prices.date > "2007-04-10"
    GROUP by prices.date
    ORDER by prices.date
    """
```

Future Plans
--------
<h5>Short-term</h5>
- Short-term plans can be found in my github [Issues](https://github.com/at4260/inbestment/issues)

<h5>Long-term</h5>
- Use machine learning to estimate user's assets, income, and company 401K information (to limit number of user inputted fields)
- More customizations and options in risk tolerance portfolios
- Allows user to input all assets from multiple sources (current accounts and investments) and re-allocates their portfolio to Inbestment's recommendation

License
--------
[MIT License](http://www.opensource.org/licenses/mit-license.php)

Copyright (c) 2015 Alice Tsao

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
