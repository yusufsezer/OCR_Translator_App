# GUI for OCR Text Translator App
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QFrame
from PyQt5.QtGui import QPixmap, QImage
from image_capture import ImageCapture

class TranslatorGUI (QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.imageCaptureDelegate = ImageCapture() # Webcam Image Capture Delegate

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

        # Create label and fill with default image
        # self.imageDisplay = QPixmap("default.jpg")
        # self.imageLabel = QLabel()
        # self.imageLabel.setPixmap(self.imageDisplay.scaledToHeight(self.height()))

        self.img = QImage()
        self.img.load('default.jpg')
        print(self.img.size())
        self.imageFrame = QFrame()
        self.imageFrame.setStyleSheet('border-image: url("default.jpg")')
        # self.frameBtn = QPushButton(self.imageFrame)
        # self.frameBtn.setText("EXAMPLE")
        # self.frameBtn.setStyleSheet('background-color: blue')
        # self.frameBtn.setGeometry(self.imageFrame.size().width()/2, self.imageFrame.height()/2, 100, 200)

        # Add appropriate widgets to right vertical layout
        self.rightVLayout.addWidget(self.imageFrame)




        # setup and show window
        self.setLayout(self.hLayout)
        self.setWindowTitle("OCR Translator App")
        self.show()

    def take_picture(self):
        imageFileName = self.imageCaptureDelegate.capture_image()
        self._load_image(imageFileName)
        # self.frameBtn.setGeometry(self.imageFrame.size().width()/2-50, self.imageFrame.height()/2-100, 100, 200)

        pass

    def select_existing_image(self):
        fileDialog = QFileDialog()
        imageFileName = fileDialog.getOpenFileName()
        print(imageFileName)
        self._load_image(imageFileName)
        print("Select an Existing Image")
        pass

    def translate_image_text(self):
        print("Translate Text in Image")
        pass

    def _load_image(self, fileName):
        self.imageDisplay.load(fileName)
        self.imageLabel.setPixmap(self.imageDisplay.scaledToHeight(self.height()))
        pass