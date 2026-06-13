import os
import time
import random


class QuotesProvider:
    def __init__(self, config):
        qcfg = config.get("quotes", {})

        self.enabled = bool(qcfg.get("enabled", False))
        self.file = qcfg.get("file", "assets/quotes.txt")
        self.shuffle = bool(qcfg.get("shuffle", True))
        self.rotate_interval = int(qcfg.get("rotate_interval", 60))

        self.quotes = []
        self.index = 0
        self.last_rotate = 0

        if self.enabled:
            self._load()

    def _load(self):
        path = self.file

        # Allow relative path from project root
        if not os.path.isabs(path):
            root = os.path.dirname(os.path.dirname(__file__))
            path = os.path.join(root, path)

        if not os.path.exists(path):
            print("💬 quotes file missing:", path)
            self.quotes = []
            return

        try:
            with open(path, "r", encoding="utf-8") as f:
                self.quotes = [line.strip() for line in f if line.strip()]

            if not self.quotes:
                print("💬 quotes file is empty:", path)
                return

            if self.shuffle:
                random.shuffle(self.quotes)

            self.last_rotate = time.time()

        except Exception as e:
            print("💬 failed to load quotes:", e)
            self.quotes = []

    def update(self):
        if not self.enabled or not self.quotes:
            return

        if time.time() - self.last_rotate > self.rotate_interval:
            self.index = (self.index + 1) % len(self.quotes)
            self.last_rotate = time.time()

    def current_quote(self):
        if not self.enabled or not self.quotes:
            return ""
        return self.quotes[self.index]

    # ✅ Compatibility method (fixes your earlier mismatch)
    def current(self):
        return self.current_quote()
