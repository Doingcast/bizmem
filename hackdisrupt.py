from flask import Flask, jsonify, Response
import requests
from requests_oauthlib import OAuth2, OAuth1
import json
from xml.etree import ElementTree
from ConcurOAuthPython import getbasic, getTokenGivenUsernamePasswordAndConsumerKey
from BeautifulSoup import BeautifulSoup
from datetime import datetime, timedelta
#Constants
USER = "user46@concurdisrupt.com"
PWD = "disrupt"
KEY = 'mbGLfEhU1rUUG8IOImdmVt'
#TOKEN = 'NPuB/Wr+a9OkYNWz9Mw/kWNWvyk='
SAMPLE_REPORT_NAME = 'Disrupt Hackathon NYC Trip'
SAMPLE_REPORT_ID = 'D7E30A5A1E1F4ACF82FE'

#Initializing FLASK app
app = Flask(__name__)

#Getting the Current TOKEN
TOKEN = getTokenGivenUsernamePasswordAndConsumerKey('user46@concurdisrupt.com', 'disrupt', KEY)['Access_Token']['Token']

#oauth
auth = {
    'Authorization': "OAuth %s" %  TOKEN,
    'Accept':'application/xml',
    'lastModifiedDate': '2001-01-01' #This will get older itinerariesk
    }

@app.route('/')
def itineraries():
    """
     Returns all itineraries
    """
    resp = requests.get('https://www.concursolutions.com/api/travel/trip/v1.1',headers = auth)
    return Response(resp.text, mimetype='application/xml')

@app.route('/itinerary/info')
def itinerary_info():
    """
     Returns all itineraries
    """
    TripID = 'nHyQT$pcgFtPlchwTlyhTG$pjyel9xI$sVJ9OTTrUw'
    resp = requests.get('https://www.concursolutions.com/api/travel/trip/v1.1/%s' % TripID,headers = auth)
    root = BeautifulSoup(resp.text)
    for booking in root.bookings.findAll('booking'):
        for air in booking.findAll('air'):
            resp = """
        <div>
            <ul><li><strong>Flight</strong></li></ul>
        </div>
        <div>%s -&gt; %s</div>
        <div><en-todo/> arrive on %s by %s</div>
        <div><en-todo/> takeoff is at %s</div>
        <hr></hr>
            """ % (
                air.startcitycode.text,
                air.endcitycode.text,
                air.startcitycode.text,
                (datetime.strptime(air.startdatelocal.text, '%Y-%m-%dT%H:%M:%S') - timedelta(hours=3)).strftime("%m/%d - %H:%M"),
                datetime.strptime(air.startdatelocal.text, '%Y-%m-%dT%H:%M:%S').strftime("%H:%M"),
                )
    return Response(resp.text, mimetype='application/xml')

@app.route('/entries/')
def entries():
    """
     Returns all expense entries
    """

    #Expense Entries
    headers = auth
    headers['']
    resp = requests.get('https://www.concursolutions.com/api/v3.0/expense/entries/',headers = auth)
    return Response(resp.text, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug = True)
