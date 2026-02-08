# Galactic Unicorn WiFi Display

A MicroPython application for the **Pimoroni Galactic Unicorn** that provides WiFi connectivity with captive portal provisioning, real-time clock display, and weather information.

![Pimoroni Galactic Unicorn](https://shop.pimoroni.com/cdn/shop/products/galactic-unicorn_1500x1500.jpg?v=1666086229&width=400)

## Features

- 🌐 **WiFi Provisioning** - Easy setup via captive portal (no config files needed)
- ⏰ **Clock Display** - Time and date with automatic NTP synchronization
- 🌤️ **Weather Display** - Current temperature and conditions from Open-Meteo
- 🔄 **Auto-Rotation** - Automatically cycles between screens
- 💡 **Brightness Control** - Adjustable via hardware buttons

## Hardware Requirements

- [Galactic Unicorn](https://shop.pimoroni.com/products/galactic-unicorn) (53×11 RGB LED matrix with Pico W)
- USB-C cable for power/programming

## Quick Start

### 1. Install Pimoroni MicroPython

Download the latest [Pimoroni Pico firmware](https://github.com/pimoroni/pimoroni-pico/releases) with Galactic Unicorn support and flash it to your device.

### 2. Upload Files

Copy the `src/` folder contents to your Pico W:
```
/config.py
/config_manager.py
/constants.py
/dns_server.py
/gu_display.py
/gu_main.py
/logger.py
/main.py
/provisioning.py
/weather_api.py
/web_server.py
/wifi_manager.py
/templates/
```

### 3. Initial Setup

1. Power on the Galactic Unicorn
2. The display will show "Connecting..."
3. If no WiFi is configured, it enters **AP Mode**:
   - Connect your phone/computer to WiFi network: **Picore-W-Setup**
   - Password: **12345678**
   - A captive portal will open (or navigate to http://192.168.4.1)
   - Enter your WiFi credentials and submit
4. The device will restart and connect to your WiFi

## Usage

### Screen Navigation

| Button | Action |
|--------|--------|
| **A** | Switch to Clock screen |
| **B** | Switch to Weather screen |
| **C** (hold 3s) | Reset to AP mode (reconfigure WiFi) |
| **Brightness +** | Increase display brightness |
| **Brightness -** | Decrease display brightness |

### Display Screens

**Clock Screen**
- Shows current time (HH:MM) with blinking dot separator and date (MM/DD)
- Time is synced via NTP (UTC+8 default)

**Weather Screen**
- Current temperature
- Weather condition (Sunny, Cloudy, Rain, etc.)
- Today's high/low temperatures

## Configuration

### Changing Location (Weather)

Edit `weather_api.py` and modify the default coordinates:
```python
def __init__(self, latitude: float = 25.0330, longitude: float = 121.5654):
```

### Changing Timezone

Edit `gu_main.py` line 127:
```python
hour = (hour + 8) % 24  # Change 8 to your UTC offset
```

### Changing AP Settings

Edit `config.py`:
```python
AP_SSID = "Picore-W-Setup"     # Your custom SSID
AP_PASSWORD = "12345678"        # Your custom password
```

## Troubleshooting

### Display shows "Connecting..." indefinitely
- The device cannot connect to your WiFi
- Wait ~45 seconds for it to enter AP Mode
- Reconfigure WiFi credentials

### Weather shows "N/A"
- Check WiFi connection
- Weather API requires internet access
- Verify coordinates are valid

### Screen is too dim/bright
- Use the Brightness +/- buttons on the device

### Factory Reset
To clear saved WiFi credentials:
1. Connect via USB and Thonny/rshell
2. Run: `import restore; restore.reset()`
3. Or delete `/config.json` from the device

## Project Structure

```
gu-pico/
├── src/                    # Source code
│   ├── gu_main.py         # Main application entry point
│   ├── wifi_manager.py    # WiFi state machine
│   ├── gu_display.py      # Display driver
│   ├── weather_api.py     # Weather API client
│   └── ...
├── examples/              # Example scripts
├── ref_source/            # Reference materials
├── CODE_REFERENCE.md      # Galactic Unicorn API reference
├── CLAUDE.md              # Developer reference
└── README.md              # This file
```

## License

MIT License - See LICENSE file for details.

## Acknowledgments

- [Pimoroni](https://pimoroni.com/) for Galactic Unicorn hardware and MicroPython libraries
- [Open-Meteo](https://open-meteo.com/) for free weather API
