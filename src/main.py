import sys
import os
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    app.setApplicationName("C64 Studio Python")
    app.setOrganizationName("C64StudioPy")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    # Add src to path if needed
    sys.path.append(os.path.dirname(__file__))
    main()
