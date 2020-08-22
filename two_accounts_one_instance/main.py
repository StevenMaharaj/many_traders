import json
import asyncio
import websockets
from pprint import pprint


from od import Order, auth, Account

with open('config.json') as f:
    config = json.load(f)

with open('sub.json') as f:
    sub = json.load(f)
acc_main = Account()
acc_sub = Account()

async def call_api(config,acc):
    async with websockets.connect('wss://test.deribit.com/ws/api/v2') as websocket:
        ###############
        # Before sending message, make sure that your connection
        # is authenticated (use public/auth call before)
        ###############
        _ = await auth(websocket, config)
    #    o1 = Order(10,"limit",11859.00,'buy')
    #    response = await o1.send(websocket)
    #    pprint(response)
        acc = Account()

        while websocket.open:
            await acc.update(websocket,config)
            await asyncio.sleep(0.1)
            print(acc.open_orders)

loop = asyncio.get_event_loop()
# loop.create_task(call_api(config))
# print("senond")
# loop.run_until_complete(call_api(sub))

asyncio.ensure_future(call_api(config,acc_main))
asyncio.ensure_future(call_api(sub,acc_sub))
loop.run_forever()



