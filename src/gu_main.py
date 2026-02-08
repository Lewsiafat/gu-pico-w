"""
Galactic Unicorn Main Application.
Integrates WiFiManager with GU display for visual status feedback.
"""
import uasyncio as asyncio
import ntptime
import machine
import time
from wifi_manager import WiFiManager
from gu_display import GUDisplay
from weather_api import WeatherAPI
from galactic import GalacticUnicorn
from constants import STATE_CONNECTING, STATE_CONNECTED, STATE_AP_MODE
from logger import Logger

# Screen modes
SCREEN_CLOCK = 0
SCREEN_WEATHER = 1

# Weather refresh interval (seconds)
WEATHER_REFRESH = 600  # 10 minutes

# Long-press duration for reset (seconds)
LONG_PRESS_DURATION = 3


class GUApplication:
    """
    Main application coordinating WiFiManager and GU display.
    """

    def __init__(self):
        """Initialize WiFiManager and display."""
        self._display = GUDisplay(brightness=0.5)
        self._wm = WiFiManager()
        self._weather = WeatherAPI()
        self._log = Logger("GUApp")
        self._display_task = None
        self._current_screen = SCREEN_CLOCK
        self._weather_data = None
        self._reset_press_start = None  # Track long-press for reset

        # Register WiFi event handlers
        self._wm.on("state_change", self._on_state_change)
        self._wm.on("ap_mode_started", self._on_ap_started)
        self._wm.on("connected", self._on_connected)

    def _cancel_display_task(self):
        """Cancel any running display task."""
        self._display.stop()
        if self._display_task:
            self._display_task.cancel()
            self._display_task = None

    def _on_state_change(self, old_state, new_state):
        """Handle WiFi state changes."""
        if new_state == STATE_CONNECTING:
            self._cancel_display_task()
            self._display_task = asyncio.create_task(
                self._display.show_connecting()
            )
        elif new_state == STATE_AP_MODE:
            # Show AP mode screen immediately when state changes
            self._cancel_display_task()
            ap_ssid, ap_password, ap_ip = self._wm.get_ap_config()
            self._display_task = asyncio.create_task(
                self._display.show_ap_mode(ap_ssid, ap_password, ap_ip)
            )

    def _on_ap_started(self, ssid):
        """Handle AP mode activation."""
        self._cancel_display_task()
        ap_ssid, ap_password, ap_ip = self._wm.get_ap_config()
        self._display_task = asyncio.create_task(
            self._display.show_ap_mode(ap_ssid, ap_password, ap_ip)
        )

    def _on_connected(self, ip_address):
        """Handle successful WiFi connection."""
        self._cancel_display_task()
        self._display_task = asyncio.create_task(
            self._connected_sequence(ip_address)
        )

    async def _sync_ntp(self):
        """Sync RTC with NTP server."""
        try:
            ntptime.settime()
            self._log.info("NTP time synced")
        except Exception as e:
            self._log.error(f"NTP sync failed: {e}")

    async def _fetch_weather(self):
        """Fetch weather data from API."""
        self._weather_data = await self._weather.fetch()

    async def _connected_sequence(self, ip_address):
        """Show connected status, sync time, then start auto-rotation."""
        # Show connected for 5 seconds
        await self._display.show_connected(ip_address, duration=5.0)

        # Sync NTP time
        await self._sync_ntp()

        # Fetch initial weather
        await self._fetch_weather()

        # Start auto-rotation loop
        await self._auto_rotate_screens()

    async def _auto_rotate_screens(self):
        """Auto-rotate between clock and weather every 10 seconds."""
        ROTATE_INTERVAL = 10  # seconds

        while True:
            # Show clock for 10 seconds
            self._current_screen = SCREEN_CLOCK
            self._display.stop()
            elapsed = 0
            while elapsed < ROTATE_INTERVAL:
                # Update clock display
                await self._show_clock_frame()
                await asyncio.sleep(1)
                elapsed += 1

            # Show weather for 10 seconds
            self._current_screen = SCREEN_WEATHER
            if self._weather_data:
                self._display.stop()
                self._graphics_clear()
                await self._show_weather_frame()
                await asyncio.sleep(ROTATE_INTERVAL)

    async def _show_clock_frame(self):
        """Show one frame of clock (called repeatedly)."""
        import machine
        rtc = machine.RTC()
        year, month, day, _, hour, minute, second, _ = rtc.datetime()
        hour = (hour + 8) % 24  # UTC+8

        time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
        date_str = "{}/{}".format(month, day)
        display_str = "{}{}".format(time_str, date_str)

        g = self._display._graphics
        g.set_pen(self._display._black)
        g.clear()

        text_w = g.measure_text(display_str, 1)
        text_x = (53 - text_w) // 2
        self._display._draw_outlined_text(display_str, text_x, 2,
                                          self._display._cyan, 
                                          self._display._black, 1)
        self._display._gu.update(g)

    async def _show_weather_frame(self):
        """Show weather display."""
        if not self._weather_data:
            return

        g = self._display._graphics
        g.set_pen(self._display._black)
        g.clear()

        temp_str = "{:.0f}C".format(self._weather_data["temp"])
        status = self._weather_data["status"]
        hilo_str = "H{:.0f} L{:.0f}".format(
            self._weather_data["high"], 
            self._weather_data["low"]
        )

        # Row 1: temp + status
        self._display._draw_outlined_text(temp_str, 1, 0,
                                          self._display._yellow,
                                          self._display._black, 1)
        status_w = g.measure_text(status, 1)
        status_x = (53 - status_w) // 2
        self._display._draw_outlined_text(status, status_x, 0,
                                          self._display._white,
                                          self._display._black, 1)

        # Row 2: hi/lo centered
        hilo_w = g.measure_text(hilo_str, 1)
        hilo_x = (53 - hilo_w) // 2
        self._display._draw_outlined_text(hilo_str, hilo_x, 6,
                                          self._display._green,
                                          self._display._black, 1)

        self._display._gu.update(g)

    def _graphics_clear(self):
        """Helper to clear graphics."""
        g = self._display._graphics
        g.set_pen(self._display._black)
        g.clear()

    def _show_current_screen(self):
        """Display the current screen."""
        self._cancel_display_task()

        if self._current_screen == SCREEN_CLOCK:
            self._display_task = asyncio.create_task(
                self._display.show_clock(utc_offset=8)
            )
        elif self._current_screen == SCREEN_WEATHER:
            if self._weather_data:
                self._display_task = asyncio.create_task(
                    self._display.show_weather(
                        self._weather_data["temp"],
                        self._weather_data["status"],
                        self._weather_data["high"],
                        self._weather_data["low"]
                    )
                )

    def _handle_buttons(self):
        """Handle button presses for screen switching and reset."""
        gu = self._display.gu

        # Brightness control
        self._display.handle_brightness_buttons()

        # Long-press C button to reset to AP mode
        if gu.is_pressed(GalacticUnicorn.SWITCH_C):
            if self._reset_press_start is None:
                self._reset_press_start = time.time()
            else:
                held_time = time.time() - self._reset_press_start
                if held_time >= LONG_PRESS_DURATION:
                    self._log.info("Long-press detected, entering AP mode")
                    self._reset_press_start = None
                    self._wm.enter_ap_mode()
                    return
        else:
            self._reset_press_start = None

        # Screen switching (only when connected)
        if self._wm.is_connected():
            if gu.is_pressed(GalacticUnicorn.SWITCH_A):
                if self._current_screen != SCREEN_CLOCK:
                    self._current_screen = SCREEN_CLOCK
                    self._show_current_screen()

            if gu.is_pressed(GalacticUnicorn.SWITCH_B):
                if self._current_screen != SCREEN_WEATHER:
                    self._current_screen = SCREEN_WEATHER
                    self._show_current_screen()

    async def _weather_refresh_loop(self):
        """Periodically refresh weather data."""
        while True:
            await asyncio.sleep(WEATHER_REFRESH)
            if self._wm.is_connected():
                await self._fetch_weather()
                # Update display if on weather screen
                if self._current_screen == SCREEN_WEATHER:
                    self._show_current_screen()

    async def run(self):
        """Main application loop."""
        self._log.info("Galactic Unicorn WiFi Manager starting")

        # Initial display while waiting for WiFi
        self._display_task = asyncio.create_task(
            self._display.show_connecting()
        )

        # Start weather refresh task
        asyncio.create_task(self._weather_refresh_loop())

        # Main loop: handle buttons
        while True:
            self._handle_buttons()
            await asyncio.sleep(0.1)


async def main():
    """Entry point for the application."""
    app = GUApplication()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- System Stopped ---")
