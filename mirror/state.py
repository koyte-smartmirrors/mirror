import pygame
from datetime import datetime


class MirrorState:
    def __init__(self, config):
        self.config = config

        # ----------------------------------------------------
        # Configuration
        # ----------------------------------------------------
        clock_cfg = config.get("clock", {})
        color_cfg = config.get("colors", {})

        # Time format
        self.show_seconds = clock_cfg.get("show_seconds", False)
        self.time_format = "%I:%M:%S %p" if self.show_seconds else "%I:%M %p"

        # Font
        font_size = clock_cfg.get("font_size", 64)
        self.font = pygame.font.SysFont(None, font_size)

        # Colors
        self.text_color = color_cfg.get("text", (255, 255, 255))
        self.bg_color = color_cfg.get("background", (0, 0, 0))

        # State
        self.time_text = ""
        self.last_rendered_time = None

    # ----------------------------------------------------
    # Optional event handling (touch / keys / GPIO later)
    # ----------------------------------------------------
    def handle_event(self, event):
        # Placeholder for future interaction
        pass

    # ----------------------------------------------------
    # Update logic
    # ----------------------------------------------------
    def update(self):
        now = datetime.now()
        formatted = now.strftime(self.time_format).lstrip("0")

        # Only update if the displayed time changed
        if formatted != self.last_rendered_time:
            self.time_text = formatted
            self.last_rendered_time = formatted

    # ----------------------------------------------------
    # Rendering
    # ----------------------------------------------------
    def draw(self, screen):
        # Clear background
        screen.fill(self.bg_color)

        # Render time text
        text_surface = self.font.render(
            self.time_text,
            True,
            self.text_color
        )

        # Position: top-right with margin
        margin = 12
        rect = text_surface.get_rect(
            topright=(screen.get_width() - margin, margin)
        )

        screen.blit(text_surface, rect)
