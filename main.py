import sys
from pathlib import Path

from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
from PySide6.QtCore import QTimer

from ui.main_window import MainWindow


def main():
    
    app = QApplication(sys.argv)

    # Caminho do ícone
    if getattr(sys, "frozen", False):
        base_dir = Path(sys.executable).parent
    else:
        base_dir = Path(__file__).resolve().parent

    icon_path = base_dir / "assets" / "icone.ico"

    if icon_path.exists():
        app.setWindowIcon(QIcon(str(icon_path)))

    window = MainWindow()

    if icon_path.exists():
        window.setWindowIcon(QIcon(str(icon_path)))

    window.showMaximized()
    
    # Aguarda renderização da janela antes de inicializar dados pesados
    def finish_initialization():
        window.finish_init()
    
    QTimer.singleShot(500, finish_initialization)
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()