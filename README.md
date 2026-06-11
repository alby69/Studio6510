# C64 Studio Python

Modern IDE for Commodore 64 development in Python.

## Description
Inspired by CBM Prg Studio, this project aims to provide a complete suite of tools for C64 development, including:
- Assembly Editor with 6502 syntax highlighting.
- Sprite, Charset, and Map editors.
- Build system integration (KickAssembler).
- Emulator integration (VICE).

## Documentation
Documentation can be found in the `docs/` folder:
- [Architecture](docs/ARCHITECTURE.md)
- [Roadmap](docs/ROADMAP.md)

## Requirements
- Python 3.12+
- PySide6
- PyYAML

## Setup

### Local Setup
```bash
pip install -r requirements.txt
python src/main.py
```

### Docker Setup
To run the IDE inside a Docker container (requires an X11 server on the host):

```bash
docker-compose up --build
```

On Linux, you might need to run `xhost +local:docker` before starting the container to allow access to the X server.
