import json
from pathlib import Path

DEFAULT_CONFIG = {
    "location": {
        "latitude": 40.7128,
        "longitude": -74.0060
    },
    "units": "metric",
    "update_interval_seconds": 60
}

class Config:
    def __init__(self, path="config.json"):
        self.path = Path(path)
        self.data = DEFAULT_CONFIG.copy()
        self.load()

    def load(self):
        if self.path.exists():
            with open(self.path, "r") as f:
                self.data.update(json.load(f))

    def get(self, key, default=None):
        return self.data.get(key, default)