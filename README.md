# ProtoPlay Engine

**ProtoPlay** has evolved from a simple prototype into a **data-driven, no-code 2D Game Engine** built entirely in Python using `pygame-ce` and `pygame_gui`. 

It comes with a fully playable platformer out of the box, but its true power lies in its **live-editing capabilities**. You can build levels, tweak physics, and import assets—all while the game is running, without writing a single line of code.

## Features

### 🛠️ In-Game Editor Suite
Press **`TAB`** at any time during gameplay to open the Engine Overlay!
* **Property Inspector:** A live-updating control panel. Use sliders and text boxes to change `GRAVITY`, `PLAYER_SPEED`, `JUMP_STRENGTH`, and more. Changes are applied instantly and saved to your `project.json`.
* **Level Painter:** Pause the physics and use your mouse to paint blocks, coins, enemies, and player spawns directly onto the screen. Hit "Save Level" to instantly commit your design to disk.
* **Asset Importer:** Browse your computer and import `.png` or `.wav` files directly into the project from within the engine.

### 🎮 Gameplay Mechanics
* **State Machine Architecture:** Clean transitions between Main Menu, Gameplay, and Game Over states.
* **Fluid Platforming:** Smooth continuous movement and double-jump capabilities.
* **Combat & Interactions:** Enemy patrols, coin collection, health systems, and invincibility frames.
* **Dynamic Resolution:** Change the screen width and height in the engine; the game window and UI adapt instantly.

## Installation & Setup

1. **Prerequisites:** Ensure you have Python 3 installed.
2. **Install Dependencies:**
   ```bash
   pip install pygame-ce pygame_gui
   ```
3. **Run the Engine:**
   ```bash
   python main.py
   ```

## Controls

* **Arrow Keys / WASD:** Move left and right.
* **Up Arrow / Spacebar:** Jump (hold to jump continuously, press again mid-air to double jump).
* **ESC:** Pause / Unpause the game.
* **TAB:** Toggle the Engine Editor Mode.

## Project Structure

* `main.py` - The core application loop and entry point.
* `project.json` - The data-driven configuration file containing all live variables.
* `core/` - The engine guts (Scene management, State Machine, Resource Caching, Editor UI).
* `entities/` - Game objects (Player, Enemy, Coin, Block).
* `states/` - Logic for different game screens (Menu, Gameplay).
* `levels/` - Text-based grid representations of the maps.
* `assets/` - Images and sound files.
