import asyncio
import websockets
import json

with open('config.json') as f:
    config = json.load(f)


async def auth(websocket, config):
    msga = \
        {
            "jsonrpc": "2.0",
            "id": 9929,
            "method": "public/auth",
            "params": {
                "grant_type": "client_credentials",
                "client_id": config['client_id'],
                "client_secret": config['client_secret']
            }
        }
    await websocket.send(json.dumps(msga))
    res = await websocket.recv()
    return res


class Order:
    def __init__(self, quantity, ty, price, side):
        self.quantity = quantity
        self.ty = ty
        self.price = price
        self.side = side
        self.triggered = False
        self.id = 0

    async def send(self, websocket):
        msg = \
            {
                "jsonrpc": "2.0",
                "id": 5275,
                "method": f"private/{self.side}",
                "params": {
                    "instrument_name": config['instrument_name'],
                    "amount": self.quantity,
                    "type": self.ty,
                    "price": self.price,

                }
            }
        await websocket.send(json.dumps(msg))
        res = await websocket.recv()
        return res

    def update(self, res):
        res["result"]


class Account:

    def __init__(self):
        self.postions = []
        self.open_orders = []

    async def update(self, websocket, config):

        # update postions
        msg_psotions = \
            {
                "jsonrpc": "2.0",
                "id": 2236,
                "method": "private/get_positions",
                "params": {
                    "currency": config['currency'],
                    # "kind": "future"
                }
            }
        await websocket.send(json.dumps(msg_psotions))
        response = await websocket.recv()
        res = json.loads(response)
        self.postions = []
        for position in res["result"]:
            self.postions += [
                {
                    "average_price": position["average_price"],
                    "direction": position["direction"],
                    "instrument_name": position['instrument_name'],
                    "size": position["size"],
                }
            ]
        # update postions
        msg_open_orders = \
            {
                "jsonrpc": "2.0",
                "id": 1953,
                "method": "private/get_open_orders_by_currency",
                "params": {
                    "currency": config["currency"]
                }
            }
        await websocket.send(json.dumps(msg_open_orders))
        response = await websocket.recv()
        res = json.loads(response)
        self.open_orders = []
        for open_order in res["result"]:
            self.open_orders += [
                {
                    "time_in_force": open_order["time_in_force"],
                    "reduce_only": open_order["reduce_only"],
                    "profit_loss": open_order["profit_loss"],
                    "price": open_order["price"],
                    "post_only": open_order["post_only"],
                    "order_type": open_order["order_type"],
                    "order_state": open_order["order_state"],
                }
            ]


class Book:
    def __init__(self, depth):
        self.depth = depth
        self.best_bid_price = 0.0,
        self.best_bid_amount = 0,
        self.best_ask_price = 0.0,
        self.best_ask_amount = 0,
        self.bids = [[0.0, 0]]*self.depth
        self.asks = [[0.0, 0]]*self.depth

    async def update(self, websocket, config):

        # update the order book

        msg_book = \
            {
                "jsonrpc": "2.0",
                "id": 8772,
                "method": "public/get_order_book",
                "params": {
                    "instrument_name": config['instrument_name'],
                    "depth": self.depth
                }
            }
        await websocket.send(json.dumps(msg_book))
        response = await websocket.recv()
        res = json.loads(response)
        self.best_bid_price = res['result']["best_bid_price"]
        self.best_bid_amount = res['result']["best_bid_amount"]
        self.best_ask_price = res['result']["best_ask_price"]
        self.best_ask_amount = res['result']["best_ask_amount"]
        self.bids = res['result']["bids"]
        self.asks = res['result']["asks"]

