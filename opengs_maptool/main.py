from opengs_maptool.app import App
from opengs_maptool.ui.main_window import MainWindow


def main() -> int:
    app = App()

    window = MainWindow(app)
    window.show()
    
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
