from google.cloud import vision
from google.cloud import translate
from PyQt5.QtCore import QByteArray, QBuffer
import collections
WordBox = collections.namedtuple('WordBox', ['word', 'geometry'])


class ImageTranslator:

    def __init__(self, target_language='en'):
        self.__vision_client = vision.Client()
        self.__translate_client = translate.Client()
        self.__target_language = target_language

    def set_target_language(self, target_language):
        self.__target_language = target_language

    def translate_image_text(self, image):
        # image data to be fed to Google Cloud Vision API
        data = QByteArray()
        buffer = QBuffer(data)
        image.save(buffer, 'JPG')

        # Use Google Cloud Vision API's OCR capabilities to extract text from image
        img_to_translate = self.__vision_client.image(content = data.data())
        text_to_translate = img_to_translate.detect_text()

        word_boxes = []
        # Create WordBox namedtuples with the translation and bounding box of each word
        # Append each WordBox to word_boxes
        for word_data in text_to_translate[1:]:
            translated_word = self.__translate_client.translate(word_data.description, target_language=self.__target_language)
            boundary_vertices = word_data.bounds.vertices
            box = []
            for vertex in boundary_vertices:
                box.append((vertex.x_coordinate, vertex.y_coordinate))
            word_boxes.append(WordBox(word=translated_word['translatedText'], geometry=box))

        return word_boxes