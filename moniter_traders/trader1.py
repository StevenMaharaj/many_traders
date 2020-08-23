import numpy as np

import asyncio

import asyncio
import websockets

async def hello():
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        trader_no = 1
        await websocket.send(f"trader {trader_no} has logged on")
        while websocket.open:
            while True:
                action = np.random.choice(["BUY","SELL"])
                await websocket.send(f"Trader {trader_no} makes a {action} order")

                await asyncio.sleep(1)
            

asyncio.get_event_loop().run_until_complete(hello())