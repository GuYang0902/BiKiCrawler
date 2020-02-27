import websocket
import ssl
import gzip
import time
import datetime
import json
import demjson

def on_message(ws, message):  # 服务器有数据更新时，主动推送过来的数据
    # print(message)
    ret = gzip.decompress(message).decode("utf-8")
    if ('ping' in ret):
        return
    text = demjson.decode(ret)
    print(text)
    for index in range(len(text['tick']['data'])):
        print('ds='+str(text['tick']['data'][index]['ds']))
        print('price='+str(text['tick']['data'][index]['price']))
        print('side='+str(text['tick']['data'][index]['side']))
        print('vol='+str(text['tick']['data'][index]['vol']))
        print('###################分割线#############################')
    # print(text.keys())
    # print('amount='+str(text['tick']['data'][0]['amount']) )
    # print('ds='+str(text['tick']['data'][0]['ds']))
    # print('id='+str(text['tick']['data'][0]['id']))
    # print('price='+str(text['tick']['data'][0]['price']))
    # print('side='+str(text['tick']['data'][0]['side']))
    # print('ts='+str(text['tick']['data'][0]['ts']))
    # print('vol='+str(text['tick']['data'][0]['vol']))

# 程序报错时，就会触发on_error事件
def on_error(ws, error):
    print(error)

# 程序关闭后触发close时间
def on_close(ws):
    print("Connection closed ……")

# 连接到服务器之后就会触发on_open事件
def on_open(ws):
    # ws.send('{"event":"req","params":{"channel":"review"}}') #获取review数据
    # 获取btcusdt
    ws.send('{"event": "sub", "params": {"channel": "market_btcusdt_trade_ticker", "cb_id": "btcusdt", "top": 100}}')

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("wss://wspool.mpuuss.top/kline-api/ws",
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
