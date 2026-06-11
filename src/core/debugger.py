import socket
import threading
import time
from PySide6.QtCore import QObject, Signal

class VICEDebugger(QObject):
    connected = Signal(bool)
    registersUpdated = Signal(dict)
    disconnected = Signal()

    def __init__(self, host="127.0.0.1", port=6502):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = None
        self.running = False
        self._thread = None

    def connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(2)
            self.sock.connect((self.host, self.port))
            self.running = True
            self._thread = threading.Thread(target=self._listen, daemon=True)
            self._thread.start()
            self.connected.emit(True)
            return True
        except Exception as e:
            print(f"Debugger connection failed: {e}")
            self.connected.emit(False)
            return False

    def disconnect(self):
        self.running = False
        if self.sock:
            self.sock.close()
        self.disconnected.emit()

    def send_command(self, cmd):
        if self.sock:
            try:
                self.sock.send(f"{cmd}\n".encode())
            except Exception as e:
                print(f"Error sending command: {e}")
                self.disconnect()

    def step(self):
        self.send_command("z") # Step

    def next(self):
        self.send_command("n") # Next

    def run(self):
        self.send_command("g") # Go/Run

    def break_exec(self):
        self.send_command("\x03") # Ctrl+C to break

    def _listen(self):
        buffer = ""
        while self.running:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                buffer += data
                if "\n" in buffer:
                    lines = buffer.split("\n")
                    for line in lines[:-1]:
                        self._handle_line(line)
                    buffer = lines[-1]
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Debugger listen error: {e}")
                break
        self.running = False
        self.disconnected.emit()

    def _handle_line(self, line):
        # VICE monitor output parsing
        # Example: ADDR: 0810, A: 00, X: 00, Y: 00, SP: f6, FLAGS: 32
        if "A:" in line and "X:" in line:
            parts = line.split(",")
            regs = {}
            for p in parts:
                if ":" in p:
                    k, v = p.split(":")
                    regs[k.strip()] = v.strip()
            self.registersUpdated.emit(regs)
