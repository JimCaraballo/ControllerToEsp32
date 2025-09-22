import pygame
import serial
import time
import math
import sys

pygame.init()
pygame.joystick.init()

if sys.platform == 'darwin':
    PORT = "/dev/cu.usbserial-0001"
elif sys.platform == 'win32':
    import os # Just for making the code a lil bit cute with colors :3
    os.system('')
    print("\n---------------\nDefault port: 3")
    PORT = "COM5"
elif sys.platform == 'linux':
    PORT = "/dev/ttyUSB0"
else:
    print("Unsupported platform")
    exit()

# Colors for the strings <3
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
RESET = '\033[0m'
decolines = "-" * 100

BAUD = 115200 # Most micros use this serial comunication speed (is standard)

ser = serial.Serial(PORT, BAUD, timeout = 1.0)
time.sleep(2.0)
last_line = None

js = None
if pygame.joystick.get_count() > 0:
    js = pygame.joystick.Joystick(0)
    js.init()
    print(f'{GREEN}Device connected{RESET}')

    # Info of the controller 
    print(f"---------------\nDevice name: {BLUE}{js.get_name()}{RESET}")
    print(f"Buttons number: {js.get_numbuttons()}")
    print(f"Axis number: {js.get_numaxes()}")
    print(f"Hats (D-pads) number: {js.get_numhats()}\n" + decolines)
    
else:
    exit()

def ControllerData(buttons, joystick, axes):

    # read Buttons
    for b in range(joystick.get_numbuttons()):
        buttons[b] = int(joystick.get_button(b))

    # reqd joysticks
    for a in range(joystick.get_numaxes()):
        axes[a] = math.floor(0.005 + joystick.get_axis(a) * 100) / 100.0

    # Checking if the controller have D-pad (hat)
    if joystick.get_numhats() > 0:
        dpad = [joystick.get_hat(0)[0], joystick.get_hat(0)[1]]
    else:
        dpad = [0, 0]
    
    controller_data = [buttons, axes, dpad]
    return controller_data

def to_csv(jsInput):
    parts = []
    parts.append(f"| {RED}Buttons{RESET}")
    parts += [str(b) for b in jsInput[0]]
    parts.append(f"| {RED}Axis{RESET}")
    parts += [str(f"{a:.2f}") for a in jsInput[1]]
    parts.append(f"| {RED}D-Pad{RESET}")
    parts += [str(d) for d in jsInput[2]]
    return ",".join(parts)+"\n"

while True:
    pygame.event.pump()

    for _ in pygame.event.get():
        pass

    b = list(range(js.get_numbuttons()))
    a = list(float(x) for x in range(js.get_numaxes()))

    line = to_csv(ControllerData(b, js, a))

    if line != last_line:
        print(line.strip(), end='\r') # Debug only to see the output
        ser.write(line.encode("utf-8"))
        last_line = line

    pygame.time.Clock().tick(500)