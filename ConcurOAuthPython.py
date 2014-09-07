#from https://gist.github.com/Trudeaucj/09c25e79c332e93703a0
import requests
import json
import base64

baseUrl = 'https://www.concursolutions.com'
oauthUrl = baseUrl+'/net2/oauth2/accesstoken.ashx'
reportDigestUrl = ''

def getbasic(user, password):
    # basic authentication (according to HTTP)
    return base64.encodestring(user + ":" + password)


def getTokenGivenUsernamePasswordAndConsumerKey(username, password, consumerKey):
    """
    Given:
        String username (Concur username)
        String password (Concur password)
        String ConsumerKey (Registered partner applciation consumerKey)

    Example:
        Python dictionary of the Oauth Response:
        getTokenGivenUsernamePasswordAndConsumerKey('example@concur.com', '12345', 'ConsumerKey')
        {u'Access_Token': {u'Expiration_date': u'5/7/2015 10:17:14 PM', u'Token': u'NhYhZsP1zK1sARLHkWqSJpwfBIw=',
        u'Instance_Url': u'https://www.concursolutions.com/', u'Refresh_Token': u's9Scoa2GdFkjQYFRgsXKrdcwJBrgIan'}}

        You can then save this token and use it in the headers of your HTTP calls with the parameter:
        Authorization: OAuth {Token}

    """
    basic = 'Basic ' + getbasic(username, password)
    headers1 = {'Authorization': basic.rstrip(), 'X-ConsumerKey': consumerKey, 'Accept':'application/json'}
    r = requests.get(oauthUrl, headers=headers1)
    return json.loads(r.content)

if __name__ == '__main__':
    print getTokenGivenUsernamePasswordAndConsumerKey('user46@concurdisrupt.com', 'disrupt', 'mbGLfEhU1rUUG8IOImdmVt')['Access_Token']['Token']