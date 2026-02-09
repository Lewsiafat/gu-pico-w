"""
Galactic Unicorn Display Driver for Picore-W.
Provides scrolling text and WiFi status display functionality.
"""
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import uasyncio as asyncio

# Display dimensions
WIDTH = GalacticUnicorn.WIDTH   # 53
HEIGHT = GalacticUnicorn.HEIGHT  # 11

# Scroll settings
SCROLL_SPEED = 0.04  # Seconds per pixel
PADDING = 5          # Pixels padding at start/end


class GUDisplay:
    """
    Display manager for Galactic Unicorn.
    Handles scrolling text and WiFi status display.
    """

    def __init__(self, brightness: float = 0.5):
        """
        Initialize the Galactic Unicorn display.

        Args:
            brightness: Initial brightness level (0.0-1.0).
        """
        self._gu = GalacticUnicorn()
        self._graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
        self._gu.set_brightness(brightness)

        # Pre-create common pen colors
        self._black = self._graphics.create_pen(0, 0, 0)
        self._white = self._graphics.create_pen(255, 255, 255)
        self._yellow = self._graphics.create_pen(255, 255, 0)
        self._green = self._graphics.create_pen(0, 255, 100)
        self._cyan = self._graphics.create_pen(0, 200, 255)

        # State tracking
        self._running = False
        self._current_task = None

    @property
    def gu(self) -> GalacticUnicorn:
        """Access underlying GalacticUnicorn for button checks."""
        return self._gu

    def stop(self):
        """Stop any running display task."""
        self._running = False
        if self._current_task:
            self._current_task.cancel()
            self._current_task = None

    def clear(self):
        """Clear the display."""
        self._graphics.set_pen(self._black)
        self._graphics.clear()
        self._gu.update(self._graphics)

    def _draw_text(self, text: str, x: int, y: int, pen, scale: float = 1):
        """Draw text at position with specified pen color."""
        self._graphics.set_pen(pen)
        self._graphics.text(text, x, y, -1, scale)

    def _draw_outlined_text(self, text: str, x: int, y: int, 
                            fg_pen, bg_pen, scale: float = 1):
        """Draw text with outline for better visibility."""
        # Draw outline (8 directions)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx != 0 or dy != 0:
                    self._graphics.set_pen(bg_pen)
                    self._graphics.text(text, x + dx, y + dy, -1, scale)
        # Draw foreground
        self._graphics.set_pen(fg_pen)
        self._graphics.text(text, x, y, -1, scale)

    async def scroll_text(self, message: str, pen=None, speed: float = None):
        """
        Scroll text across the display.

        Args:
            message: Text to scroll.
            pen: Color pen to use (default: yellow).
            speed: Seconds per scroll step (default: SCROLL_SPEED).
        """
        if pen is None:
            pen = self._yellow
        if speed is None:
            speed = SCROLL_SPEED

        self._running = True
        msg_width = self._graphics.measure_text(message, 1)
        scroll_range = msg_width + WIDTH + PADDING * 2

        shift = -PADDING

        while self._running:
            # Clear
            self._graphics.set_pen(self._black)
            self._graphics.clear()

            # Draw text
            self._draw_outlined_text(message, PADDING - shift, 2, 
                                     pen, self._black, 1)

            self._gu.update(self._graphics)

            # Update scroll position
            shift += 1
            if shift >= scroll_range:
                shift = -PADDING

            await asyncio.sleep(speed)

    async def show_ap_mode(self, ssid: str, password: str, ip: str):
        """
        Display AP mode info with scrolling text.

        Args:
            ssid: Access point SSID.
            password: Access point password.
            ip: AP IP address.
        """
        message = f"  WiFi Setup  |  SSID: {ssid}  |  Pass: {password}  |  http://{ip}  "
        await self.scroll_text(message, self._cyan)

    async def show_connected(self, ip: str, duration: float = 10.0):
        """
        Display connected status for specified duration.

        Args:
            ip: IP address to display.
            duration: Seconds to show the message.
        """
        self._running = True

        # Prepare text
        line1 = "Connected!"
        line2 = ip

        # Center calculations
        w1 = self._graphics.measure_text(line1, 1)
        w2 = self._graphics.measure_text(line2, 1)
        x1 = (WIDTH - w1) // 2
        x2 = (WIDTH - w2) // 2

        # Clear and draw
        self._graphics.set_pen(self._black)
        self._graphics.clear()

        self._draw_outlined_text(line1, x1, 0, self._green, self._black, 1)
        self._draw_outlined_text(line2, x2, 6, self._white, self._black, 1)

        self._gu.update(self._graphics)

        # Wait for duration (with running check for early stop)
        elapsed = 0
        while self._running and elapsed < duration:
            await asyncio.sleep(0.1)
            elapsed += 0.1

    async def show_welcome(self):
        """Display welcome message (main function placeholder)."""
        self._running = True

        message = "Welcome!"
        w = self._graphics.measure_text(message, 1)
        x = (WIDTH - w) // 2
        y = 2

        self._graphics.set_pen(self._black)
        self._graphics.clear()
        self._draw_outlined_text(message, x, y, self._yellow, self._black, 1)
        self._gu.update(self._graphics)

        # Keep display on until stopped
        while self._running:
            await asyncio.sleep(1)

    async def show_connecting(self):
        """Display connecting animation."""
        self._running = True
        dots = 0

        while self._running:
            message = "Connecting" + "." * (dots + 1)
            w = self._graphics.measure_text(message, 1)
            x = (WIDTH - w) // 2

            self._graphics.set_pen(self._black)
            self._graphics.clear()
            self._draw_outlined_text(message, x, 2, self._white, self._black, 1)
            self._gu.update(self._graphics)

            dots = (dots + 1) % 3
            await asyncio.sleep(0.5)

    def adjust_brightness(self, delta: float):
        """Adjust display brightness by delta."""
        self._gu.adjust_brightness(delta)

    def handle_brightness_buttons(self):
        """Check and handle brightness button presses."""
        if self._gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
            self._gu.adjust_brightness(0.02)
        if self._gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
            self._gu.adjust_brightness(-0.02)

    async def show_clock(self, utc_offset: int = 8):
        """
        Display time and date with UTC offset (horizontal layout).

        Args:
            utc_offset: Hours offset from UTC (default: +8 for Taiwan).
        """
        import machine
        import time

        self._running = True
        rtc = machine.RTC()

        while self._running:
            # Get RTC time and apply offset
            year, month, day, _, hour, minute, second, _ = rtc.datetime()

            # Apply UTC offset
            hour = (hour + utc_offset) % 24

            # Format strings (no leading zeros for date)
            time_str = "{:02}:{:02}:{:02}".format(hour, minute, second)
            date_str = "{}/{}".format(month, day)

            # Combine for horizontal layout
            display_str = "{} {}".format(time_str, date_str)

            # Clear display
            self._graphics.set_pen(self._black)
            self._graphics.clear()

            # Draw centered text
            text_w = self._graphics.measure_text(display_str, 1)
            text_x = (WIDTH - text_w) // 2
            self._draw_outlined_text(display_str, text_x, 2, 
                                     self._cyan, self._black, 1)

            self._gu.update(self._graphics)
            await asyncio.sleep(1)

    async def show_weather(self, temp: float, status: str, 
                           high: float, low: float):
        """
        Display weather information.

        Args:
            temp: Current temperature in Celsius.
            status: Weather status text (e.g., "Sunny").
            high: Today's high temperature.
            low: Today's low temperature.
        """
        self._running = True

        # Format strings (truncate status to 7 chars max)
        temp_str = "{:.0f}C".format(temp)
        status = status[:7]  # Prevent display overflow
        hilo_str = "H{:.0f} L{:.0f}".format(high, low)

        # Clear display
        self._graphics.set_pen(self._black)
        self._graphics.clear()

        # Row 1: temp + status centered together (moved up 1 pixel)
        temp_w = self._graphics.measure_text(temp_str, 1)
        status_w = self._graphics.measure_text(status, 1)
        gap = 2
        total_w = temp_w + gap + status_w
        start_x = (WIDTH - total_w) // 2
        
        self._draw_outlined_text(temp_str, start_x, -1, 
                                 self._yellow, self._black, 1)
        self._draw_outlined_text(status, start_x + temp_w + gap, -1, 
                                 self._white, self._black, 1)

        # Row 2: hi/lo centered (moved up 1 pixel)
        hilo_w = self._graphics.measure_text(hilo_str, 1)
        hilo_x = (WIDTH - hilo_w) // 2
        self._draw_outlined_text(hilo_str, hilo_x, 5, 
                                 self._green, self._black, 1)

        self._gu.update(self._graphics)

        # Keep display on until stopped (with timeout protection)
        while self._running:
            await asyncio.sleep(1)

