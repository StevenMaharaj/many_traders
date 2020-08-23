import json
import asyncio
import websockets
from pprint import pprint


from od import Order, auth, Account,Book

with open('config.json') as f:
    config = json.load(f)


acc_main = Account()


        
    

async def call_api(config,acc):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        ###############
        # Before sending message, make sure that your connection
        # is authenticated (use public/auth call before)
        ###############

        book = Book(depth=5)
        _ = await auth(websocket, config)
    #    o1 = Order(10,"limit",11859.00,'buy')
    #    response = await o1.send(websocket)
    #    pprint(response)
        limit_sell = Order(quantity=10, ty='limit', price = 0.0, side='buy')
        limit_buy = Order(quantity=10, ty='limit', price = 0.0, side='sell')

        old_postion_size = 0
        current_postion_size = 0
        direction = 'zero'
        consolidation =0.05

        # stack first orders orders
        await book.update(websocket,config)
        
        limit_buy.price = book.best_bid_price
        limit_buy.send(websocket)
        limit_buy.price = book.best_bid_price - consolidation
        limit_buy.send(websocket)

        limit_sell.price = book.best_ask_price + consolidation
        limit_sell.send(websocket)
        limit_sell.price = book.best_bid_price + 2*consolidation
        limit_sell.send(websocket)

        while websocket.open:
            await acc.update(websocket,config)
            await book.update(websocket,config)

            if old_postion_size != acc.postions[0]['size']:
                if (acc.postions[0]['direction']=='buy') & (acc.postions[0]['size'] > old_postion_size):
                    # adjust price and buy 
                elif (acc.postions[0]['direction']=='sell') & (acc.postions[0]['size'] > old_postion_size):
                    # adjust price and sell
                elif (acc.postions[0]['direction']=='buy') & (acc.postions[0]['size'] < old_postion_size):
                    # adjust price and sell
                elif (acc.postions[0]['direction']=='sell') & (acc.postions[0]['size'] < old_postion_size):
                    # adjust price and buy


                    


            await asyncio.sleep(0.1)
            print(acc.open_orders)
            print(book.asks)

loop = asyncio.get_event_loop()
# loop.create_task(call_api(config))
# print("senond")
# loop.run_until_complete(call_api(sub))

asyncio.ensure_future(call_api(config,acc_main))
# asyncio.ensure_future(call_api(sub,acc_sub))
loop.run_forever()



