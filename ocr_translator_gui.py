from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QFrame, QSizePolicy, QComboBox
from PyQt5.QtGui import QImage
from image_capture import ImageCapture
from image_frame import ImageFrame
from image_translator import ImageTranslator


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
        word_boxes = self.translateDelegate.translate_image_text(self.image)
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
        print(word_boxes)
