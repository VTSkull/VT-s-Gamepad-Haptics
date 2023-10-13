import os,json,threading,time
os.environ['SDL_JOYSTICK_HIDAPI_PS4_RUMBLE'] = '1'
import pygame as pg
from typing import List, Any
os.system('cls')
#initialize pygame
pg.init()
pg.joystick.init()

#setup pygame
screen = pg.display.set_mode((400, 720))
pg.display.set_caption("VT's gamepad haptics")
clock = pg.time.Clock()

#joysticks
joysticks = [pg.joystick.Joystick(i) for i in range(pg.joystick.get_count())]

#image/data stuff
main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "assets")
pygame_icon = pg.image.load('assets/ps4.png')
pg.display.set_icon(pygame_icon)

#colors
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

#text
font = pg.font.Font('freesansbold.ttf', 20)

#variables
contactValues = []
contactBinds = {}
contactBindsKeys = []
contactBindsValues = []
spacing = 90
enabled = True
running = True
joyConValues = []
joyConPositions = []


#get contact binds
with open("ContactBinds.json","r") as file:
    contactBinds = json.load(file)
    file.close()

for x in contactBinds:
    contactValues.append(0.0)

#update Contact Binds Keys and Values
contactBindsKeys = list(contactBinds.keys())
contactBindsValues = list(contactBinds.values())

#get joysticks
for joystick in joysticks:
    if joystick.get_name() == "Nintendo Switch Joy-Con (L/R)":
        joyConValues.append(0.0)
        joyConValues.append(0.0)
        joyConPositions.append(joysticks.index(joystick))
    print(joystick.get_name())    
pg.joystick.Joystick

#load images
def load_image(name, colorkey=None, scale=1):
    fullname = os.path.join(data_dir, name)
    image = pg.image.load(fullname)

    size = image.get_size()
    size = (size[0] * scale, size[1] * scale)
    image = pg.transform.scale(image, size)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pg.RLEACCEL)
    return image, image.get_rect()

#button class
objects = []
class Button():
    def __init__(self, x, y, width, height, buttonText='Button', onclickFunction=None, onePress=False, args=[], thread=False, joyCon=False, usedJoyCon=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onclickFunction = onclickFunction
        self.onePress = onePress
        self.alreadyPressed = False
        self.argument = args
        self.thread = thread
        self.joyCon = joyCon
        self.usedJoyCon = usedJoyCon
        self.fillColors = {
            'normal': '#aaaaaa',
            'hover': '#666666',
            'pressed': '#333333',
        }
        self.buttonSurface = pg.Surface((self.width, self.height))
        self.buttonRect = pg.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, (20, 20, 20))
        objects.append(self)

    def process(self):
        mousePos = pg.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pg.mouse.get_pressed(num_buttons=3)[0]:
                self.buttonSurface.fill(self.fillColors['pressed'])
                if self.onePress:
                    
                    #do function
                    if self.thread:
                        if self.argument == None:
                            x = threading.Thread(target=self.onclickFunction, daemon=True)
                        else:
                            x = threading.Thread(target=self.onclickFunction, args=(self.argument, self.joyCon, self.usedJoyCon), daemon=True)
                        x.start()
                    else:
                        if self.argument == None:
                            self.onclickFunction()
                        else:
                            elf.onclickFunction(self.argument)
                            
                elif not self.alreadyPressed:
                    #do function
                    if self.thread:
                        if self.argument == None:
                            x = threading.Thread(target=self.onclickFunction, daemon=True)
                        else:
                            x = threading.Thread(target=self.onclickFunction, args=(self.argument, self.joyCon, self.usedJoyCon), daemon=True)
                        x.start()
                    else:
                        if self.argument == None:
                            self.onclickFunction()
                        else:
                            elf.onclickFunction(self.argument)
                            
                    self.alreadyPressed = True
                    
            else:
                self.alreadyPressed = False
        self.buttonSurface.blit(self.buttonSurf, [
            self.buttonRect.width/2 - self.buttonSurf.get_rect().width/2,
            self.buttonRect.height/2 - self.buttonSurf.get_rect().height/2
        ])
        screen.blit(self.buttonSurface, self.buttonRect)

#viberate button function
def Viberate(controllerNum, joycon, usedJoycon):
    global contactValues, joyConValues
    if joycon:
        joyConValues[usedJoycon] = 0.5
        contactValues[controllerNum+usedJoycon] = 0.5
        print("set joycon value")
        time.sleep(1)
        joyConValues[usedJoycon] = 0.0
        contactValues[controllerNum+usedJoycon] = 0.0
        print(contactValues)
    else:
        contactValues[controllerNum] = 0.5
        time.sleep(1)
        contactValues[controllerNum] = 0.0

#toggle haptics function
def ToggleHaptics():
    global enabled
    if enabled:
        enabled = False
    else:
        enabled = True

#set up buttons
for x in range(len(joysticks)):
    if joysticks[x].get_name() != "Nintendo Switch Joy-Con (L/R)":
        Button(50, (spacing*x)+spacing, 300, 35, 'Vibrate', Viberate, args=x, thread=True)
for x in range(len(joyConPositions)):
    for y in [0,1]:
        Button(50, (spacing*(y+(len(joysticks)-1))+spacing), 300, 35, 'vibrate', Viberate, args=joyConPositions[x], joyCon=True, usedJoyCon=y, thread=True)
Button(201, 1, 198, 35, 'Toggle Haptics', ToggleHaptics, args=None)
    
#OSC receiver thread
def OSC():
    global contactValues
    print("thread started")
    from pythonosc.dispatcher import Dispatcher
    dispatcher = Dispatcher()
    
    #haptics function
    def UpdateHaptics(address: str, *args: List[Any]) -> None:
        value1 = args[0]
        addressList = address.split('/')
        if addressList[-1] not in contactBindsKeys:
            return

        #print(contactBindsValues)
        if contactBindsValues[contactBindsKeys.index(addressList[-1])][:2] == "ns":
            joyConValues[int(contactBindsValues[contactBindsKeys.index(addressList[-1])][2:])] = value1
            
        contactValues[contactBindsKeys.index(addressList[-1])] = value1
        print(contactValues)

    #start server
    dispatcher.map("/avatar/parameters/*", UpdateHaptics)
    from pythonosc.osc_server import BlockingOSCUDPServer
    server = BlockingOSCUDPServer(("127.0.0.1", 9001), dispatcher)
    server.serve_forever()

#start OSC receiver thread
oscThread = threading.Thread(target=OSC, daemon=True)
oscThread.start()

#OSC chatbox setup
chatbox = True
def ToggleChatbox():
    global chatbox
    if chatbox:
        chatbox = False
    else:
        chatbox = True
Button(1, 1, 199, 35, 'Toggle Chatbox', ToggleChatbox, args=None)

#OSC chatbox thread
def chatbox():
    from pythonosc import udp_client
    client = udp_client.SimpleUDPClient("127.0.0.1", 9000)
    while True:
        if chatbox:
            if enabled:
                client.send_message("/chatbox/input", ["VT's Gamepad Haptics: Enabled", True, False])
            else:
                client.send_message("/chatbox/input", ["VT's Gamepad Haptics: Disabled", True, False])
        time.sleep(2)

#start chatbox thread
chatboxThread = threading.Thread(target=chatbox, daemon=True)
chatboxThread.start()

#main loop
while running:

    #quit the program
    try:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
    except:
        pass

    screen.fill("white")

    for object in objects:
        object.process()
        
    #for each controller
    for x in range(len(joysticks)+len(joyConValues)-1):
        if contactValues[x] > 0:
            if enabled:
                print(joyConValues)
                if contactBindsValues[x][:2] == "ns":
                    if joyConValues[0] != 0.0 and joyConValues[1] != 0.0:
                        joysticks[joyConPositions[0]].rumble(joyConValues[0],joyConValues[1],0)
                    elif joyConValues[0] != 0.0:
                        joysticks[joyConPositions[0]].rumble(joyConValues[0],0,0)
                    elif joyConValues[1] != 0.0:
                        joysticks[joyConPositions[0]].rumble(0,joyConValues[1],0)
                    else:
                        joysticks[joyConPositions[0]].stop_rumble()
                        
                else:
                    joysticks[x].rumble(contactValues[x],0.1,0)
            else:
                if joysticks[x].get_name() != "Nintendo Switch Joy-Con (L/R)":
                    joysticks[x].stop_rumble()
        #else:
        #    joysticks[x].stop_rumble()
        try:
            if joysticks[x].get_name() == "PS4 Controller":
                screen.blit(load_image("ps4.png",scale=0.1)[0],(10,(spacing*x)+spacing/2))
            elif joysticks[x].get_name() == "Nintendo Switch Joy-Con (L)":
                screen.blit(load_image("Ljoycon.png",scale=0.15)[0],(-8,((spacing*x)+spacing/2)-10))
            elif joysticks[x].get_name() == "Nintendo Switch Joy-Con (R)":
                screen.blit(load_image("Rjoycon.png",scale=0.15)[0],(-8,((spacing*x)+spacing/2)-10))
            elif joysticks[x].get_name() == "Nintendo Switch Joy-Con (L/R)":
                screen.blit(load_image("Ljoycon.png",scale=0.15)[0],(-8,((spacing*x)+spacing/2)-10))
        except:
            screen.blit(load_image("Rjoycon.png",scale=0.15)[0],(-8,((spacing*x)+spacing/2)-10))
        #display the info
        text = font.render(str(contactValues[x]), True, "black")
        screen.blit(text,(80,((spacing*x)+20)+spacing/2))
        text = font.render(str(contactBindsKeys[x]), True, "black")
        screen.blit(text,(70,(spacing*x)+spacing/2))


    pg.display.flip()
    clock.tick(60)  # limits FPS to 60

pg.quit()
