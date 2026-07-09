# ProtoPlay Engine Rules

When assisting with this project, strictly follow these architectural guidelines:

1. **Frameworks:** The engine is built on `pygame-ce` (Pygame Community Edition) and `pygame_gui`. Do NOT use `imgui` or built-in `tkinter` for in-game UI.
2. **Data-Driven Settings:** All configurable variables (physics, visuals, speeds) MUST be stored in `project.json` and accessed via `core.engine.settings`.
3. **Dynamic Lookups:** Entities (like `Player`, `Enemy`) must fetch settings dynamically during their `update(dt)` methods (e.g., `settings.PLAYER_SPEED`) rather than caching them in `__init__`, to allow for live editing without restarting.
4. **Sub-Pixel Movement:** Pygame `Rect`s lose float precision. For entities that move, track float positions internally (e.g., `self.exact_x`) and round to `self.rect.x` to prevent slow-moving objects from completely stopping due to float truncation.
5. **Editor UI:** Any new UI elements or editor tools should be added to `core/editor_ui.py` and styled using `assets/theme.json`.
