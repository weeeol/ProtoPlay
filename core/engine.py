import json
import os

class EngineSettings:
    def __init__(self, filepath="project.json"):
        self.filepath = filepath
        self.data = {}
        self.load()

    def load(self):
        if os.path.exists(self.filepath):
            with open(self.filepath, 'r') as f:
                self.data = json.load(f)
        else:
            print(f"Warning: {self.filepath} not found. Using empty settings.")

    def save(self):
        with open(self.filepath, 'w') as f:
            json.dump(self.data, f, indent=4)

    def get(self, key, default=None):
        return self.data.get(key, default)

    def set(self, key, value):
        self.data[key] = value
        
    def __getattr__(self, name):
        if name in self.data:
            val = self.data[name]
            # Convert JSON lists to tuples for pygame colors
            if isinstance(val, list):
                return tuple(val)
            return val
        raise AttributeError(f"'EngineSettings' object has no attribute '{name}'")

# Global engine settings instance
settings = EngineSettings()
