from flask import Flask, jsonify, Response
import requests
from requests_oauthlib import OAuth2, OAuth1
import json
from xml.etree import ElementTree
from ConcurOAuthPython import getbasic, getTokenGivenUsernamePasswordAndConsumerKey

#Constants
USER = "user46@concurdisrupt.com"
PWD = "disrupt"
KEY = 'mbGLfEhU1rUUG8IOImdmVt'
TOKEN = 'NPuB/Wr+a9OkYNWz9Mw/kWNWvyk='
SAMPLE_REPORT_NAME = 'Disrupt Hackathon NYC Trip'
SAMPLE_REPORT_ID = 'D7E30A5A1E1F4ACF82FE'

#Initializing FLASK app
app = Flask(__name__)

#tests
basic = 'Basic ' + getbasic(USER, PWD)
headers1 = getTokenGivenUsernamePasswordAndConsumerKey('user46@concurdisrupt.com', 'disrupt', KEY)

#oauth
auth = {
    'Authorization': "OAuth %s" %  TOKEN,
    'Accept':'application/xml',
    }

@app.route('/')
def hello_world():
    #return json.dumps(getTokenGivenUsernamePasswordAndConsumerKey('user46@concurdisrupt.com', 'disrupt', KEY))

    #Report Digests
    #resp = requests.get('https://www.concursolutions.com/api/v3.0/expense/reportdigests',headers = auth)

    #Locations - NA
    #resp = requests.get('https://www.concursolutions.com/api/v3.0/insights/latestbookings/',headers = auth)

    #Invoices - NA
    #resp = requests.get('https://www.concursolutions.com/api/v3.0/invoice/taxrequests/',headers = auth)

    #Expense Entries
    #resp = requests.get('https://www.concursolutions.com/api/v3.0/expense/entries/',headers = auth)

    #Expense Entries
    resp = requests.get('https://www.concursolutions.com/api/travel/trip/v1.1',headers = auth)
    return Response(resp.text, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug = True)
