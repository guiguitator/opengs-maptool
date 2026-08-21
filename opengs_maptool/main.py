from opengs_maptool.app import App
from opengs_maptool.ui.main_window import MainWindow

def main() -> int:
    # Import to initialize
    from opengs_maptool.services.logging_service import LOGGING_SERVICE

    app = App()

    window = MainWindow(app)
    window.show()

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
