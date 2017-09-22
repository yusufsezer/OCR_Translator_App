from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QPoint
from PyQt5.QtGui import QPixmap, QPolygonF, QPolygon, QFont, QImage
from PyQt5.Qt import QDesktopWidget, QWheelEvent
from word_polygon import WordPolygon


class ImageView(QGraphicsView):
    """Subclassed QGraphicsView designed to display translated words over images

    :type default_image: QImage
    :param default_image: image to display when app starts. If not passed, no image is displayed when app starts.

    :type self.__currentImage: QImage
    :var self.__currentImage: Current image being displayed.

    :type self.__scene: QGraphicsScene
    :var self.__scene: The scene on which the image, translated words, and the frames of the translated words are shown.

    :type self.__word_polygons: list
    :var self.__word_polygons: list of lists. Each sublist contains a QGraphicsTextItem and a WordPolygon.
    """

    def __init__(self, default_image=None) -> None:
        super().__init__()
        self.__scene = QGraphicsScene()
        self.__currentImage = default_image
        self.__word_polygons = []

        self.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        if default_image:
            self.set_image(default_image)

        self.setScene(self.__scene)

    def set_image(self, image: QImage) -> None:
        """Sets the background image for self

        :param image: image to set as background of self
        """

        self.__scene.clear()
        self.__word_polygons = []

        screen_res = QDesktopWidget().screenGeometry()
        image = image.scaled(screen_res.width() * 0.75, screen_res.height() * 0.75, Qt.KeepAspectRatio)
        bg = QGraphicsPixmapItem(QPixmap(image))
        self.setFixedSize(image.width(),  image.height())
        self.__currentImage = image
        self.__scene.addItem(bg)

    def draw_word_boxes(self, word_boxes: list) -> None:
        """Sets up and draws translated words and their corresponding frames

        :param word_boxes: list of WordBox namedtuples, each representing a word and frame to be drawn.
                           ex: [WordBox('word'=str, 'geometry'=[(int, int)], WordBox('word'=str, 'geometry'=[(int, int)])

        """

        for wPoly in self.__word_polygons:
            self.__scene.removeItem(wPoly[0])
            self.__scene.removeItem(wPoly[1])

        self.__word_polygons = []

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

            self.__word_polygons.append([text, frame])
            self.__scene.addItem(frame)
            self.__scene.addItem(text)

    def get_current_image(self) -> QImage:
        """Returns current image being displayed

        :return: Image that is currently being displayed.
        """

        return self.__currentImage

    def wheelEvent(self, event: QWheelEvent) -> None:
        """Overriden method that prevents scrolling via mouse wheel/touch pad gestures.

        :param event: event to handle
        """

        pass
