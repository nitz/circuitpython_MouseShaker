import board
from digitalio import DigitalInOut, Direction
import touchio
import usb_hid
from adafruit_hid.mouse import Mouse
import adafruit_dotstar as dotstar
import time
import math

######################### SETTINGS ##############################

moveMouseEverySeconds = 1
moveMouseShakeDistancePixels = 50
moveMouseShakeTimeSeconds = 3

######################### END SETTINGS ##############################

print("Initialization started.")

# RGB LED
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)

# Built in red LED
led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

# Mouse HID device
mouse = Mouse(usb_hid.devices)

# Capacitive touch on D3
touch = touchio.TouchIn(board.D3)

######################### HELPERS ##############################

# Helper to give us a nice color swirl


def wheel(pos):
    # Input a value 0 to 255 to get a color value.
    # The colours are a transition r - g - b - back to r.
    if (pos < 0):
        return (0, 0, 0)
    if (pos > 255):
        return (0, 0, 0)
    if (pos < 85):
        return (int(pos * 3), int(255 - (pos*3)), 0)
    elif (pos < 170):
        pos -= 85
        return (int(255 - pos*3), 0, int(pos*3))
    else:
        pos -= 170
        return (0, int(pos*3), int(255 - pos*3))

# a simple linear interpolation


def lerp(a, b, t):
    return (1 - t) * a + (t * b)

######################### MAIN SETUP ##############################


print("Initialization complete. Starting main loop.")

i = 0
frameTime = time.monotonic()
lastFrameTime = frameTime
nextMouseShake = frameTime + moveMouseEverySeconds
shakeRemaining = 0
shakePixelsHalf = moveMouseShakeDistancePixels / 2
moveEnabled = True
mousePos = 0

######################### MAIN LOOP ##############################

while True:
    frameTime = time.monotonic()
    delta = frameTime - lastFrameTime

    if moveEnabled:
        # a nice rainbow wheel while we are active
        i = (i+1) % 256
        dot[0] = wheel(i & 255)
    else:
        # a soft red flash while we are disabled
        redPercent = (math.sin(frameTime * 6) + 1.0) / 2
        red = lerp(8, 64, redPercent)
        dot[0] = (int(red), 0, 0)

    # use D3 as capacitive touch to turn on internal LED,
    # and enable or disable the move feature.
    led.value = touch.value
    if touch.value:
        moveEnabled = not moveEnabled
        time.sleep(0.2)  # a shitty debounce
        if moveEnabled:
            # re-init our shake variable state,
            # but go ahead and have the next move be now.
            nextMouseShake = frameTime
            shakeRemaining = 0

    if moveEnabled:
        # if we are currently shaking, update our shake
        if (shakeRemaining > 0):
            shakeRemaining -= delta
            movePercent = math.sin(shakeRemaining * 3.14159)
            moveAbsolute = int(shakePixelsHalf * movePercent)
            moveDelta = moveAbsolute - mousePos
            #print("Shake move: {}, {}, {}".format(moveDelta, moveAbsolute, mousePos))
            mouse.move(moveDelta, 0)
            mousePos += moveDelta
        # if not shaking, check if it's time to shake the mouse
        elif (frameTime >= nextMouseShake):
            shakeRemaining = moveMouseShakeTimeSeconds
            nextMouseShake = frameTime + moveMouseShakeTimeSeconds + moveMouseEverySeconds
            mousePos = 0

    time.sleep(0.01)  # make bigger to slow down
    lastFrameTime = frameTime