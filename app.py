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
    
    if req.get("result").get("action") == "firstfb":
        result= req.get("result")
        contexts=result.get("contexts")
        generic_con=contexts[1]

        generic_conparams=generic_con.get("parameters")
    
        facebook_id=str(generic_conparams.get("facebook_sender_id"))
        user_id_url="https://graph.facebook.com/v2.6/"+facebook_id+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAARq6hqpYzMBACdg4Y2PXnoc8YlDkKysqZClfKC0X09aZBvklWsoNZAMP00ZCvrnm0O6nT2n1gh7YhDCnYvGWVbpPtzK5ZAa6qsjm98ZCZCmnmbc0hDZBBz6WGCSBCQ3Vm4FYnZBkyJdkbdHjZCHh98VOn8tM64Lyqvik3o2l23OfGIgZDZD"
        user_req=requests.get(user_id_url)
        user_json=user_req.json()
        facebook_user_firstname=user_json["first_name"]
        
        TimeStamp=str(datetime.datetime.utcnow())
        

        speech = TimeStamp
        
        print("Response:")
        print speech
        facebook_message = {
            "attachment":{
                "type":"template",
                "payload":{
                    "template_type":"generic",
                    "elements":[
                        
                        
                        {
                            "title":"Hi, "+ facebook_user_firstname +", I can help you find the best local flower shop",                            
                            "image_url":"http://www.fiorita.cz/wp-content/uploads/2017/03/kvetinarstvi-praha-jarni-kytice-tulipany-anemony-pryskyrniky.jpg",
                            "subtitle":"This bouquet was tied by my sponsors. You can order flowers through their web",
                            #}
                        
                            "buttons":[
                                {
                                    "type":"web_url",
                                    "url":"http://www.fiorita.cz",
                                    "title":"View sponsor's web"
                                                                  
                                },{                                  
                                    "type":"postback",
                                    "title":"Start Chatting",
                                    "payload":"Yes, please"
                                },{
                                    "type":"postback",
                                    "title":"Quit",
                                    "payload":"No, thanks"
                                }
                            ]              
                        }      
                        
                    ]
                }
            }
        }

        
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":0}]
        }
    
        
        
            
    elif req.get("result").get("action") == "ask.location":
        
    
        #TimeStamp=str(datetime.datetime.utcnow())
        

        #speech = TimeStamp


        print("Response:")
        #print(speech)
        

        facebook_message = {
            "text":"You have chosen pick-up service from a local florist. For better service please share your current location:",
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
            "contextOut": [{"name":"facebook_location", "lifespan":0}]
        }
    elif req.get("result").get("action")=="input.location":
        #import userloc
                
        result = req.get("result")
        contexts=result.get("contexts")
        fblocation=contexts[0]
        conparams=fblocation.get("parameters")
    
        CustLong=str(conparams.get("long"))
        CustLat=str(conparams.get("lat"))
        CustLoc=CustLat+","+CustLong
        #generic_con=contexts[3]
        generic_con=contexts[2]

        generic_conparams=generic_con.get("parameters")
    
        facebook_id=str(generic_conparams.get("facebook_sender_id"))
        user_id_url="https://graph.facebook.com/v2.6/"+facebook_id+"?fields=first_name,last_name,profile_pic,locale,timezone,gender&access_token=EAARq6hqpYzMBACdg4Y2PXnoc8YlDkKysqZClfKC0X09aZBvklWsoNZAMP00ZCvrnm0O6nT2n1gh7YhDCnYvGWVbpPtzK5ZAa6qsjm98ZCZCmnmbc0hDZBBz6WGCSBCQ3Vm4FYnZBkyJdkbdHjZCHh98VOn8tM64Lyqvik3o2l23OfGIgZDZD"
        user_req=requests.get(user_id_url)
        user_json=user_req.json()
        facebook_user_firstname=user_json["first_name"]
        search_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        photos_url = "https://maps.googleapis.com/maps/api/place/photo"
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        amp = str("&")
        ques= str("?")
        photo_ref = str("photoreference=")
        photo_width=str("maxwidth=1600")
        key_eq=str("key=")
        key_str=str(key)
        #str_address="florist at"+str(address)
    
    #trying to retrieve pics
    
        search_payload = {"key":key, "location":CustLoc, "radius": 5000, "type": "florist"}
        search_req = requests.get(search_url, params=search_payload)
        search_json = search_req.json()
        gplace_id=search_json["results"][0]["place_id"]
        gplace_id2=search_json["results"][1]["place_id"]
        gplace_id3=search_json["results"][2]["place_id"]
        details_payload={"key":key, "placeid":gplace_id}
        details_payload2={"key":key, "placeid":gplace_id2}
        details_payload3={"key":key, "placeid":gplace_id3}
        details_req=requests.get(details_url, params=details_payload)
        details_req2=requests.get(details_url, params=details_payload2)
        details_req3=requests.get(details_url, params=details_payload3)
        details_json=details_req.json()
        details_json2=details_req2.json()
        details_json3=details_req3.json()


    
   # photo id of businesses 
    
        photo_id = details_json["result"]["photos"][0]["photo_reference"]
        photo_id2=details_json2["result"]["photos"][0]["photo_reference"]
        photo_id3=details_json3["result"]["photos"][0]["photo_reference"]
        
   # name of businesses
   
        name_shop1=details_json["result"]["name"]
        name_shop2=details_json2["result"]["name"]
        name_shop3=details_json3["result"]["name"]
        
   # addresses and tel of businesses
   
        phone_shop1=details_json["result"]["international_phone_number"]
        phone_shop2=details_json2["result"]["international_phone_number"]
        phone_shop3=details_json3["result"]["international_phone_number"]
        form_add1=details_json["result"]["formatted_address"]
        form_add2=details_json2["result"]["formatted_address"]
        form_add3=details_json3["result"]["formatted_address"]
    

   


# do not remember
    
        photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
        photo_request = requests.get(photos_url, params=photo_payload)
   
    # final pictures to be shown to the user
    
        final_pic=photos_url+ques+photo_width+amp+photo_ref+photo_id+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"
        final_pic2=photos_url+ques+photo_width+amp+photo_ref+photo_id2+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"
        final_pic3=photos_url+ques+photo_width+amp+photo_ref+photo_id3+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"

           
        
        speech="test"
        
        
        print("Response:")
        print speech
        
        #What we see
        
        facebook_message = {
           # "attachment": {
           #     "type":"image",
           #     "payload":{
           #         "url": final_pic
           #     }
           # }
        #}
            "attachment": {
            "type": "template",
            "payload": {
                "template_type": "list",
                "elements": [
                    {
                        "title": name_shop1,
                        "image_url": final_pic,
                        "subtitle": form_add1,
                        #"default_action": {
                        #   "type": "web_url",
                        #   "url": "https://peterssendreceiveapp.ngrok.io/shop_collection",
                        #   "messenger_extensions": true,
                        #   "webview_height_ratio": "tall",
                        #   "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                        #    },
                        "buttons":[
                            {
                                "title": "Call me",
                                "type": "phone_number",
                                "payload":phone_shop1                        
                            }
                        ]
                    },
                    {
                        "title": name_shop2,
                        "image_url": final_pic2,
                        "subtitle": form_add2,
                        #"default_action": {
                        #    "type": "web_url",
                        #    "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
                        #    "messenger_extensions": true,
                        #    "webview_height_ratio": "tall",
                        #    "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                        #},
                        "buttons": [
                            {
                                "title": "Call me",
                                "type": "phone_number",
                                "payload": phone_shop2
                                                 
                            }
                        ]                
                    },
                    {
                        "title": name_shop3,
                        "image_url": final_pic3,
                        "subtitle": form_add3,
                        #"default_action": {
                        #    "type": "web_url",
                        #    "url": "https://peterssendreceiveapp.ngrok.io/view?item=100",
                        #    "messenger_extensions": true,
                        #    "webview_height_ratio": "tall",
                        #    "fallback_url": "https://peterssendreceiveapp.ngrok.io/"
                        #},
                        "buttons": [
                            {
                                "title": "Call me",
                                "type": "phone_number",
                                "payload": phone_shop3
                                                 
                            }
                        ]                
                    }
                
                
                ],
                "buttons": [
                    {
                        "title": "View More",
                        "type": "postback",
                        "payload": "More examples"                        
                    }
                ]  
            }
        
        }
    }           
                    
     #"Your current location is " + CustLong  +" " + CustLat+" hello "+facebook_user_firstname
     #   }
        print(json.dumps(facebook_message))
        return {
            "data":{"facebook":facebook_message},
            "contextOut": [{"name":"facebook_location", "lifespan":0},{"name":"generic","lifespan":0},{"name":"flowerchatline","facebook_user_first":facebook_user_firstname,"lifespan":100}]
        }
    elif req.get("result").get("action")=="search.florist":
        search_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        photos_url = "https://maps.googleapis.com/maps/api/place/photo"
        details_url = "https://maps.googleapis.com/maps/api/place/details/json"
        amp = str("&")
        ques= str("?")
        photo_ref = str("photoreference=")
        photo_width=str("maxwidth=1600")
        key_eq=str("key=")
        key_str=str(key)
        str_address="florist at"+str(address)
    
    #trying to retrieve pics
    
        search_payload = {"key":key, "query":str_address, "radius": 10000}
        search_req = requests.get(search_url, params=search_payload)
        search_json = search_req.json()
        gplace_id=search_json["results"][0]["place_id"]
        gplace_id2=search_json["results"][1]["place_id"]
        details_payload={"key":key, "placeid":gplace_id}
        details_payload2={"key":key, "placeid":gplace_id2}
        details_req=requests.get(details_url, params=details_payload)
        details_req2=requests.get(details_url, params=details_payload2)
        details_json=details_req.json()
        details_json2=details_req2.json()


    
    #webadd=details_json["result"]["website"]
    #webadd_str=str(webadd)
    
        photo_id = details_json["result"]["photos"][1]["photo_reference"]
        photo_id2=details_json2["result"]["photos"][1]["photo_reference"]
        name_shop1=details_json["result"]["name"]
        name_shop2=details_json2["result"]["name"]
        phone_shop1=details_json["result"]["international_phone_number"]
        phone_shop2=details_json2["result"]["international_phone_number"]
        form_add1=details_json["result"]["formatted_address"]
        form_add2=details_json2["result"]["formatted_address"]
    

    #website0=details_json["result"]["website"]
    #website1=details_json2["result"]["website"]
    #hwebsite0="http://"+website0
    #hwebsite1="http://"+website1



    #photo_id = search_json["results"][0]["photos"][0]["photo_reference"]
    #photo_link=photos_url+"?maxwidth=1600"+"&"+"photoreference="+photo_id+"&"+key
    
        photo_payload = {"key" : key, "maxwidth": 1600, "maxhight": 1600, "photoreference" : photo_id}
        photo_request = requests.get(photos_url, params=photo_payload)
    #final_pic=str(photo_request)
    
        final_pic=photos_url+ques+photo_width+amp+photo_ref+photo_id+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"
        final_pic2=photos_url+ques+photo_width+amp+photo_ref+photo_id2+amp+key_eq+"AIzaSyD8pgLKrEDnUYBoGVvpw0B4dT4qAyHaRXg"



        
    return {}
    

    



if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port
app.run(debug=True, port=port, host='0.0.0.0')