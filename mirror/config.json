import time
import pygame
import feedparser


class NewsWidget:
    def __init__(self, config):
        news_cfg = config.get("news", {})
        colors_cfg = config.get("colors", {})

        self.enabled = news_cfg.get("enabled", True)

        # Colors come from config.json so it matches your mirror theme
        self.text_color = tuple(colors_cfg.get("text", [255, 255, 255]))

        # Font
        self.font_size = int(news_cfg.get("font_size", 22))
        self.font = pygame.font.SysFont(None, self.font_size)

        # Refresh headlines every X seconds (network fetch)
        self.update_interval = int(news_cfg.get("update_interval", 900))
        self.last_update = 0

        # Rotate what you display every X seconds (no network)
        self.rotate_seconds = float(news_cfg.get("rotate_seconds", 8))
        self._last_rotate_ms = 0
        self._index = 0

        # How many items to fetch and how many to display at once
        self.max_items = int(news_cfg.get("max_items", 40))          # total stored
        self.display_items = int(news_cfg.get("display_items", 1))   # shown lines

        # Optional: show source label
        self.show_source = bool(news_cfg.get("show_source", True))

        # Backward compatible: single feed_url OR list of feeds
        # feeds format: [{"name": "KTVB Local", "url": "..."}, ...]
        feeds = news_cfg.get("feeds")
        if isinstance(feeds, list) and feeds:
            self.feeds = feeds
        else:
            single = news_cfg.get("feed_url", "")
            self.feeds = [{"name": "News", "url": single}] if single else []

        # Internal storage: list of dicts {title, link, source}
        self.items = []

        # Position (default bottom-left)
        self.margin = int(news_cfg.get("margin", 20))
        self.position = news_cfg.get("position", "bottom-left")

    def update(self):
        """Called every frame; throttles network refresh and rotates headline index."""
        if not self.enabled or not self.feeds:
            return

        now = time.time()
        if now - self.last_update >= self.update_interval:
            self._refresh_items()
            self.last_update = now

        # Rotate display index based on pygame ticks
        ticks = pygame.time.get_ticks()
        if self.items and (ticks - self._last_rotate_ms) >= int(self.rotate_seconds * 1000):
            self._index = (self._index + self.display_items) % max(len(self.items), 1)
            self._last_rotate_ms = ticks

    def _refresh_items(self):
        """Fetch and merge feeds; de-dupe by (title, link) and keep newest as returned."""
        merged = []
        seen = set()

        for feed in self.feeds:
            name = str(feed.get("name", "Feed")).strip() or "Feed"
            url = str(feed.get("url", "")).strip()
            if not url:
                continue

            parsed = feedparser.parse(url)
            for entry in parsed.entries[: self.max_items]:
                title = str(getattr(entry, "title", "")).strip()
                link = str(getattr(entry, "link", "")).strip()
                if not title:
                    continue

                key = (title.lower(), link)
                if key in seen:
                    continue
                seen.add(key)

                merged.append({
                    "title": title,
                    "link": link,
                    "source": name
                })

        # Keep a capped list
        self.items = merged[: self.max_items]
        self._index = 0
        self._last_rotate_ms = pygame.time.get_ticks()

    def draw(self, screen):
        if not self.enabled or not self.items:
            return

        # Decide anchor point
        if self.position == "bottom-left":
            x = self.margin
            y = screen.get_height() - self.margin
            anchor = "bottomleft"
        elif self.position == "bottom-right":
            x = screen.get_width() - self.margin
            y = screen.get_height() - self.margin
            anchor = "bottomright"
        elif self.position == "top-left":
            x = self.margin
            y = self.margin
            anchor = "topleft"
        else:  # top-right
            x = screen.get_width() - self.margin
            y = self.margin
            anchor = "topright"

        # Build the lines to show
        start = self._index
        lines = []
        for i in range(self.display_items):
            idx = (start + i) % len(self.items)
            item = self.items[idx]
            title = item["title"]
            if self.show_source:
                title = f"[{item['source']}] {title}"
            lines.append(title)

        # Render lines (stacked)
        rendered = [self._render_fit(screen, line) for line in lines]

        # Place them with consistent spacing
        line_h = self.font_size + 6
        total_h = line_h * len(rendered)

        if anchor.startswith("bottom"):
            y0 = y - total_h
        else:
            y0 = y

        for i, surf in enumerate(rendered):
            rect = surf.get_rect()
            if anchor.endswith("left"):
                rect.topleft = (x, y0 + i * line_h)
            else:
                rect.topright = (x, y0 + i * line_h)
            screen.blit(surf, rect)

    def _render_fit(self, screen, text):
        """Truncate with ellipsis so it fits within screen width minus margins."""
        max_w = screen.get_width() - (self.margin * 2)
        if self.font.size(text)[0] <= max_w:
            return self.font.render(text, True, self.text_color)

        ell = "…"
        # Trim until it fits
        trimmed = text
        while trimmed and self.font.size(trimmed + ell)[0] > max_w:
            trimmed = trimmed[:-1]
        return self.font.render(trimmed + ell, True, self.text_color)
