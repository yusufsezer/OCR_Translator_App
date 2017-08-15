# Inherits from QFrame
# Reimplements sizeHint() so that ImageFrame instances default to half the width and half the height of their parent
# Reimplements heightForWidth() so that ImageFrame instances maintain the same aspect ratio of the image they display

from PyQt5.QtWidgets import QFrame, QDesktopWidget
from PyQt5.QtCore import QSize

class ImageFrame(QFrame):

    def __init__(self, aspectRatio = .66, width = 600):
        super().__init__()
        self.aspectRatio = aspectRatio
        self.width = width

    def sizeHint(self):
        return QSize(self.width, self.heightForWidth(self.width))
        #return QSize(900, 900)

    def heightForWidth(self, width):
        return width / self.aspectRatio

    def setAspectRatio(self, aspectRatio):
        self.aspectRatio = aspectRatio

    def setWidth(self, width):
        screenWidth = QDesktopWidget().screenGeometry(-1).width()
        if width > screenWidth / 3:
            self.width = screenWidth / 3
        else:
            self.width = width