import pygame

_image_cache = {}
_sound_cache = {}
_font_cache = {}

def get_image(path):
    if path not in _image_cache:
        try:
            _image_cache[path] = pygame.image.load(path).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image {path}: {e}")
            # Create a placeholder surface if image fails to load
            placeholder = pygame.Surface((50, 50))
            placeholder.fill((255, 0, 255))
            _image_cache[path] = placeholder
    return _image_cache[path]

def get_sound(path):
    if path not in _sound_cache:
        try:
            _sound_cache[path] = pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"Error loading sound {path}: {e}")
            _sound_cache[path] = None
    return _sound_cache[path]

def get_font(name, size):
    key = (name, size)
    if key not in _font_cache:
        try:
             _font_cache[key] = pygame.font.Font(name, size)
        except pygame.error as e:
             print(f"Error loading font {name}: {e}")
             _font_cache[key] = pygame.font.Font(None, size) # Fallback to default
    return _font_cache[key]
