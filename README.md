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
Python, SQL, SQLAlchemy, Flask, Flask-Login, Flask-WTF, Jinja, Python Passlib, Python Aggcat (client for Intuit API)

<h5>Front-end</h5>
Highcharts, Javascript, JQuery, HTML, CSS

Features
--------
<h5>Survey and Profile</h5>
- INPUT

<h5>Results</h5>
- INPUT

<h5>Investments</h5>
- The Quandl API allows me to call a ticker and returns a JSON object with pricing information. I am using the daily close price, and then, using a raw SQL query to calculate the percent change for each individual date's close price compared to the inception's close price.
- Used Highcharts to pass the data

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

Future Plans
--------


Technical Choices
--------

License
--------
[MIT License](http://www.opensource.org/licenses/mit-license.php)

Copyright (c) 2015 Alice Tsao

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
