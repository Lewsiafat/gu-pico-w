# Release Notes

## [v1.1.0] - 2026-02-09

### Added
- **project-release skill**: Automates documentation updates, professional commits, version tagging, and pushing to remote
- **skill-creator skill**: Guide for creating new skills with scripts, references, and assets
- **/update workflow**: Step-by-step release workflow accessible via `/update` command

### Fixed
- Weather status text now truncated to 7 characters to prevent display overflow on 53px width
- "Overcast" shortened to "Ovrcast" in weather codes for display compatibility

---

## [v1.0.1] - 2026-02-08

### Fixed
- Stability improvements for long-running operation
- Added incremental sleeps and garbage collection to prevent memory exhaustion
- HTTP timeout (10s) for weather API calls

---

## [v1.0.0] - 2026-02-08

### Added
- Initial release with clock and weather display
- WiFi provisioning via captive portal
- NTP time synchronization (UTC+8)
- Open-Meteo weather integration
- Button controls (A: clock, B: weather, C hold: reset)
- Brightness adjustment via hardware buttons
