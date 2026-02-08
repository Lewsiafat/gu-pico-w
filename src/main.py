# main.py - Auto-boot entry point for Picore-W
# MicroPython runs this file automatically on power-on

import time

# Startup delay - wait for hardware to initialize
time.sleep(1)

# Import and run the main application
import uasyncio as asyncio
from gu_main import main

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n--- System Stopped ---")