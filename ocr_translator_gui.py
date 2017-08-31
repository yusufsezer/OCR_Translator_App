# GUI for OCR Text Translator App
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QFrame, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QByteArray, QBuffer
from image_capture import ImageCapture
from image_frame import ImageFrame
from image_translator import ImageTranslator

class TranslatorGUI (QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.imageCaptureDelegate = ImageCapture() # Webcam Image Capture Delegate
        self.translateDelegate = ImageTranslator() # OCR Text-in-Image Translator

    def init_ui(self):

        # Create layouts and add vertical layouts to the horizontal layout
        self.hLayout = QHBoxLayout()
        self.leftVLayout = QVBoxLayout()
        self.rightVLayout = QVBoxLayout()
        self.hLayout.addLayout(self.leftVLayout)
        self.hLayout.addLayout(self.rightVLayout)

        # Create and setup descriptive label
        self.welcomeLabel = QLabel("Welcome to the OCR (Optical Character Recognition) Translator App. "
                                   "Use this app to translate the text contained in images!")
        self.welcomeLabel.setWordWrap(True)

        # Create and setup buttons
        self.takePicBtn = QPushButton("Take a Picture")
        self.takePicBtn.clicked[bool].connect(self.take_picture)
        self.slctImgBtn = QPushButton("Select an Existing Image")
        self.slctImgBtn.clicked[bool].connect(self.select_existing_image)
        self.translateImgBtn = QPushButton("Translate Text in Image")
        self.translateImgBtn.clicked[bool].connect(self.translate_image_text)

        # Add appropriate widgets to the left vertical layout
        self.leftVLayout.addWidget(self.welcomeLabel)
        self.leftVLayout.addWidget(self.takePicBtn)
        self.leftVLayout.addWidget(self.slctImgBtn)
        self.leftVLayout.addWidget(self.translateImgBtn)

        # Create QImage and ImageFrame to display image
        self.image = QImage()
        self.imageFrame = ImageFrame()
        self.imageFrame.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))
        # self.frameBtn = QPushButton(self.imageFrame)
        # self.frameBtn.setText("EXAMPLE")
        # self.frameBtn.setGeometry((self.imageFrame.width / 2) - 250,
        #                           (self.imageFrame.width / self.imageFrame.aspectRatio / 2) - 250, 500, 500)
        self._load_image("default.jpg")

        # Add appropriate widgets to right vertical layout
        self.rightVLayout.addWidget(self.imageFrame)

        # setup and show window
        self.setLayout(self.hLayout)
        self.setWindowTitle("OCR Translator App")
        self.show()

    def take_picture(self):
        imageFileName = self.imageCaptureDelegate.capture_image()
        self._load_image(imageFileName)

    def select_existing_image(self):
        fileDialog = QFileDialog()
        imageFileName = fileDialog.getOpenFileName()
        self._load_image(imageFileName[0])

    def translate_image_text(self):
        self.translateDelegate.translate_image_text(self.image)

    def _load_image(self, fileName):
        self.image.load(fileName)
        imgWidth = self.image.width()
        imgAspectRatio = self.image.width() / self.image.height()
        self.imageFrame.setStyleSheet('border-image: url("%s")' % fileName)
        self.imageFrame.setAspectRatio(imgAspectRatio)
        self.imageFrame.setWidth(imgWidth)
        # self.frameBtn.setGeometry((self.imageFrame.width/2)-250,(self.imageFrame.width/self.imageFrame.aspectRatio/2)-250, 500, 500)
        # self.frameBtn.setStyleSheet('border-image: null; background-color: transparent')
