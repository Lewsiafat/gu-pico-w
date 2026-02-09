# CLAUDE.md - Developer Reference

This file provides guidance for AI assistants and developers working on this codebase.

## Project Overview

**gu-pico** is a MicroPython application for the **Pimoroni Galactic Unicorn** (53x11 RGB LED matrix) running on Raspberry Pi Pico W. It features WiFi provisioning via captive portal and displays clock/weather information.

## Architecture

```
src/
├── main.py              # Auto-boot entry point (launches gu_main with startup delay)
├── gu_main.py           # Full application entry point with display
├── wifi_manager.py      # WiFi state machine (core networking)
├── gu_display.py        # Display driver (scrolling text, status screens)
├── weather_api.py       # Open-Meteo weather API client
├── config.py            # WiFiConfig class with connection parameters
├── config_manager.py    # Persistent credential storage
├── constants.py         # WiFiState enum and legacy constants
├── dns_server.py        # Captive portal DNS server
├── web_server.py        # HTTP server for provisioning
├── provisioning.py      # WiFi credential submission handler
├── logger.py            # Logging utility
├── restore.py           # Factory reset helper
└── templates/           # HTML templates for web UI
```

## Key Components

### WiFiManager (`wifi_manager.py`)
- **State machine** with states: `IDLE`, `CONNECTING`, `CONNECTED`, `FAIL`, `AP_MODE`
- **Event-driven**: Use `wm.on('connected', callback)` for state notifications
- **Auto-provisioning**: Falls back to AP mode after failed connections
- **Dependency injection**: Accepts custom DNSServer/WebServer instances

### GUDisplay (`gu_display.py`)
- Wraps `GalacticUnicorn` and `PicoGraphics`
- Methods: `show_connecting()`, `show_ap_mode()`, `show_connected()`, `show_clock()`, `show_weather()`
- All display methods are `async` for non-blocking operation

### GUApplication (`gu_main.py`)
- Coordinates WiFiManager, GUDisplay, and WeatherAPI
- Auto-rotates between clock and weather screens (10s intervals)
- Button A/B for manual screen switching

### WeatherAPI (`weather_api.py`)
- Uses Open-Meteo API (free, no key required)
- Default location: Taipei (25.0330, 121.5654)
- Returns: `{temp, status, high, low, code}`
- **Stability**: 10-second HTTP timeout, automatic garbage collection
- **Display constraint**: Status text truncated to 7 chars max to fit 53px width

## Development Patterns

### Async/Await
All long-running operations use `uasyncio`:
```python
import uasyncio as asyncio
await asyncio.sleep(1)
asyncio.create_task(my_coroutine())
```

### Event Handling
WiFiManager emits events:
```python
wm.on('connected', lambda ip: print(f"Connected: {ip}"))
wm.on('ap_mode_started', lambda ssid: print(f"AP: {ssid}"))
wm.on('state_change', lambda old, new: ...)
```

### Display Updates
Always use `gu.update(graphics)` after drawing:
```python
graphics.set_pen(BLACK)
graphics.clear()
graphics.set_pen(WHITE)
graphics.text("Hello", x, y, -1, 1)
gu.update(graphics)
```

## Configuration

### WiFiConfig Defaults (`config.py`)
| Parameter | Default | Description |
|-----------|---------|-------------|
| `MAX_RETRIES` | 5 | Connection attempts before failure |
| `CONNECT_TIMEOUT` | 15 | Seconds per connection attempt |
| `AP_SSID` | "Picore-W-Setup" | Provisioning hotspot name |
| `AP_PASSWORD` | "12345678" | Provisioning hotspot password |
| `AP_IP` | "192.168.4.1" | Captive portal IP |

### Credential Storage
Credentials stored in `/config.json` via `ConfigManager`:
```python
ConfigManager.save_wifi_credentials(ssid, password)
ssid, password = ConfigManager.get_wifi_credentials()
```

## Hardware Reference

### Galactic Unicorn
- **Display**: 53×11 RGB LEDs
- **Buttons**: A, B, C, D, Sleep, Volume Up/Down, Brightness Up/Down
- **Button Constants**: `GalacticUnicorn.SWITCH_A`, `SWITCH_B`, etc.

### Button Mapping
| Button | Constant | Function |
|--------|----------|----------|
| A | `SWITCH_A` | Switch to clock screen |
| B | `SWITCH_B` | Switch to weather screen |
| C (hold 3s) | `SWITCH_C` | Reset to AP mode |
| Brightness ± | `SWITCH_BRIGHTNESS_UP/DOWN` | Adjust brightness |

## Common Tasks

### Adding a New Screen
1. Add method to `GUDisplay` class
2. Add screen constant to `gu_main.py`
3. Update `_show_current_screen()` switch
4. Add button handler if needed

### Modifying Weather Location
```python
self._weather = WeatherAPI(latitude=YOUR_LAT, longitude=YOUR_LON)
```

### Changing NTP Timezone
In `gu_main.py`, modify the UTC offset:
```python
hour = (hour + 8) % 24  # Change 8 to your offset
```

## Code Reference

See `CODE_REFERENCE.md` for complete Galactic Unicorn API documentation including:
- PicoGraphics drawing functions
- Color pen creation
- Text rendering and scrolling
- Audio/synthesizer API
- HSV color conversion
