# hardware_setup.py Customised for the EMF Camp TiDAL badge

# Released under the MIT License (MIT). See LICENSE.
# Copyright (c) 2021 Peter Hinch, Ihor Nehrutsa

# Supports:
# EMF Camp TiDAL badge 1.14" screen and joystick

from machine import Pin
import gc
import tidal
from st7789_passthrough import *
SSD = ST7789Passthrough

mode = PORTRAIT  # Options PORTRAIT, USD, REFLECT combined with |

gc.collect()  # Precaution before instantiating framebuf

portrait = mode & PORTRAIT
ht, wd = (240, 135) if portrait else (135, 240)
ssd = SSD(None, height=ht, width=wd, dc=None, cs=None, rst=None, disp_mode=mode)

# Create and export a Display instance
from gui.core.ugui import Display

# nxt = tidal.JOY_RIGHT
# sel = tidal.JOY_CENTRE
# prev = tidal.JOY_LEFT
# increase = tidal.JOY_UP
# decrease = tidal.JOY_DOWN
# display = Display(ssd, nxt, sel, prev, increase, decrease)

class DummyInput:
    def precision(self, val):
        pass

    def adj_mode(self, v=None):
        pass

    def is_adjust(self):
        return False

    def is_precision(self):
        return False

class NoInputDisplay(Display):
    def __init__(self, objssd):
        # Note, does NOT call super
        self.ipdev = DummyInput()
        self.height = objssd.height
        self.width = objssd.width
        self._is_grey = False  # Not greyed-out

display = NoInputDisplay(ssd)
