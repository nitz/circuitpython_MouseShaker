# circuitpython_MouseShaker
A teeny circuitpython script that makes your mouse shake to keep your PC awake.

## Hardware

This was created and used on an [Adafruit Trinket M0](https://www.adafruit.com/product/3500), a low cost SAMD21 development board that I absolutely adore.

## Usage

Plug the device in with this main loaded up, and every few seconds your mouse will shake! You can edit the settings at the top of the `main.py` to adjust how often or how far it shakes easily. As well, tapping on pin `3` with your finger will enable/disable the shake. (It uses the capacitive touch of the pin, so it can be a little tricky to get the feel for. The RGB LED will go through a nice color wheel while it's active, and pulse red while it's not. The other led lights up when you're activiating the touch on pin `3`.

## License

MIT License, go wild.
