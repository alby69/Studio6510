# C64 Studio Python - Project Proposal & Architecture

## 1. Overview
C64 Studio Python is a modern, cross-platform IDE for Commodore 64 development, inspired by CBM Prg Studio but built with Python 3.12+ and PySide6 (Qt6).

## 2. Technology Stack
- **Language:** Python 3.12+
- **UI Framework:** PySide6 (Qt6)
- **Data Storage:**
    - SQLite (for project assets and metadata)
    - YAML (for human-readable configuration)
- **External Tools Integration:**
    - KickAssembler (Default Assembler)
    - VICE (Default Emulator)
- **Graphics:** QGraphicsView for pixel-perfect editors.

## 3. Architecture

### Directory Structure
```text
c64studio/
├── src/
│   ├── main.py                # Entry point
│   ├── core/                  # Core logic
│   │   ├── project.py         # Project management
│   │   ├── settings.py        # Global settings
│   │   └── plugin_manager.py  # Plugin system
│   ├── models/                # Data models
│   │   ├── sprite.py
│   │   ├── charset.py
│   │   ├── tile.py
│   │   └── map.py
│   ├── ui/                    # UI Components
│   │   ├── main_window.py     # Main IDE Window (QMainWindow)
│   │   ├── dock_widgets/      # Dockable panels (Project Explorer, etc.)
│   │   └── widgets/           # Custom reusable widgets
│   ├── editors/               # Specialized editors
│   │   ├── base_editor.py     # Base class for all editors
│   │   ├── asm_editor.py      # Assembly code editor
│   │   ├── sprite_editor.py   # Sprite editor
│   │   ├── charset_editor.py  # Charset editor
│   │   └── map_editor.py      # Map/Tile editor
│   ├── compilers/             # Assembler wrappers
│   │   ├── base_compiler.py
│   │   └── kick_assembler.py
│   ├── emulators/             # Emulator wrappers
│   │   └── vice.py
│   └── utils/                 # Helpers (binutils, conversion, etc.)
├── assets/                    # Icons and resources
├── plugins/                   # Third-party plugins
├── tests/                     # Unit tests
├── requirements.txt
└── README.md
```

### Core Classes (MVC Pattern)
- **Model:** `Sprite`, `Charset`, `TileMap` classes holding the raw data.
- **View:** `SpriteEditorWidget`, `MapEditorWidget` using `QGraphicsView`.
- **Controller/Logic:** `Project` class managing the lifecycle and saving/loading.

## 4. Plugin System
A simple directory-based plugin system where each plugin can register:
- New Menu items.
- New Editor types.
- New Export formats.
