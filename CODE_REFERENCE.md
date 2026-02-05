# Galactic Unicorn Code Reference

This document provides a comprehensive reference for developing MicroPython applications for the Galactic Unicorn (53x11 RGB LED matrix display).

## Table of Contents

- [Hardware Overview](#hardware-overview)
- [Quick Start](#quick-start)
- [API Reference](#api-reference)
  - [Imports and Initialization](#imports-and-initialization)
  - [System State](#system-state)
  - [Drawing](#drawing)
  - [Audio](#audio)
  - [Constants](#constants)
- [Common Patterns](#common-patterns)
- [Code Examples](#code-examples)

---

## Hardware Overview

**Galactic Unicorn** features:
- **Display**: 53x11 bright RGB LEDs (583 total pixels)
- **Refresh Rate**: ~300fps with 14-bit precision
- **Audio**: 1W amplifier + speaker
- **Buttons**: 9 buttons (A, B, C, D, Sleep, Volume Up/Down, Brightness Up/Down)
- **Sensors**: Onboard light sensor (0-4095 range)
- **Connectivity**: 2x Qw/ST (Qwiic/STEMMA QT) connectors for I2C devices
- **GPIO**: I2C on GP4 (SDA) and GP5 (SCL)

---

## Quick Start

### Minimal Example

```python
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time

# Initialize
graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()

# Create colors
BLACK = graphics.create_pen(0, 0, 0)
YELLOW = graphics.create_pen(255, 255, 0)

# Draw
graphics.set_pen(BLACK)
graphics.clear()
graphics.set_pen(YELLOW)
graphics.text("Hello!", 5, 2, -1, 0.55)

# Display
gu.update(graphics)
time.sleep(1)
```

---

## API Reference

### Imports and Initialization

```python
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

# Create Galactic Unicorn object
gu = GalacticUnicorn()

# Create graphics surface for drawing
graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
```

### System State

#### Brightness Control

```python
# Set brightness (0.0 to 1.0)
gu.set_brightness(0.5)

# Get current brightness
brightness = gu.get_brightness()  # Returns float 0.0-1.0

# Adjust brightness by delta
gu.adjust_brightness(0.1)   # Increase by 0.1
gu.adjust_brightness(-0.2)  # Decrease by 0.2
```

#### Volume Control

```python
# Set volume (0.0 to 1.0)
gu.set_volume(0.5)

# Get current volume
volume = gu.get_volume()  # Returns float 0.0-1.0

# Adjust volume by delta
gu.adjust_volume(0.1)   # Increase by 0.1
gu.adjust_volume(-0.2)  # Decrease by 0.2
```

#### Light Sensor

```python
# Read light sensor value (0-4095)
light_level = gu.light()
```

#### Button Input

```python
# Check if button is pressed (returns True/False)
if gu.is_pressed(GalacticUnicorn.SWITCH_A):
    print("Button A pressed!")
```

**Button Constants:**

| Constant | Pin | Description |
|----------|-----|-------------|
| `SWITCH_A` | 0 | User button A |
| `SWITCH_B` | 1 | User button B |
| `SWITCH_C` | 3 | User button C |
| `SWITCH_D` | 6 | User button D |
| `SWITCH_SLEEP` | 27 | Sleep button |
| `SWITCH_VOLUME_UP` | 7 | Volume up button |
| `SWITCH_VOLUME_DOWN` | 8 | Volume down button |
| `SWITCH_BRIGHTNESS_UP` | 21 | Brightness up button |
| `SWITCH_BRIGHTNESS_DOWN` | 26 | Brightness down button |

### Drawing

#### Update Display

```python
# Copy PicoGraphics buffer to display with gamma correction
gu.update(graphics)
```

> ⚠️ **Note**: Unlike other Pimoroni boards, `update()` is a GalacticUnicorn method that takes a PicoGraphics object as an argument.

#### Clear Display

```python
# Clear the framebuffer (turns off all LEDs)
gu.clear()
```

#### PicoGraphics Drawing Functions

```python
# Create color pens
WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0, 0, 0)
RED = graphics.create_pen(255, 0, 0)

# Set active pen
graphics.set_pen(WHITE)

# Clear screen with current pen
graphics.clear()

# Draw pixel
graphics.pixel(x, y)

# Draw text
graphics.text(text, x, y, wordwrap, scale)
# wordwrap: -1 for no wrap, or pixel width to wrap at
# scale: text size multiplier (e.g., 1, 0.55)

# Measure text width
width = graphics.measure_text(text, scale)

# Set font
graphics.set_font("bitmap8")  # Default 8x8 bitmap font
```

### Audio

#### Play Audio Sample

```python
# Play 16-bit PCM audio sample
audio_data = bytearray([...])  # 16-bit PCM data
gu.play_sample(audio_data)
```

#### Synthesizer

```python
# Get synth channel (0-7)
channel = gu.synth_channel(0)

# Configure channel
channel.configure(
    waveforms=128,      # Waveform type
    frequency=440,      # Hz
    volume=1.0,         # 0.0-1.0
    attack=100,         # Attack duration (ms)
    decay=100,          # Decay duration (ms)
    sustain=0.8,        # Sustain level (0.0-1.0)
    release=200,        # Release duration (ms)
    pulse_width=0.5     # Pulse width for square wave
)

# Play synth
gu.play_synth()

# Trigger note
channel.trigger_attack()
channel.trigger_release()

# Play tone (simplified)
channel.play_tone(frequency=440, volume=1.0, attack=100, release=200)

# Stop all audio
gu.stop_playing()
```

**Channel Methods:**

```python
channel.waveforms(waveforms)      # Set/get waveform
channel.frequency(frequency)      # Set/get frequency (Hz)
channel.volume(volume)            # Set/get volume (0.0-1.0)
channel.attack_duration(ms)       # Set/get attack duration
channel.decay_duration(ms)        # Set/get decay duration
channel.sustain_level(level)      # Set/get sustain level
channel.release_duration(ms)      # Set/get release duration
channel.pulse_width(width)        # Set/get pulse width
channel.restore()                 # Restore default settings
```

### Constants

```python
# Display dimensions
width = GalacticUnicorn.WIDTH   # 53
height = GalacticUnicorn.HEIGHT  # 11

# Calculate total pixels
num_pixels = GalacticUnicorn.WIDTH * GalacticUnicorn.HEIGHT  # 583
```

---

## Common Patterns

### 1. Outlined Text

Draw text with a black outline for better visibility:

```python
def outline_text(text, x, y):
    # Draw black outline (8 surrounding pixels)
    graphics.set_pen(BLACK)
    graphics.text(text, x - 1, y - 1, -1, 1)
    graphics.text(text, x, y - 1, -1, 1)
    graphics.text(text, x + 1, y - 1, -1, 1)
    graphics.text(text, x - 1, y, -1, 1)
    graphics.text(text, x + 1, y, -1, 1)
    graphics.text(text, x - 1, y + 1, -1, 1)
    graphics.text(text, x, y + 1, -1, 1)
    graphics.text(text, x + 1, y + 1, -1, 1)
    
    # Draw white text on top
    graphics.set_pen(WHITE)
    graphics.text(text, x, y, -1, 1)
```

### 2. Centered Text

Calculate position to center text horizontally:

```python
message = "Hello World"
graphics.set_font("bitmap8")

# Measure text width
text_width = graphics.measure_text(message, 1)

# Calculate centered x position
x = int(GalacticUnicorn.WIDTH / 2 - text_width / 2)
y = 2  # Vertical position

graphics.text(message, x, y, -1, 1)
```

### 3. Scrolling Text

Implement horizontal text scrolling:

```python
MESSAGE = "Scrolling text example"
PADDING = 5
STEP_TIME = 0.075  # Seconds per step

shift = 0
msg_width = graphics.measure_text(MESSAGE, 1)

while True:
    # Clear background
    graphics.set_pen(BLACK)
    graphics.clear()
    
    # Draw scrolling text
    graphics.set_pen(WHITE)
    graphics.text(MESSAGE, PADDING - shift, 2, -1, 1)
    
    # Update shift
    shift += 1
    if shift >= (msg_width + PADDING * 2) - GalacticUnicorn.WIDTH:
        shift = 0
    
    gu.update(graphics)
    time.sleep(STEP_TIME)
```

### 4. HSV to RGB Conversion

Convert HSV color space to RGB (useful for gradients and effects):

```python
import math

@micropython.native
def from_hsv(h, s, v):
    """Convert HSV to RGB.
    
    Args:
        h: Hue (0.0-1.0)
        s: Saturation (0.0-1.0)
        v: Value/Brightness (0.0-1.0)
    
    Returns:
        Tuple of (r, g, b) as integers (0-255)
    """
    i = math.floor(h * 6.0)
    f = h * 6.0 - i
    v *= 255.0
    p = v * (1.0 - s)
    q = v * (1.0 - f * s)
    t = v * (1.0 - (1.0 - f) * s)
    
    i = int(i) % 6
    if i == 0:
        return int(v), int(t), int(p)
    if i == 1:
        return int(q), int(v), int(p)
    if i == 2:
        return int(p), int(v), int(t)
    if i == 3:
        return int(p), int(q), int(v)
    if i == 4:
        return int(t), int(p), int(v)
    if i == 5:
        return int(v), int(p), int(q)
```

### 5. Gradient Background

Create horizontal gradient background:

```python
def gradient_background(start_hue, start_sat, start_val, 
                       end_hue, end_sat, end_val):
    half_width = GalacticUnicorn.WIDTH // 2
    
    for x in range(0, half_width):
        # Interpolate HSV values
        hue = ((end_hue - start_hue) * (x / half_width)) + start_hue
        sat = ((end_sat - start_sat) * (x / half_width)) + start_sat
        val = ((end_val - start_val) * (x / half_width)) + start_val
        
        # Convert to RGB and create pen
        colour = from_hsv(hue, sat, val)
        graphics.set_pen(graphics.create_pen(
            int(colour[0]), int(colour[1]), int(colour[2])
        ))
        
        # Draw mirrored columns
        for y in range(0, GalacticUnicorn.HEIGHT):
            graphics.pixel(x, y)
            graphics.pixel(GalacticUnicorn.WIDTH - x - 1, y)
    
    # Draw center column
    colour = from_hsv(end_hue, end_sat, end_val)
    graphics.set_pen(graphics.create_pen(
        int(colour[0]), int(colour[1]), int(colour[2])
    ))
    for y in range(0, GalacticUnicorn.HEIGHT):
        graphics.pixel(half_width, y)
```

### 6. Button Handling with Brightness Control

Standard pattern for brightness adjustment:

```python
while True:
    # Brightness control
    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
        gu.adjust_brightness(+0.01)
    
    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
        gu.adjust_brightness(-0.01)
    
    # Your application logic here
    
    gu.update(graphics)
    time.sleep(0.01)
```

### 7. Button IRQ (Interrupt) Handling

Use interrupts for precise button detection:

```python
import machine

button_a = machine.Pin(GalacticUnicorn.SWITCH_A, 
                       machine.Pin.IN, 
                       machine.Pin.PULL_UP)

def button_callback(pin):
    print("Button A pressed!")
    # Handle button press

# Attach interrupt (triggers on falling edge when pressed)
button_a.irq(trigger=machine.Pin.IRQ_FALLING, 
             handler=button_callback)
```

### 8. WiFi Connection

Connect to WiFi for network features:

```python
import network
import time

def connect_wifi(ssid, password):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(ssid, password)
    
    # Wait for connection (max 20 seconds)
    max_wait = 100
    while max_wait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_wait -= 1
        print('Waiting for connection...')
        time.sleep(0.2)
    
    if wlan.status() == 3:
        print(f"Connected! IP: {wlan.ifconfig()[0]}")
        return True
    else:
        print("Connection failed")
        return False

# Usage
connect_wifi("YourSSID", "YourPassword")
```

### 9. Time Synchronization with NTP

Get accurate time from internet:

```python
import ntptime
import machine

rtc = machine.RTC()

def sync_time():
    try:
        ntptime.settime()
        print("Time synchronized")
        return True
    except OSError:
        print("NTP sync failed")
        return False

# Get current time
year, month, day, weekday, hour, minute, second, _ = rtc.datetime()
```

### 10. I2C Breakout Connection

Connect I2C devices via Qw/ST connectors:

```python
from pimoroni_i2c import PimoroniI2C
from pimoroni import BREAKOUT_GARDEN_I2C_PINS

# Using predefined pins
i2c = PimoroniI2C(**BREAKOUT_GARDEN_I2C_PINS)

# Or specify pins directly (GP4=SDA, GP5=SCL)
i2c = PimoroniI2C(sda=4, scl=5)
```

---

## Code Examples

### Example 1: Simple Scrolling Message

```python
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time

graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()

# Start position (off screen)
scroll = float(-GalacticUnicorn.WIDTH)
MESSAGE = "Pirate. Monkey. Robot. Ninja."

BLACK = graphics.create_pen(0, 0, 0)
YELLOW = graphics.create_pen(255, 255, 0)

while True:
    # Calculate scroll position
    width = graphics.measure_text(MESSAGE, 1)
    scroll += 0.25
    if scroll > width:
        scroll = float(-GalacticUnicorn.WIDTH)
    
    # Clear and draw
    graphics.set_pen(BLACK)
    graphics.clear()
    graphics.set_pen(YELLOW)
    graphics.text(MESSAGE, round(0 - scroll), 2, -1, 0.55)
    
    gu.update(graphics)
    time.sleep(0.02)
```

### Example 2: Digital Clock

```python
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time
import machine

graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()
rtc = machine.RTC()

WHITE = graphics.create_pen(255, 255, 255)
BLACK = graphics.create_pen(0, 0, 0)

gu.set_brightness(0.5)

while True:
    # Get current time
    year, month, day, wd, hour, minute, second, _ = rtc.datetime()
    
    # Format time string
    clock = "{:02}:{:02}:{:02}".format(hour, minute, second)
    
    # Clear background
    graphics.set_pen(BLACK)
    graphics.clear()
    
    # Draw centered time
    graphics.set_font("bitmap8")
    text_width = graphics.measure_text(clock, 1)
    x = int(GalacticUnicorn.WIDTH / 2 - text_width / 2)
    
    graphics.set_pen(WHITE)
    graphics.text(clock, x, 2, -1, 1)
    
    gu.update(graphics)
    time.sleep(0.1)
```

### Example 3: Rainbow Effect

```python
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time
import math

graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()

hue_offset = 0.0

@micropython.native
def from_hsv(h, s, v):
    # [Same as pattern #4 above]
    pass

while True:
    for x in range(GalacticUnicorn.WIDTH):
        for y in range(GalacticUnicorn.HEIGHT):
            hue = (x + hue_offset) / GalacticUnicorn.WIDTH
            r, g, b = from_hsv(hue, 1.0, 0.8)
            graphics.set_pen(graphics.create_pen(r, g, b))
            graphics.pixel(x, y)
    
    hue_offset += 0.01
    if hue_offset >= GalacticUnicorn.WIDTH:
        hue_offset = 0.0
    
    gu.update(graphics)
    time.sleep(0.05)
```

### Example 4: Button-Controlled Display

```python
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN
import time

graphics = PicoGraphics(display=DISPLAY_GALACTIC_UNICORN)
gu = GalacticUnicorn()

colors = [
    graphics.create_pen(255, 0, 0),    # Red
    graphics.create_pen(0, 255, 0),    # Green
    graphics.create_pen(0, 0, 255),    # Blue
    graphics.create_pen(255, 255, 0),  # Yellow
]

current_color = 0

while True:
    # Button A: Next color
    if gu.is_pressed(GalacticUnicorn.SWITCH_A):
        current_color = (current_color + 1) % len(colors)
        time.sleep(0.2)  # Debounce
    
    # Button B: Previous color
    if gu.is_pressed(GalacticUnicorn.SWITCH_B):
        current_color = (current_color - 1) % len(colors)
        time.sleep(0.2)  # Debounce
    
    # Fill screen with current color
    graphics.set_pen(colors[current_color])
    graphics.clear()
    
    # Brightness control
    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_UP):
        gu.adjust_brightness(+0.01)
    if gu.is_pressed(GalacticUnicorn.SWITCH_BRIGHTNESS_DOWN):
        gu.adjust_brightness(-0.01)
    
    gu.update(graphics)
    time.sleep(0.01)
```

---

## Performance Tips

1. **Use `@micropython.native` decorator** for computationally intensive functions (like HSV conversion)
2. **Minimize pen creation** - Create pens once and reuse them
3. **Keep sleep times small** - Use `time.sleep(0.001)` minimum to prevent USB serial failures
4. **Batch drawing operations** - Update display after all drawing is complete
5. **Use integer math** where possible for better performance on RP2040/RP2350

## Display Characteristics

- **Gamma Correction**: Automatically applied by the library for linear visual output
- **14-bit Precision**: Smooth color gradients, especially at low brightness
- **300fps Refresh**: No flickering or smearing, even when filmed
- **Interleaved Framebuffer**: Handled automatically by the library

## Resources

- [Galactic Unicorn Product Page](https://shop.pimoroni.com/products/galactic-unicorn)
- [MicroPython Firmware Releases](https://github.com/pimoroni/pimoroni-pico/releases)
- [PicoGraphics Documentation](https://github.com/pimoroni/pimoroni-pico/tree/main/micropython/modules/picographics)
- [Pimoroni Pico GitHub](https://github.com/pimoroni/pimoroni-pico)

---

*This reference is based on the Galactic Unicorn MicroPython library and examples from the Pimoroni Pico repository.*
