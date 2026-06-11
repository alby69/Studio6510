# C64 Studio Python - Development Roadmap

## Phase 1: Foundation (The IDE)
- [x] Basic project structure and requirements.
- [x] Main Window with `QDockWidget` system.
- [x] Project Explorer (File system tree).
- [x] Simple Text Editor for Assembly (with syntax highlighting).
- [x] Settings Management (paths to VICE/KickAssembler).

## Phase 2: Build & Run
- [x] Wrapper for KickAssembler (run process, parse errors).
- [x] Wrapper for VICE (launch PRG).
- [x] Console output window in the IDE.

## Phase 3: Graphics Suite - Sprite Editor
- [x] Pixel grid drawing.
- [x] Palette management (C64 colors).
- [x] Multicolor/Single color toggle (UI + Model).
- [x] Animation preview (UI + Timer logic).
- [x] Export to ASM (Basic Data blocks).

## Phase 4: Graphics Suite - Charset Editor
- [x] 8x8 character editing.
- [x] Import/Export from/to binary and ASM.

## Phase 5: Map & Screen Designer
- [x] Tile creation from Charset (Model).
- [x] Map painting (Basic grid painting).
- [x] Screen layout tool (Basic Screen Designer).

## Phase 6: Advanced Features
- [x] Debugger integration (VICE remote monitor).
- [x] Git integration.
- [x] Plugin API (Plugin Manager + Loading logic).
