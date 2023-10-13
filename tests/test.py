import argparse, time, os
from datetime import datetime
from pythonosc import udp_client

os.system('cls')
parser = argparse.ArgumentParser()
parser.add_argument("--ip", default="127.0.0.1",
      help="The ip of the OSC server")
parser.add_argument("--port", type=int, default=9001,
      help="The port the OSC server is listening on")
args = parser.parse_args()
client = udp_client.SimpleUDPClient(args.ip, args.port)

#send = input("")
for x in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]:
    client.send_message("/avatar/parameters/RightThighHapticGeneral", x)
    time.sleep(0.2)


#for x in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,0.8,0.7,0.6,0.5,0.4,0.3,0.2,0.1,0.0]:
#    client.send_message("/avatar/parameters/TummyHapticGeneral", x)
#    time.sleep(0.2)
