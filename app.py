import json, config
import re
from flask import Flask,request,jsonify
app = Flask(__name__)
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET)
coins = {
    "ETHUSDT":"None",
    "BTCUSDT":"None",
    "ADAUSDT":"None",
    "DOGEUSDT":"None",
}
lavs = {
    "ETHUSDT":20,
    "BTCUSDT":20,
    "ADAUSDT":20,
    "DOGEUSDT":20,
}
def order(coin,amount,leverage,position):
    if coins[coin] != position :
        try:
            result = request_client.change_margin_type(coin, marginType=FuturesMarginType.ISOLATED)
            print("Margin Type: " + result)
        except Exception as e:
            print("an exception occured - {}".format(e))
        try:
            result = request_client.cancel_all_orders(coin)
            print("Order cancel: " + result)
        except Exception as e:
            print("an exception occured - {}".format(e))
        try:
            result = request_client.change_initial_leverage(coin, leverage)
            print("Leverage: " + result)
        except Exception as e:
            print("an exception occured - {}".format(e))
    return True
@app.route('/')
def main_view():
    return 'Hello from loseb k.!'
@app.route('/tradehook',methods=['POST'])
def webhook():
    resData = json.loads(request.data)
    order_response = order(resData['coin'],resData['quantity'],resData['leverage'],resData['positionSide'])
    print(order_response)
    print(resData)
    if resData['passkey'] != config.WEBHOOK_PASS:
        return {
            "code":"error",
            "message":"Invalid"
        }
    return {
        "code":"success",
        "message" : "We are good here"
    } 
    
"""
 
import config
from binance_f import RequestClient
from binance_f.constant.test import *
from binance_f.base.printobject import *
from binance_f.model.constant import *

request_client = RequestClient(api_key=config.API_KEY, secret_key=config.API_SECRET)
result = request_client.get_account_information()
print(result)
print("canDeposit: ", result.canDeposit)
print("canWithdraw: ", result.canWithdraw)
print("feeTier: ", result.feeTier)
print("maxWithdrawAmount: ", result.maxWithdrawAmount)
print("totalInitialMargin: ", result.totalInitialMargin)
print("totalMaintMargin: ", result.totalMaintMargin)
print("totalMarginBalance: ", result.totalMarginBalance)
print("totalOpenOrderInitialMargin: ", result.totalOpenOrderInitialMargin)
print("totalPositionInitialMargin: ", result.totalPositionInitialMargin)
print("totalUnrealizedProfit: ", result.totalUnrealizedProfit)
print("totalWalletBalance: ", result.totalWalletBalance)
print("updateTime: ", result.updateTime)
print("=== Assets ===")
PrintMix.print_data(result.assets)
print("==============")
print("=== Positions ===")
PrintMix.print_data(result.positions)
print("==============") """

""" import json, config
from binance.client import Client
from binance.enums import *
client = Client(config.API_KEY,config.API_SECRET,testnet=True)

account_balance = client.get_asset_balance(asset='USDT')
print(account_balance)
account_trades = client.get_my_trades(symbol='ETHUSDT')
print(account_trades)
account_orders = client.get_all_orders(symbol='ETHUSDT')
print(account_orders)

order = client.futures_create_order(symbol='ETHUSDT', side='BUY', type='MARKET', quantity=10)
print(order)  """