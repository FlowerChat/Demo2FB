#!/usr/bin/env python


import urllib
import json
import os

from flask import Flask, render_template, jsonify
import requests
from key import key
import imghdr
from flask import request
from flask import make_response
#import psycopg2
import datetime





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
    
    if req.get("result").get("action") == "welcome.firstfb":
        #result= req.get("result")
        #contexts=result.get("contexts")
        #generic_con=contexts{"name":"generic"}

        #generic_conparams=generic_con.get("parameters")
    
        #facebook_id=str(generic_conparams.get("facebook_sender_id"))
        #user_id_url="https://graph.facebook.com/v2.6/"+facebook_id+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAARq6hqpYzMBACdg4Y2PXnoc8YlDkKysqZClfKC0X09aZBvklWsoNZAMP00ZCvrnm0O6nT2n1gh7YhDCnYvGWVbpPtzK5ZAa6qsjm98ZCZCmnmbc0hDZBBz6WGCSBCQ3Vm4FYnZBkyJdkbdHjZCHh98VOn8tM64Lyqvik3o2l23OfGIgZDZD"
        #user_req=requests.get(user_id_url)
        #user_json=user_req.json()
        #facebook_user_firstname=user_json["first_name"]
        
        TimeStamp=str(datetime.datetime.utcnow())
        

        speech = TimeStamp
        
        print("Response:")
        print (speech)
        facebook_message = {
            "text": "Hi, "+ TimeStamp +", I am a FlowerChat bot who will help you find the best florist"
        }

        
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":5},{"name":"flowerchatline","facebook_user_first":facebook_user_firstname,"lifespan":100}]
        }
    
        
        
            
    elif req.get("result").get("action") == "input.welcome":
        
    
        TimeStamp=str(datetime.datetime.utcnow())
        

        speech = TimeStamp


        print("Response:")
        print(speech)
        

        facebook_message = {
            "text":"For better service please share your current location:",
            "quick_replies":[
                {
                    "content_type":"location",
                }
            ]
        }
        

        print(json.dumps(facebook_message))
        return {
            #"speech": speech,
            #"displayText": speech,
            "data": {"facebook": facebook_message},
        # "contextOut": [],
            "contextOut": [{"name":"facebook_location", "lifespan":5}]
        }
    elif req.get("result").get("action")=="input.location":
        #import userloc
                
        result = req.get("result")
        contexts=result.get("contexts")
        fblocation=contexts[0]
        conparams=fblocation.get("parameters")
    
        CustLong=str(conparams.get("long"))
        CustLat=str(conparams.get("lat"))
        #generic_con=contexts[3]
        generic_con=contexts{"name":"generic"}

        generic_conparams=generic_con.get("parameters")
    
        facebook_id=str(generic_conparams.get("facebook_sender_id"))
        user_id_url="https://graph.facebook.com/v2.6/"+facebook_id+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAARq6hqpYzMBACdg4Y2PXnoc8YlDkKysqZClfKC0X09aZBvklWsoNZAMP00ZCvrnm0O6nT2n1gh7YhDCnYvGWVbpPtzK5ZAa6qsjm98ZCZCmnmbc0hDZBBz6WGCSBCQ3Vm4FYnZBkyJdkbdHjZCHh98VOn8tM64Lyqvik3o2l23OfGIgZDZD"
        user_req=requests.get(user_id_url)
        user_json=user_req.json()
        facebook_user_firstname=user_json["first_name"]
        
           
        
        speech="test"
        
        
        print("Response:")
        print speech
        facebook_message = {
            "text": "Your current location is " + CustLong  +" " + CustLat+" hello "+facebook_user_firstname
        }
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":5},{"name":"flowerchatline","facebook_user_first":facebook_user_firstname,"lifespan":100}]
        }

        
    return {}
    

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
app.run(debug=True, port=port, host='0.0.0.0')