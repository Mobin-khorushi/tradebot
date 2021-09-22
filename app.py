import json, config
import re
from flask import Flask,request,jsonify
app = Flask(__name__)
from binance.client import Client
from binance.enums import *
client = Client(config.API_KEY,config.API_SECRET,tld='us')

def order(side,quantity,symbol,order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol,side=side,type=order_type,quantity=quantity)
        print(order)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False
    return True
@app.route('/')
def main_view():
    return 'Hello from loseb k.!'

@app.route('/tradehook',methods=['POST'])
def webhook():
    
    resData = json.loads(request.data)
    side = resData['strategy']['order_action'].upper()
    order_response = order("BUY",100,"DOGEUSD")
    print(order_response)
    print(side)
    if resData['passphrase'] != config.WEBHOOK_PASS:
        return {
            "code":"error",
            "message":"Invalid"
        }
    return {
        "code":"success",
        "message" : resData
    }