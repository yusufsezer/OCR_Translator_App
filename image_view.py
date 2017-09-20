from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPolygonF, QPolygon, QFont
from word_polygon import WordPolygon


class ImageView(QGraphicsView):
    """Subclassed QGraphicsView designed to display translated words over images

    :type default_image: QImage
    :param default_image: image to display when app starts. If not passed, no image is displayed when app starts.
    """

    def __init__(self, default_image=None):
        super().__init__()
        self.scene = QGraphicsScene()

        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if default_image:
            self.set_image(default_image)

        self.setScene(self.scene)

    def set_image(self, image):
        """Sets the background image for self

        :type image: QImage
        :param image: image to set as background of self

        :rtype None
        """

        self.scene.clear()
        bg = QGraphicsPixmapItem(QPixmap(image))
        self.setFixedSize(image.width(), image.height())
        self.scene.addItem(bg)

    def draw_word_boxes(self, word_boxes):
        """Sets up and draws translated words and their corresponding frames

        :type word_boxes: list
        :param word_boxes: list of WordBox namedtuples, each representing a word and frame to be drawn

        :rtype None
        """

        for word_box in word_boxes:
            points = list(map(lambda x: QPoint(x[0], x[1]), word_box.geometry))

            text = QGraphicsTextItem(word_box.word)
            text.setOpacity(0)
            text.setAcceptHoverEvents(False)

            font = QFont()
            font.setPixelSize(abs(points[0].y() - points[3].y()))
            text.setFont(font)

            w = text.boundingRect().width()
            h = text.boundingRect().height()
            text.setPos(points[0].x() + abs(points[0].x()-points[1].x())/2 - w/2,
                        points[0].y() + abs(points[0].y() - points[3].y())/2 - h/2)
            frame = WordPolygon(QPolygonF(QPolygon(points)), text)

            self.scene.addItem(frame)
            self.scene.addItem(text)

    def wheelEvent(self, event):
        """Overriden method that prevents scrolling via mouse wheel/touch pad gestures.

        :type event: QWheelEvent
        :param event: event to handle

        :rtype None
        """

        pass
