import requests as r
from bs4 import BeautifulSoup

url = 'https://www.veu-registry.vic.gov.au/Public/PublicRegister/Search.aspx'

data = {'ctl00$ctl00$ContentPlaceHolder1$Content$VEECSearch$StatusEdit' :

'Pending+Mandatory+Surrender;Pending+Obligatory+Surrender;Pending+Payment;Pending+Registration+Validation;Pending+Transfer;Pending+Voluntary+Surrender;Registered'}

session = r.Session()

html_raw = session.post(url, data = data)

html_txt = html_raw.text

print(html_txt)