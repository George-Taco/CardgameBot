from pypresence import Presence
import time

client_id = "843288199614431252"  # Enter your Application ID here.

RPC = Presence(client_id=client_id)

RPC.connect()

start_time = time.time()

# Make sure you are using the same name that you used when uploading the image
RPC.update(large_image="pycharm", state="While smashing my keyboard", details="Working on Blackjack.py",
           start=start_time, buttons=[{"label": "Server", "url": "https://discord.gg/fRcbHh2xHg"}])

while 1:
    time.sleep(15)  # Can only update presence every 15 seconds
