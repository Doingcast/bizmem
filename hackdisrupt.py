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
def itinerary_info(TripID = 'nHyQT$pcgFtPlchwnqtoRjd1MgMLqRPunn4pQShg'):
    """
     Returns all itineraries
    """
    #TripID = 'nHyQT$pcgFtPlchwTlyhTG$pjyel9xI$sVJ9OTTrUw'
    resp = requests.get('https://www.concursolutions.com/api/travel/trip/v1.1/%s' % TripID,headers = auth)
    root = BeautifulSoup(resp.text)
    note=""
    for booking in root.bookings.findAll('booking'):
        for air in booking.findAll('air'):
            note += """
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
    note += """
        <div>
            <ul><li><strong>Hotel</strong></li></ul>
        </div>
        <div>You're staying at:</div>
        <div>%s</div>
        <hr></hr>
            """ % (
                root.bookings.findAll('booking')[0].hotel.find('name').text,
                )
    #Counting number of Taxi Cabs
    resp = requests.get('https://www.concursolutions.com/api/v3.0/expense/entries/',headers = auth)
    root = BeautifulSoup(resp.text)
    cont_cabs = 0
    for t in root.findAll('expensetypecode'):
        if t.text == 'TAXIX':
            cont_cabs = cont_cabs + 1
    note += """
        <div>
            <ul><li><strong>Taxi</strong></li></ul>
        </div>
        <div>The last time you've been there you used %s taxi cabs.</div>
        <div><en-todo/> Download <a href="http://www.uber.com/">Uber</a> (it works the best in %s)</div>
        <hr></hr>
        """% (
        cont_cabs,
        'NYC',
    )
    return note
    #return Response(resp.text, mimetype='application/xml')

@app.route('/itinerary/all')
def all_itinerary_info():
    resp = requests.get('https://www.concursolutions.com/api/travel/trip/v1.1',headers = auth)
    root = BeautifulSoup(resp.text)
    note = ""
    for i in root.findAll("itineraryinfo"):
        note += itinerary_info(i.tripid.text)

    return note

@app.route('/entries/')
def entries():
    """
     Returns all expense entries
    """
    #Expense Entries
    resp = requests.get('https://www.concursolutions.com/api/v3.0/expense/entries/',headers = auth)
    return Response(resp.text, mimetype='application/xml')

if __name__ == '__main__':
    app.run(debug = True)
