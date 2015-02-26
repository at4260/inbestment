""" Uses Python aggcat module to call the Intuit Customer Account 
Data API """

from aggcat import AggcatClient
from lxml import etree
from aggcat.utils import remove_namespaces

def create_client():
	token_file = open("intuit_tokens.txt")
	token_list = []
	for token in token_file:
		token = token.strip()
		token_list.append(token)

	client = AggcatClient(token_list[0], token_list[1], token_list[2], '1', './testapp1.key', verify_ssl = False) 
	return client

def get_institution_details(client):
	institution = client.get_institution_details(9933)
	name = institution.content.institution_name
	return name

# credentials is a list that is being generated from controller.py
def discover_add_account(client, credentials):
	account = client.discover_and_add_accounts(9933, **credentials)
	account_data = account.content
	return account_data

def main():
	pass

if __name__ == "__main__":
	main()

