from PyQt5.QtWidgets import QGraphicsPolygonItem
from PyQt5.QtWidgets import QGraphicsSceneHoverEvent
from PyQt5.QtGui import QBrush, QColor


class WordPolygon(QGraphicsPolygonItem):
    """Subclass of QGraphicsPolygonItem designed to display a translated word and its frame

    :type polygon: QPolygonF
    :param polygon: QPolygonF representing the frame of a translated word.

    :type text: QGraphicsTextItem
    :param text: QGraphicsTextItem representing the translated word.
    """

    def __init__(self, polygon=None, text=None) -> None:
        super().__init__(polygon)
        self.text = text
        self.setAcceptHoverEvents(True)
        self.setBrush(QBrush(QColor(51, 171, 249, 75)))

    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Shows word/makes frame opaque when mouse hovers over frame.

        :param event: hover enter event to handle
        """

        self.setBrush(QBrush(QColor(51, 171, 249, 255)))
        self.text.setOpacity(1)

    def hoverLeaveEvent(self, event: QGraphicsSceneHoverEvent) -> None:
        """Hides translated word/makes frame semi-transparent when mouse stops hovering over frame.

        :param event: hover leave event to handle
        """

        self.setBrush(QBrush(QColor(51, 171, 249, 75)))
        self.text.setOpacity(0)
