import os
from dotenv import load_dotenv
from pynput import keyboard
from PySide6 import QtCore, QtGui, QtWidgets
import mss
from PIL import Image
import pytesseract

try:
    from openai import OpenAI
except Exception:  # pragma: no cover
    OpenAI = None

load_dotenv()

HOTKEY = os.getenv("HOTKEY", "<ctrl>+<alt>+c")
PROVIDER = os.getenv("PROVIDER", "openai")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
ANSWER_MAX_TOKENS = int(os.getenv("ANSWER_MAX_TOKENS", "256"))

_client = None
if PROVIDER == "openai" and OpenAI is not None and os.getenv("OPENAI_API_KEY"):
    _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def ask_model(text: str) -> str:
    if _client is None:
        return "LLM not configured"
    resp = _client.responses.create(
        model=MODEL_NAME,
        input=f"You are a concise explainer. Explain this text briefly:\n{text}",
        max_output_tokens=ANSWER_MAX_TOKENS,
    )
    return resp.output_text


class CircleOverlay(QtWidgets.QWidget):
    def __init__(self, callback):
        super().__init__()
        self.callback = callback
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint | QtCore.Qt.FramelessWindowHint
        )
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.setWindowState(QtCore.Qt.WindowFullScreen)
        self.start = None
        self.end = None

    def mousePressEvent(self, event):
        self.start = event.pos()
        self.end = event.pos()
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    def mouseReleaseEvent(self, event):
        self.end = event.pos()
        self.grab_region()
        self.close()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtGui.QColor(0, 0, 0, 100))
        if self.start and self.end:
            rect = QtCore.QRect(self.start, self.end).normalized()
            painter.setCompositionMode(QtGui.QPainter.CompositionMode_Clear)
            painter.drawEllipse(rect)

    def grab_region(self):
        rect = QtCore.QRect(self.start, self.end).normalized()
        with mss.mss() as sct:
            monitor = {
                "top": rect.top(),
                "left": rect.left(),
                "width": rect.width(),
                "height": rect.height(),
            }
            img = sct.grab(monitor)
            pil = Image.frombytes("RGB", img.size, img.rgb)
            self.callback(pil, rect.center())


class CircleApp(QtWidgets.QApplication):
    def __init__(self):
        super().__init__([])
        self.listener = keyboard.GlobalHotKeys({HOTKEY: self.trigger_overlay})
        self.listener.start()
        print(f"CircleQ running. Press {HOTKEY} to capture. Ctrl+C to quit.")

    def trigger_overlay(self):
        QtCore.QTimer.singleShot(0, self.open_overlay)

    def open_overlay(self):
        overlay = CircleOverlay(self.process_capture)
        overlay.show()

    def process_capture(self, image: Image.Image, pos: QtCore.QPoint):
        text = pytesseract.image_to_string(image)
        answer = ask_model(text)
        self.show_bubble(answer, pos)

    def show_bubble(self, answer: str, pos: QtCore.QPoint):
        label = QtWidgets.QLabel(answer)
        label.setWindowFlags(QtCore.Qt.ToolTip)
        label.move(pos.x(), pos.y())
        label.show()
        QtCore.QTimer.singleShot(5000, label.close)


def main():
    app = CircleApp()
    app.exec()


if __name__ == "__main__":
    main()
