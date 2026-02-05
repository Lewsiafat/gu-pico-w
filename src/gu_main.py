"""
Galactic Unicorn Main Application.
Integrates WiFiManager with GU display for visual status feedback.
"""
import uasyncio as asyncio
from wifi_manager import WiFiManager
from gu_display import GUDisplay
from constants import STATE_CONNECTING, STATE_CONNECTED, STATE_AP_MODE


class GUApplication:
    """
    Main application coordinating WiFiManager and GU display.
    """

    def __init__(self):
        """Initialize WiFiManager and display."""
        self._display = GUDisplay(brightness=0.5)
        self._wm = WiFiManager()
        self._display_task = None

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

    async def _connected_sequence(self, ip_address):
        """Show connected status for 10s, then welcome."""
        await self._display.show_connected(ip_address, duration=10.0)
        await self._display.show_welcome()

    async def run(self):
        """Main application loop."""
        print("--- Galactic Unicorn WiFi Manager ---")

        # Initial display while waiting for WiFi
        self._display_task = asyncio.create_task(
            self._display.show_connecting()
        )

        # Main loop: handle buttons
        while True:
            self._display.handle_brightness_buttons()
            await asyncio.sleep(0.05)


async def main():
    """Entry point for the application."""
    app = GUApplication()
    await app.run()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- System Stopped ---")
