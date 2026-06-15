import sys

from PySide6.QtWidgets import QApplication, QLabel, QMainWindow


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("NeuroForge")
        self.resize(1280, 720)
        placeholder = QLabel("NeuroForge — Phase 0 placeholder")
        placeholder.setStyleSheet("font-size: 24px; color: #888;")
        self.setCentralWidget(placeholder)


def main() -> None:
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
