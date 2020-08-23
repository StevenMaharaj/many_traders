For this to run you will numpy and asyncio, websockets

First run

```python
python monitor.py

```
This should start a server

Next run in a separate terminals

```python
python trader1.py

```

```python
python trader2.py

```

 - Traders are the client. Traders should connect to the monitor (server).
 - The monitor should print out the actions of the traders.
