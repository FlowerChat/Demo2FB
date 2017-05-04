#!/usr/bin/env python


import urllib
import json
import os

from flask import Flask, render_template, jsonify
import requests
#from key import key
import imghdr
from flask import request
from flask import make_response
#import psycopg2
import datetime
import apiai

# FB messenger credentials
ACCESS_TOKEN = "EAARq6hqpYzMBAKa5PZBPmWkRUTkJ1KTLcuqPkSVmGAmntKR1AbZBnFTZAZAMonA57ZBTCJsvEImZCr5QpJzBL7K5ntJ3FN9oeeNlKMWqTwZAqBM69YbP5mDI5sGun17mT2OnGqESZC6CtwnezgecZBwW1dm9IgJZCTgb9g2WaMV9j4IQZDZD"

# api.ai credentials
CLIENT_ACCESS_TOKEN = "fd4ac3df66f4414ea8548d9a7a170755"
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():
    # our endpoint echos back the 'hub.challenge' value specified when we setup the webhook
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Verification token mismatch", 403
        return request.args["hub.challenge"], 200

    return 'Hello World (from Flask!)', 200

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    # prepare API.ai request
    req = ai.text_request()
    req.lang = 'en'  # optional, default value equal 'en'
    req.query = message

    # get response from API.ai
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
    reply(sender, response)

    return "ok"


# search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
# photos_url = "https://maps.googleapis.com/maps/api/place/photo"
# details_url = "https://maps.googleapis.com/maps/api/place/details/json"






# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    
    if req.get("result").get("action")=="input.welcome":
        TimeStamp=str(datetime.datetime.utcnow())
            
    

    

        speech = TimeStamp


        print("Response:")
        print(speech)

       # fb_message =
        #    {
           #     "text": TimeStamp
         #   }
        
        

        print(json.dumps(fb_message))
        return {
            "speech": speech,
            "displayText": speech,
           # "data": {"facebook": fb_message},
        # "contextOut": [],
         #   "contextOut": [{"name":"flowerchatline", "lifespan":5},{"name":"choose-florist", "lifespan":1}]
        }
    return {}
    

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
app.run(debug=True, port=port, host='0.0.0.0')