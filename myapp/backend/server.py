from PySide6.QtCore import Signal, Slot, QJsonDocument
from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtNetwork import QHostAddress, QTcpServer
from PySide6.QtWebSockets import QWebSocketServer
import sys

PORT = 8001


class Server(QWebSocketServer):
    model_request = Signal(str)

    def __init__(self, parent=None):
        super().__init__(
            "Websocket Server", QWebSocketServer.SslMode.NonSecureMode, parent
        )
        if not self.listen(QHostAddress.LocalHost, PORT):
            print(f"Failed to listen on port {PORT}")
            sys.exit(-1)
        else:
            print(f"Listening on port {PORT}")
            print(f"Server URL: {self.serverUrl()}")

        self.newConnection.connect(self.on_new_connection)
        self._socket = None

    @Slot()
    def on_new_connection(self):
        self._socket = self.nextPendingConnection()
        self._socket.textMessageReceived.connect(self.on_text_message_received)
        self._socket.disconnected.connect(self.on_disconnected)

    @Slot(str)
    def send_message(self, message):
        if self._socket:
            self._socket.sendTextMessage(message)

    @Slot(str)
    def on_text_message_received(self, message):
        print(f"Received message: {message}")
        self.model_request.emit(message)

    def on_disconnected(self):
        socket = self.sender()
        if socket:
            socket.deleteLater()
            self._socket = None


if __name__ == "__main__":
    app = QApplication([])
    dialog = QDialog()
    server = Server()
    dialog.show()
    sys.exit(app.exec())
