"""
Weather API client for Open-Meteo.
Fetches current temperature, weather status, and daily hi/lo.
"""
import urequests
import uasyncio as asyncio
from logger import Logger

# Weather code to description mapping (WMO codes)
WEATHER_CODES = {
    0: "Clear",
    1: "Sunny",
    2: "Cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Fog",
    51: "Drizzle",
    53: "Drizzle",
    55: "Drizzle",
    61: "Rain",
    63: "Rain",
    65: "HvyRain",
    71: "Snow",
    73: "Snow",
    75: "HvySnow",
    77: "Snow",
    80: "Showers",
    81: "Showers",
    82: "HvyRain",
    85: "SnowShr",
    86: "SnowShr",
    95: "Storm",
    96: "Storm",
    99: "Storm",
}


class WeatherAPI:
    """
    Weather data fetcher using Open-Meteo API.
    Free API, no key required.
    """

    BASE_URL = "https://api.open-meteo.com/v1/forecast"

    def __init__(self, latitude: float = 25.0330, longitude: float = 121.5654):
        """
        Initialize weather API client.

        Args:
            latitude: Location latitude (default: Taipei).
            longitude: Location longitude (default: Taipei).
        """
        self._lat = latitude
        self._lon = longitude
        self._log = Logger("WeatherAPI")
        self._cache = None
        self._last_fetch = 0

    def _build_url(self) -> str:
        """Build API request URL."""
        params = (
            f"latitude={self._lat}"
            f"&longitude={self._lon}"
            "&current=temperature_2m,weather_code"
            "&daily=temperature_2m_max,temperature_2m_min"
            "&timezone=auto"
        )
        return f"{self.BASE_URL}?{params}"

    def _parse_response(self, data: dict) -> dict:
        """Parse API response into weather dict."""
        current = data.get("current", {})
        daily = data.get("daily", {})

        temp = current.get("temperature_2m", 0)
        code = current.get("weather_code", 0)
        status = WEATHER_CODES.get(code, "Unknown")

        # Get today's hi/lo (first element)
        highs = daily.get("temperature_2m_max", [0])
        lows = daily.get("temperature_2m_min", [0])
        high = highs[0] if highs else 0
        low = lows[0] if lows else 0

        return {
            "temp": temp,
            "status": status,
            "high": high,
            "low": low,
            "code": code,
        }

    async def fetch(self) -> dict:
        """
        Fetch current weather data.

        Returns:
            dict: {temp, status, high, low, code}
        """
        import gc
        response = None
        try:
            url = self._build_url()
            self._log.debug(f"Fetching: {url}")

            # Synchronous request with timeout to prevent hanging
            response = urequests.get(url, timeout=10)
            data = response.json()
            response.close()
            response = None

            self._cache = self._parse_response(data)
            self._log.info(f"Weather: {self._cache['temp']}°C, {self._cache['status']}")
            
            # Free memory
            del data
            gc.collect()
            
            return self._cache

        except Exception as e:
            self._log.error(f"Fetch failed: {e}")
            # Ensure response is closed on error
            if response:
                try:
                    response.close()
                except:
                    pass
            gc.collect()
            # Return cached data or defaults
            if self._cache:
                return self._cache
            return {
                "temp": 0,
                "status": "N/A",
                "high": 0,
                "low": 0,
                "code": -1,
            }

    def get_cached(self) -> dict:
        """Get cached weather data without fetching."""
        return self._cache or {
            "temp": 0,
            "status": "N/A",
            "high": 0,
            "low": 0,
            "code": -1,
        }
