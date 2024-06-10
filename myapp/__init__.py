from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMenu
from PySide6.QtGui import QIcon

from myapp.backend.server import Server
from myapp.backend.core import Core
from myapp import settings

from tufup.client import Client
import logging
import sys
import shutil
import os
import resource_rc

logger = logging.getLogger(__name__)

__version__ = settings.APP_VERSION


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class DesktopApp(QWebEngineView):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("myapp")
        self.setGeometry(100, 100, 400, 300)

        index = QUrl("qrc:/myapp/frontend/dist/index.html")
        self.load(index)


class SystemTrayIcon(QMainWindow):
    def __init__(self):
        super().__init__()
        self.menu = QMenu()
        self.tray_icon = QSystemTrayIcon(QIcon(resource_path("icon.png")), self)
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.show()

        server = Server()
        self._core = Core(server)

        showAction = self.menu.addAction("Show")
        showAction.triggered.connect(self.show)

        self.show()

        self.menu.addSeparator()

        exitAction = self.menu.addAction("Exit")
        exitAction.triggered.connect(self.exit)

    def show(self):
        self.window = DesktopApp()
        self.window.show()

    def exit(self):
        sys.exit()


def progress_hook(bytes_downloaded: int, bytes_expected: int):
    progress_percent = bytes_downloaded / bytes_expected * 100
    print(f"\r{progress_percent:.1f}%", end="")
    if progress_percent >= 100:
        print("")


def update(pre: str):
    # Create update client
    client = Client(
        app_name=settings.APP_NAME,
        app_install_dir=settings.INSTALL_DIR,
        current_version=settings.APP_VERSION,
        metadata_dir=settings.METADATA_DIR,
        metadata_base_url=settings.METADATA_BASE_URL,
        target_dir=settings.TARGET_DIR,
        target_base_url=settings.TARGET_BASE_URL,
        refresh_required=False,
    )

    # Perform update
    new_update = client.check_for_updates(pre=pre)
    print(f"New update: {new_update}")
    if new_update:
        if new_update.custom:
            print("changes in this update:")
            for item in new_update.custom.get("changes", []):
                print(f"\t- {item}")
        # apply the update
        client.download_and_apply_update(
            skip_confirmation=True,
            progress_hook=progress_hook,
            purge_dst_dir=True,
            exclude_from_purge=None,
            log_file_name="install.log",
        )


def main(cmd_args):
    pre_release_channel = None
    while cmd_args:
        arg = cmd_args.pop(0)
        if arg in ["a", "b", "rc"]:
            pre_release_channel = arg

    for dir_path in [settings.INSTALL_DIR, settings.METADATA_DIR, settings.TARGET_DIR]:
        dir_path.mkdir(exist_ok=True, parents=True)

    if not settings.TRUSTED_ROOT_DST.exists():
        shutil.copy(src=settings.TRUSTED_ROOT_SRC, dst=settings.TRUSTED_ROOT_DST)
        logger.info("Trusted root metadata copied to cache.")

    print("Checking for updates...")
    print(f"Current version: {settings.APP_VERSION}")
    print(f"Pre-release channel: {pre_release_channel}")
    update(pre=pre_release_channel)

    if hasattr(sys, "_MEIPASS"):
        os.environ["QTWEBENGINEPROCESS_PATH"] = os.path.normpath(
            os.path.join(
                sys._MEIPASS,
                "PySide6",
                "Qt",
                "lib",
                "QtWebEngineCore.framework",
                "Helpers",
                "QtWebEngineProcess.app",
                "Contents",
                "MacOS",
                "QtWebEngineProcess",
            )
        )
        os.environ["QTWEBENGINE_RESOURCES_PATH"] = os.path.normpath(
            os.path.join(
                sys._MEIPASS,
                "..",
                "Resources",
                "PySide6",
                "Qt",
                "lib",
                "QtWebEngineCore.framework",
                "Resources",
            )
        )
        os.environ["QTWEBENGINE_LOCALES_PATH"] = os.path.normpath(
            os.path.join(
                sys._MEIPASS,
                "..",
                "Resources",
                "PySide6",
                "Qt",
                "lib",
                "QtWebEngineCore.framework",
                "Resources",
                "qtwebengine_locales",
            )
        )

    app = QApplication()
    app.setQuitOnLastWindowClosed(False)
    trayIcon = SystemTrayIcon()

    app.exec()
