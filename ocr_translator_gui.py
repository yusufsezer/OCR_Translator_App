from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QFrame, QSizePolicy, QComboBox
from PyQt5.QtGui import QImage, QPolygon, QPolygonF, QRegion, QPainterPath, QPainter, QPen, QBrush
from PyQt5.QtCore import QByteArray, QBuffer, QPoint
from image_capture import ImageCapture
from image_frame import ImageFrame
from image_translator import ImageTranslator
# import collections
# WordBox = collections.namedtuple('WordBox', ['word', 'geometry'])


class TranslatorGUI (QWidget):

    language_codes = {'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Chinese': 'zh'}

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.imageCaptureDelegate = ImageCapture() # Webcam Image Capture Delegate
        self.translateDelegate = ImageTranslator() # OCR Text-in-Image Translator Delegate

    def init_ui(self):

        # Create one horizontal and two vertical layouts
        # Add both vertical layouts to the horizontal layouts
        self.hLayout = QHBoxLayout()
        self.leftVLayout = QVBoxLayout()
        self.rightVLayout = QVBoxLayout()
        self.hLayout.addLayout(self.leftVLayout)
        self.hLayout.addLayout(self.rightVLayout)

        # Create and setup descriptive label
        self.welcomeLabel = QLabel("Welcome to the OCR (Optical Character Recognition) Translator App. "
                                   "Use this app to translate the text contained in images!")
        self.welcomeLabel.setWordWrap(True)

        # Create and setup buttons/combobox
        self.takePicBtn = QPushButton("Take a Picture")
        self.takePicBtn.clicked[bool].connect(self.__take_picture)
        self.slctImgBtn = QPushButton("Select an Existing Image")
        self.slctImgBtn.clicked[bool].connect(self.__select_existing_image)
        self.translateImgBtn = QPushButton("Translate Text in Image")
        self.translateImgBtn.clicked[bool].connect(self.__translate_image_text)
        self.selectTargetLanguageBox = QComboBox()
        self.selectTargetLanguageBox.addItems(['English', 'Spanish', 'French', 'German', 'Chinese'])

        # Add appropriate widgets to the left vertical layout
        self.leftVLayout.addWidget(self.welcomeLabel)
        self.leftVLayout.addWidget(self.selectTargetLanguageBox)
        self.leftVLayout.addWidget(self.takePicBtn)
        self.leftVLayout.addWidget(self.slctImgBtn)
        self.leftVLayout.addWidget(self.translateImgBtn)

        # Create QImage and ImageFrame to display image
        # Load image into QImage
        self.image = QImage()
        self.imageFrame = ImageFrame()
        self.imageFrame.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # self.frameBtn = QPushButton(self.imageFrame)
        # self.frameBtn.setText("EXAMPLE")
        # self.frameBtn.setGeometry((self.imageFrame.width / 2) - 250,
        #                           (self.imageFrame.width / self.imageFrame.aspectRatio / 2) - 250, 500, 500)
        self.__load_image("default.jpg")

        # Add appropriate widgets to right vertical layout
        self.rightVLayout.addWidget(self.imageFrame)

        # setup and show window
        self.setLayout(self.hLayout)
        self.setWindowTitle("OCR Translator App")
        self.show()

    def __take_picture(self):
        imageFileName = self.imageCaptureDelegate.capture_image()
        self.__load_image(imageFileName)

    def __select_existing_image(self):
        fileDialog = QFileDialog()
        imageFileName = fileDialog.getOpenFileName()
        self.__load_image(imageFileName[0])

    def __translate_image_text(self):
        self.translateDelegate.set_target_language(TranslatorGUI.language_codes[self.selectTargetLanguageBox.currentText()])

        data = QByteArray()
        buffer = QBuffer(data)
        self.image.save(buffer, 'JPG')

        word_boxes = self.translateDelegate.translate_image_text(data.data())
        self.__draw_word_boxes(word_boxes)

    def __load_image(self, fileName):
        self.image.load(fileName)
        imgWidth = self.image.width()
        imgAspectRatio = self.image.width() / self.image.height()
        self.imageFrame.setStyleSheet('border-image: url("%s")' % fileName)
        self.imageFrame.setAspectRatio(imgAspectRatio)
        self.imageFrame.setWidth(imgWidth)
        # self.frameBtn.setGeometry((self.imageFrame.width/2)-250,(self.imageFrame.width/self.imageFrame.aspectRatio/2)-250, 500, 500)
        # self.frameBtn.setStyleSheet('border-image: null; background-color: transparent')

    def __draw_word_boxes(self, word_boxes):
        word_box = word_boxes[0]
        word_vertices = word_box.geometry
        print(word_box)
        print(word_vertices)
        btn = QPushButton()
        btn.setText(word_box.word)
        btn.setStyleSheet("background-color: darkBlue; border-style: none")
        poly = QPolygon()
        flattened_vertices = []
        # for point in word_vertices:
        #     print(point[0])
        #     flattened_vertices.append(QPoint(point[0], point[1]))
        print(flattened_vertices)
        flattened_vertices = [coordinate for li in word_vertices for coordinate in li]
        print(flattened_vertices)
        poly.setPoints([4] + flattened_vertices)
        btn.setMask(QRegion(poly))
        self.rightVLayout.addWidget(btn)
        # print(1)
        # painter = QPainter(self.imageFrame)
        # painter.begin(self.imageFrame)
        # print(2)
        # path = QPainterPath()
        # print(3)
        # path.addPolygon(QPolygonF(poly))
        # print(4)
        # pen = QPen()
        # pen.setWidth(45)
        # painter.
        # painter.drawEllipse(100.0, 200.0, 800.0, 600.0)
        # painter.drawPath(path)
        # print('done')
