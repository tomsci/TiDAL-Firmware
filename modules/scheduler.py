import tidal_helpers
import time
import uasyncio

_scheduler = None

def get_scheduler():
    """Return the global scheduler object."""
    global _scheduler
    if not _scheduler:
        _scheduler = Scheduler()
    return _scheduler

class TimerTask:
    def __init__(self, fn, target_time, period_interval=None):
        self.scheduler = None
        self.target_time = target_time
        self.fn = fn
        self.period_interval = period_interval

    def cancel(self):
        if self.scheduler:
            self.scheduler.cancel_task(self)

    async def async_call(self):
        self.fn()

class Scheduler:
    _current_app = None
    _root_app = None
    sleep_enabled = True

    def __init__(self):
        self._timers = []

    def switch_app(self, app):
        """Asynchronously switch to the specified app."""
        uasyncio.create_task(self._switch_app(app))

    async def _switch_app(self, app):
        if app is None:
            app = self._root_app
        if app == self._current_app:
            # Nothing to do
            return
        print(f"Switching app to {app.get_app_id()}")

        if app.buttons:
            app.buttons.activate()
        elif self._current_app and self._current_app.buttons:
            # Then we'd better at least deactivate the current buttons
            self._current_app.buttons.deactivate()

        if self._current_app:
            self._current_app.on_deactivate()

        self._current_app = app
        if not app.started:
            app.started = True
            app.on_start()
        app.on_activate()

    def _get_next_sleep_time(self):
        if next_timer_task := self.peek_timer():
            next_time = next_timer_task.target_time
            return max(1, next_time - time.ticks_ms())
        else:
            return 0

    def main(self, initial_app):
        """Main entry point to the scheduler. Does not return."""
        self._root_app = initial_app
        self.switch_app(initial_app)
        tidal_helpers.esp_sleep_enable_gpio_wakeup()
        first_time = True
        while True:
            while self.check_for_interrupts() or first_time:
                first_time = False
                uasyncio.run_until_complete()

            t = self._get_next_sleep_time()
            if self.sleep_enabled:
                # print(f"Sleepy time {t}")
                # Make sure any debug prints show up on the USB UART
                tidal_helpers.uart_tx_flush(0)
                wakeup_cause = tidal_helpers.lightsleep(t)
                # print(f"Returned from lightsleep reason={wakeup_cause}")
            else:
                if t == 0:
                    # Add a bit of a sleep (which uses less power than straight-up looping)
                    time.sleep(0.1)
                else:
                    time.sleep(t / 1000)

    def set_sleep_enabled(self, flag):
        print(f"Light sleep enabled: {flag}")
        self.sleep_enabled = flag

    def is_sleep_enabled(self):
        return self.sleep_enabled

    def check_for_interrupts(self):
        """Check for any pending interrupts and schedule uasyncio tasks for them."""
        found = False
        if self._current_app and self._current_app.check_for_interrupts():
            found = True
        t = time.ticks_ms()
        while True:
            task = self.peek_timer()
            if task and task.target_time <= t:
                # print(f"Timer ready at {task.target_time}")
                found = True
                del self._timers[0]
                task.scheduler = None
                uasyncio.create_task(task.async_call())
                if task.period_interval:
                    # Re-add the task with an updated target time
                    task.target_time = task.target_time + task.period_interval
                    self.add_timer_task(task)
                continue # Check next timer in the queue
            else:
                break

        return found

    def add_timer_task(self, task):
        self._timers.append(task)
        task.scheduler = self
        self._timers.sort(key=lambda t: t.target_time)

    def cancel_task(self, task):
        self._timers.remove(task)

    def peek_timer(self):
        if len(self._timers) > 0:
            return self._timers[0]
        else:
            return None

    def after(self, ms, callback):
        task = TimerTask(callback, time.ticks_ms() + ms)
        self.add_timer_task(task)
        return task

    def periodic(self, ms, callback):
        task = TimerTask(callback, time.ticks_ms() + ms, ms)
        self.add_timer_task(task)
        return task