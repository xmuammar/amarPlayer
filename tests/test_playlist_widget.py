import os
os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')

import unittest
from PySide6.QtCore import QPoint, QPointF, Qt
from PySide6.QtTest import QTest
from PySide6.QtWidgets import QApplication, QScroller
from playlist_widget import TapPlaylist


class PlaylistTapTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.widget = TapPlaylist()
        self.widget.resize(320, 250)
        self.widget.addItems([f'Track {i}' for i in range(60)])
        self.widget.show()
        QTest.qWait(20)
        self.played = []
        self.widget.itemTapped.connect(lambda item: self.played.append(item.text()))
        self.viewport = self.widget.viewport()
        self.point = self.widget.visualItemRect(self.widget.item(1)).center()

    def tearDown(self):
        self.widget.close()
        self.widget.deleteLater()
        self.app.processEvents()

    def test_tap_plays_once(self):
        QTest.mouseClick(self.viewport, Qt.LeftButton, pos=self.point)
        QTest.qWait(300)
        self.assertEqual(self.played, ['Track 1'])

    def test_drag_does_not_play_and_next_tap_works(self):
        start = QPoint(100, 190)
        QTest.mousePress(self.viewport, Qt.LeftButton, pos=start)
        for y in range(180, 40, -10):
            QTest.mouseMove(self.viewport, QPoint(100, y), delay=15)
        QTest.mouseRelease(self.viewport, Qt.LeftButton, pos=QPoint(100, 40))
        QTest.qWait(300)
        self.assertEqual(self.played, [])
        QScroller.scroller(self.viewport).stop()
        QTest.qWait(100)
        QTest.mouseClick(self.viewport, Qt.LeftButton, pos=QPoint(100, 100))
        QTest.qWait(300)
        self.assertEqual(len(self.played), 1)

    def test_small_jitter_is_tap(self):
        QTest.mousePress(self.viewport, Qt.LeftButton, pos=self.point)
        QTest.mouseMove(self.viewport, self.point + QPoint(1, 1))
        QTest.mouseRelease(self.viewport, Qt.LeftButton, pos=self.point + QPoint(1, 1))
        QTest.qWait(300)
        self.assertEqual(self.played, ['Track 1'])

    def test_tap_stops_kinetic_scroll_without_playing(self):
        scroller = QScroller.scroller(self.viewport)
        scroller.scrollTo(QPointF(0, 400), 1000)
        QTest.qWait(100)
        self.assertEqual(scroller.state(), QScroller.Scrolling)
        QTest.mouseClick(self.viewport, Qt.LeftButton, pos=QPoint(100, 100))
        QTest.qWait(300)
        self.assertEqual(self.played, [])

    def test_release_outside_does_not_play(self):
        QTest.mousePress(self.viewport, Qt.LeftButton, pos=self.point)
        QTest.mouseRelease(self.viewport, Qt.LeftButton, pos=QPoint(-50, -50))
        QTest.qWait(300)
        self.assertEqual(self.played, [])

    def test_right_click_does_not_play(self):
        QTest.mouseClick(self.viewport, Qt.RightButton, pos=self.point)
        self.assertEqual(self.played, [])


if __name__ == '__main__':
    unittest.main()
