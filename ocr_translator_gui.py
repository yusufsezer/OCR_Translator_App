from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QFileDialog, QComboBox
from PyQt5.QtGui import QImage
from PyQt5.QtCore import QByteArray, QBuffer
from image_capture import ImageCapture
from image_view import ImageView
from image_translator import ImageTranslator


class TranslatorGUI (QWidget):
    """Subclass of QWidget that serves as the main window and interface for the application.

    :type self.imageCaptureDelegate: ImageCapture
    :var self.imageCaptureDelegate: Uses OpenCV to access webcam and take pictures with it.

    :type self.translateDelegate: ImageTranslator
    :var self.translateDelegate: Delegate that handles requests to Google's Cloud Vision/Translate APIs

    :type self.imageView: ImageView
    :var self.imageView: The object that displays the image and handles drawing translated words and their frames.
    """

    def __init__(self) -> None:
        super().__init__()
        self.init_ui()
        self.imageCaptureDelegate = ImageCapture()
        self.translateDelegate = ImageTranslator()

    def init_ui(self) -> None:
        """Initializes the application's Graphical User Interface.
        """

        # Create necessary layouts
        h_layout = QHBoxLayout()
        left_v_layout = QVBoxLayout()
        right_v_layout = QVBoxLayout()
        h_layout.addLayout(left_v_layout)
        h_layout.addLayout(right_v_layout)

        # Create and setup descriptive label, buttons, and combo box
        welcome_label = QLabel("Welcome to the OCR (Optical Character Recognition) Translator App. "
                               "Use this app to translate the text contained in images!")
        welcome_label.setWordWrap(True)
        take_pic_btn = QPushButton("Take a Picture")
        take_pic_btn.clicked[bool].connect(self.__take_picture)
        slct_img_btn = QPushButton("Select an Existing Image")
        slct_img_btn.clicked[bool].connect(self.__select_existing_image)
        translate_img_btn = QPushButton("Translate Text in Image")
        translate_img_btn.clicked[bool].connect(self.__translate_image_text)
        select_target_language_box = QComboBox()
        select_target_language_box.addItems(['English', 'Spanish', 'French', 'German', 'Chinese', 'Turkish'])
        select_target_language_box.currentIndexChanged.connect(lambda x: self.__set_target_language(select_target_language_box))

        # Initialize ImageView instance to display image
        self.imageView = ImageView(QImage())

        # Add appropriate widgets to the left and right vertical layouts
        left_v_layout.addWidget(welcome_label)
        left_v_layout.addWidget(select_target_language_box)
        left_v_layout.addWidget(take_pic_btn)
        left_v_layout.addWidget(slct_img_btn)
        left_v_layout.addWidget(translate_img_btn)
        right_v_layout.addWidget(self.imageView)

        # setup and show window
        self.setLayout(h_layout)
        self.setWindowTitle("OCR Translator App")
        self.show()

    def __take_picture(self) -> None:
        """Launches image capture window, allows user to take image, then loads it.
        """

        image_file_name = self.imageCaptureDelegate.capture_image()
        self.__load_image(image_file_name)

    def __select_existing_image(self) -> None:
        """Launches file dialog box, allows user to select an existing image, then loads it.
        """

        file_dialog = QFileDialog()
        image_file_name = file_dialog.getOpenFileName()
        self.__load_image(image_file_name[0])

    def __set_target_language(self, box: QComboBox) -> None:
        """Sets the target language for translation requests based on the currently selected value in the combo box.
        """

        self.translateDelegate.set_target_language(box.currentText())

    def __translate_image_text(self) -> None:
        """Requests OCR translation from self.translateDelegate, and triggers drawing of translation.
        """

        data = QByteArray()
        buffer = QBuffer(data)
        self.imageView.get_current_image().save(buffer, 'JPG')

        word_boxes = self.translateDelegate.translate_image_text(data.data())
        self.imageView.draw_word_boxes(word_boxes)

    def __load_image(self, file_name: str) -> None:
        """Triggers display of image in self.imageView

        :param file_name: the file name of the image to be loaded.
        """

        self.imageView.set_image(QImage(file_name))
