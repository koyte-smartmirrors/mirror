import pygame
import time
import requests


class WeatherWidget:
    def __init__(self, config):
        weather_cfg = config.get("weather", {})
        color_cfg = config.get("colors", {})

        self.enabled = weather_cfg.get("enabled", False)
        self.api_key = weather_cfg.get("api_key")
        self.city = weather_cfg.get("city")
        self.units = weather_cfg.get("units", "imperial")
        self.update_interval = weather_cfg.get("update_interval", 600)

        self.text_color = tuple(color_cfg.get("text", [255, 255, 255]))
        self.font = pygame.font.SysFont(None, weather_cfg.get("font_size", 28))

        self.last_update = 0
        self.temperature = "--"
        self.description = ""

        if self.enabled:
            self.fetch_weather()

    def fetch_weather(self):
        if not self.api_key or not self.city:
            return

        try:
            url = (
                "https://api.openweathermap.org/data/2.5/weather"
                f"?q={self.city}&appid={self.api_key}&units={self.units}"
            )

            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            self.temperature = f"{int(data['main']['temp'])}°"
            self.description = data["weather"][0]["main"]
            self.last_update = time.time()

        except Exception as e:
            print("🌩 Weather fetch failed:", e)

    def update(self):
        if not self.enabled:
            return

        if time.time() - self.last_update > self.update_interval:
            self.fetch_weather()

    def draw(self, screen):
        if not self.enabled:
            return

        margin = 12

        temp_surf = self.font.render(
            self.temperature, True, self.text_color
        )
        desc_surf = self.font.render(
            self.description, True, self.text_color
        )

        screen.blit(temp_surf, (margin, margin))
        screen.blit(
            desc_surf,
            (margin, margin + temp_surf.get_height() + 4)
        )
