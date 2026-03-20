import time
import pygame
import feedparser


class NewsWidget:
    def __init__(self, config):
        news_cfg = config.get("news", {})

        self.enabled = news_cfg.get("enabled", True)
        self.feed_url = news_cfg.get(
            "feed_url",
            "https://rss.cnn.com/rss/cnn_topstories.rss"
        )
        self.max_items = news_cfg.get("max_items", 3)
        self.update_interval = news_cfg.get("update_interval", 900)

        self.font_size = news_cfg.get("font_size", 24)
        self.font = pygame.font.SysFont(None, self.font_size)

        self.items = []
        self.last_update = 0

    def update(self):
        if not self.enabled:
            return

        now = time.time()
        if now - self.last_update < self.update_interval:
            return

        try:
            feed = feedparser.parse(self.feed_url)
            self.items = [
                entry.title
                for entry in feed.entries[: self.max_items]
            ]
        except Exception:
            self.items = []

        self.last_update = now

    def draw(self, screen):
        if not self.enabled or not self.items:
            return

        x = 20
        y = screen.get_height() - (self.font_size + 10) * (len(self.items) + 1)

        title = self.font.render("News", True, (192, 192, 192))
        screen.blit(title, (x, y))
        y += self.font_size + 8

        for item in self.items:
            text = self.font.render(f"• {item}", True, (192, 192, 192))
            screen.blit(text, (x, y))
            y += self.font_size + 6
