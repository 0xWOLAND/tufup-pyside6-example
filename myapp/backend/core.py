from PySide6.QtCore import QObject, Signal, Slot, QJsonDocument, QThreadPool, QRunnable
from myapp.backend.server import Server
from json import loads, dumps
import asyncio
from time import time


class Core(QObject):
    def __init__(self, server: Server, parent=None):
        super().__init__(parent)
        self._server = server
        self.threadpool = QThreadPool()
        self.event_loop = asyncio.get_event_loop()

    @Slot(str)
    def receive(self, request):
        self.send(f"Received request: {request}")

    @Slot(str)
    def send(self, output):
        self._server.send_message(output)

    @Slot(str)
    def error(self, error):
        self._server.send_message(dumps({"error": error}))


if __name__ == "__main__":
    from PySide6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    server = Server()
    core = Core(server)
    sys.exit(app.exec())
