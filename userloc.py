result = app.req.get("result")
contexts=result.get("contexts")
fblocation=contexts[0]
conparams=fblocation.get("parameters")
    
CustLong=str(conparams.get("long"))
CustLat=str(conparams.get("lat"))
speech="test"
        
        
print("Response:")
print speech
facebook_message = {
    "text": "Your current location is " + CustLong  +" " + CustLat
}
print(json.dumps(facebook_message))
