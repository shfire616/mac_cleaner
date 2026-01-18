import sys
import os

# Ensure project root is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication

from src.ui.main_window import MainWindow

from src.ui.styles import apply_styles



def main():

    print("Initializing Application...")

    app = QApplication(sys.argv)

    

    # Apply Global Theme

    apply_styles(app)

    

    print("Creating Main Window...")



    try:

        window = MainWindow()

        window.show()

        print("Window shown. Starting event loop...")

        sys.exit(app.exec())

    except Exception as e:

        print(f"Error starting app: {e}")

        import traceback

        traceback.print_exc()



if __name__ == "__main__":

    main()
