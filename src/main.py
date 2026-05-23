import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from ui.main_window import MainWindow
from database.db_manager import DBManager

def main():
    # Windows Taskbar Icon Fix
    if os.name == 'nt':
        import ctypes
        myappid = 'routedesk.terminal.management.1.0'
        try:
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
        except Exception:
            pass

    # Make sure DB is initialized
    DBManager.init_db()
    
    app = QApplication(sys.argv)
    app.setApplicationName("RouteDesk")
    
    # Set global icon
    icon_path = os.path.join(os.path.dirname(__file__), "assets", "icon.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))
    
    # Load Global Styles
    style_path = os.path.join(os.path.dirname(__file__), "styles", "main.qss")
    if os.path.exists(style_path):
        with open(style_path, "r", encoding="utf-8") as f:
            app.setStyleSheet(f.read())
            
    # Show Login Window First
    from PyQt6.QtWidgets import QDialog
    from ui.login_window import LoginWindow
    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        operator_name = login.operator_name
        window = MainWindow(operator_name)
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit(0)

if __name__ == "__main__":
    main()
