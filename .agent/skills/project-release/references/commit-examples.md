# Professional Commit Message Examples

## Feature Commits

```
feat(display): add weather screen with Open-Meteo integration

Implement comprehensive weather display for Galactic Unicorn:

- Add WeatherAPI client with automatic retry and 10s timeout
- Display current temperature, conditions, and daily high/low
- Map weather codes to human-readable status text
- Implement button B for quick weather screen access
- Auto-refresh data every 10 minutes with GC cleanup
```

```
feat(wifi): implement captive portal provisioning

Add seamless WiFi setup experience via mobile-friendly portal:

- Create access point with customizable SSID/password
- Serve responsive HTML configuration page
- Handle credential submission and validation
- Auto-redirect devices to setup page (captive portal)
- Persist credentials to config.json for reboot persistence
```

## Bug Fix Commits

```
fix(clock): prevent display freeze during extended operation

Address memory exhaustion causing display to stop updating:

- Add incremental asyncio sleeps (0.05s) in display loops
- Implement periodic garbage collection every 30 seconds
- Add 10-second HTTP timeout to weather API calls
- Wrap NTP sync in try/except to handle network failures
```

```
fix(wifi): resolve AP mode not starting after failed connection

Fix state machine transition when WiFi connection fails:

- Reset WLAN interface before entering AP mode
- Add explicit state transition from FAIL to AP_MODE
- Clear stale connection attempts on mode switch
```

## Documentation Commits

```
docs: add comprehensive README and developer guide

Create user and developer documentation:

- README.md with quick start, usage, and troubleshooting
- CLAUDE.md with architecture, patterns, and API reference
- Add hardware button mapping table
- Include configuration customization examples
```

## Refactor Commits

```
refactor(wifi): extract state machine to dedicated class

Improve code organization and testability:

- Move WiFi logic from gu_main.py to wifi_manager.py
- Implement event emitter pattern for state notifications
- Add dependency injection for DNS/Web server instances
- Create WiFiState enum for type-safe state handling
```

## Chore Commits

```
chore: update dependencies and clean unused imports

Maintenance and cleanup:

- Remove unused json import from config.py
- Update .gitignore with MicroPython-specific patterns
- Add restore.py for factory reset functionality
```

## Multi-Component Commits

```
feat(core): implement clock and weather display system

Complete implementation of dual-screen display:

Display:
- Add show_clock() with blinking separator
- Add show_weather() with temp and conditions
- Implement screen auto-rotation (10s interval)

Weather:
- Integrate Open-Meteo API (no key required)
- Parse current conditions and daily forecast
- Handle API errors gracefully with fallback display

Controls:
- Button A: switch to clock
- Button B: switch to weather
- Button C (hold): reset to AP mode
```
