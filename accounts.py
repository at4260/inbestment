""" Uses Python aggcat module to call the Intuit Customer Account 
Data API """

from aggcat import AggcatClient
from lxml import etree
from aggcat.utils import remove_namespaces

institutions = {"Chase": 13278, "TD Ameritrade": 9933}

def create_client():
	"""
	Processes Intuit tokens to initialize the API client.
	"""
	token_file = open("intuit_tokens.txt")
	token_list = []
	for token in token_file:
		token = token.strip()
		token_list.append(token)

	client = AggcatClient(token_list[0], token_list[1], token_list[2], 
		'1', './testapp1.key', verify_ssl = False) 
	return client

def get_institutions(client, search_string):
	"""
	Searches for the institution by search string (ex: 'Chase') 
	to return institution ID and name.
	"""
	institutions = client.get_institutions()

	xml = etree.fromstring(institutions.content.to_xml())
	xml = etree.fromstring(remove_namespaces(xml))

	for element in xml.xpath('./institution[contains(., "chase")]'):
	    id = element.xpath('./institutionId')[0].text
	    name = element.xpath('./institutionName')[0].text
	    print id, name

def get_institution_details(client, institution):
	"""
	Searches for the institution by institution ID and return
	institutional information.
	"""
	institution = client.get_institution_details(institutions[institution])
	name = institution.content.institution_name
	return name

def get_credential_fields(client, institution):
	"""
	Gets the dictionary of fields required to login to a specific
	institution.
	"""
	user_fields = {}
	credentials = client.get_credential_fields(institutions[institution])
	username_field = credentials[0]['name']
	password_field = credentials[1]['name']
	user_fields["username"] = username_field
	user_fields["password"] = password_field
	return user_fields

def discover_add_account(client, institution, credentials):
	"""
	Adds account with the credientials provided. Returns account
	object.

	Credentials is a dictionary that is being generated from
	controller.py with user inputted credentials. 
	"""
	account = client.discover_and_add_accounts(institutions[institution], 
		**credentials)
	return account

def get_account(client, account_id):
	"""
	Returns a list of all current customer accounts. Aggregates
	all accounts in the client.
	"""
	accounts = client.get_account(account_id)
	print accounts
	accounts = accounts.content
	print accounts

def get_customer_accounts(client):
	"""

	"""
	all_accounts = client.get_customer_accounts()
	print all_accounts
	all_accounts = all_accounts.content
	print all_accounts
	# for account in all_accounts:
	# 	print account
	print all_accounts.account_nickname
	
def delete_account(client, account_id):
	delete_account = client.delete_account(account_id)

def confirm_challenge(client, institution, challenge_session_id, 
	challenge_node_id, responses):
	accounts = client.confirm_challenge(institutions[institution],
		challenge_session_id, challenge_node_id, responses)
	return accounts

def main():
	# pass
	# print get_institution_details(create_client(), "TD Ameritrade")
	# get_institutions(create_client(), 'Chase')
	# get_account(create_client(), 400070545019)
	# print get_credential_fields(create_client(), "Chase")
	# print get_credential_fields(create_client(), "TD Ameritrade")
	get_customer_accounts(create_client())

if __name__ == "__main__":
	main()

