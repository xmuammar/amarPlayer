from PySide6.QtCore import Signal, QPersistentModelIndex, QElapsedTimer, Qt
from PySide6.QtWidgets import QApplication, QListWidget, QScroller


class TapPlaylist(QListWidget):
    """Activate only a completed tap, never a drag or a kinetic-scroll stop."""

    itemTapped = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._tap_position = None
        self._tap_index = QPersistentModelIndex()
        self._tap_cancelled = True
        self._scroll_stopped = QElapsedTimer()
        self._previous_scroll_state = QScroller.Inactive
        self._scroller = QScroller.scroller(self.viewport())
        self._scroller.stateChanged.connect(self._scroll_state_changed)
        self.verticalScrollBar().valueChanged.connect(self._cancel_tap)
        # Android delivers synthesized mouse events too. Use one gesture path
        # so QScroller consumes the same events that QListWidget receives.
        QScroller.grabGesture(self.viewport(), QScroller.LeftMouseButtonGesture)

    def _cancel_tap(self, *args):
        self._tap_cancelled = True

    def _scroll_state_changed(self, state):
        if self._previous_scroll_state == QScroller.Scrolling and state != QScroller.Scrolling:
            # QScroller may stop before it forwards the press to this widget.
            self._scroll_stopped.start()
        self._previous_scroll_state = state
        if state in (QScroller.Dragging, QScroller.Scrolling):
            self._cancel_tap()

    def mousePressEvent(self, event):
        self._tap_position = event.position().toPoint()
        self._tap_index = QPersistentModelIndex(self.indexAt(self._tap_position))
        self._tap_cancelled = (
            event.button() != Qt.LeftButton
            or not self._tap_index.isValid()
            or (self._scroll_stopped.isValid() and self._scroll_stopped.elapsed() < 80)
            or self._scroller.state() in (QScroller.Dragging, QScroller.Scrolling)
        )
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._tap_position is not None:
            distance = (event.position().toPoint() - self._tap_position).manhattanLength()
            if distance >= QApplication.startDragDistance():
                self._cancel_tap()
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        position = event.position().toPoint()
        is_tap = (
            event.button() == Qt.LeftButton
            and self._tap_position is not None
            and not self._tap_cancelled
            and self._tap_index.isValid()
            and self._tap_index == self.indexAt(position)
            and (position - self._tap_position).manhattanLength() < QApplication.startDragDistance()
            and self._scroller.state() not in (QScroller.Dragging, QScroller.Scrolling)
        )
        self._tap_position = None
        self._tap_cancelled = True
        super().mouseReleaseEvent(event)
        if is_tap:
            self.itemTapped.emit(self.itemAt(position))


