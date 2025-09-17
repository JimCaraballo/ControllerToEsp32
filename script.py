import pygame
import serial
import time
import math

pygame.init()
pygame.joystick.init()

PORT = "/dev/ttyUSB0"
BAUD = 230400

ser = serial.Serial(PORT, BAUD, timeout=0.0)
time.sleep(1.5)
last_line = None

js = None
if pygame.joystick.get_count() > 0:
    js = pygame.joystick.Joystick(0)
    js.init()
    print("connected")
else:
    exit()

def ControllerData(buttons, joystick, axes):

    for b in range(joystick.get_numbuttons()):
        buttons[b] = int(joystick.get_button(b))


    for a in range(joystick.get_numaxes()):
        axes[a] = math.floor(0.005 + joystick.get_axis(a) * 100) / 100.0

    dpad = [joystick.get_hat(0)[0], joystick.get_hat(0)[1]]
    controller_data = [buttons, axes, dpad]

    return controller_data

def to_csv(jsInput):
    parts = []
    parts.append("B")
    parts += [str(b) for b in jsInput[0]]
    parts.append("A")
    parts += [str(f"{a:.2f}") for a in jsInput[1]]
    parts.append("D")
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
        ser.write(line.encode("utf-8"))
        last_line = line


    pygame.time.Clock().tick(500)