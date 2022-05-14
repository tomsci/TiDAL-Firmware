from app import App
from buttons import Buttons
from machine import Signal
from tidal import JOY_UP, JOY_DOWN, JOY_LEFT, JOY_RIGHT, JOY_CENTRE

import hardware_setup
# Fix up things the Display constructor in hardware_setup would normally have set
import gui.core.ugui as _ugui_core
_ugui_core.display = hardware_setup.display
_ugui_core.ssd = hardware_setup.ssd

from gui.core.ugui import Screen, ssd

class _DummyScreen:
    tasks = []
    def on_hide(self):
        pass

class UguiWindow:
    def __init__(self, screen_cls):
        # We assume Screen.current_screen should be null here
        # Setting a dummy screen here prevents Screen.change() from starting the uasyncio event loop
        Screen.current_screen = _DummyScreen()
        self.root_screen = screen_cls()
        # And undo all that
        self.root_screen.parent = None
        Screen.current_screen = None

        buttons = Buttons()
        _NEXT = 1
        _PREV = 2
        buttons.on_press(JOY_RIGHT, lambda: Screen.ctrl_move(_NEXT))
        buttons.on_press(JOY_LEFT, lambda: Screen.ctrl_move(_PREV))
        buttons.on_press(JOY_CENTRE, lambda: Screen.sel_ctrl(), autorepeat=False)
        # ugui uses debounced PushButton objects here instead of the raw pins,
        # but so long as it's something that supports __call__ to get the state
        # it's probably fine (use Signal as it expects true to mean clicked)
        up_sig = Signal(JOY_UP, invert=True)
        down_sig = Signal(JOY_DOWN, invert=True)
        buttons.on_press(JOY_UP, lambda: Screen.adjust(up_sig, 1))
        buttons.on_press(JOY_DOWN, lambda: Screen.adjust(down_sig, -1))
        self.buttons = buttons
        self.current_screen = self.root_screen

    def redraw(self):
        Screen.show(True)
        ssd.show()

class UguiApp(App):
    def __init__(self, screen_cls=None):
        super().__init__()
        window = UguiWindow(screen_cls or self.ROOT_SCREEN)
        self.push_window(window, activate=False)

    def on_activate(self):
        Screen.current_screen = self.window.root_screen
        super().on_activate()

    def on_deactivate(self):
        super().on_deactivate()
        self.current_screen = Screen.current_screen
        Screen.current_screen = None

    def on_idle(self):
        Screen.show(False)
        ssd.show()
