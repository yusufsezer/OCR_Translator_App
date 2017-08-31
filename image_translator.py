from google.cloud import vision
from google.cloud import translate
from PyQt5.QtCore import QByteArray, QBuffer


class ImageTranslator:

    def __init__(self, target_language = 'en'):
        self.__vision_client = vision.Client()
        self.__translate_client = translate.Client()
        self.__target_language = target_language

    def set_target_language(self, target_language):
        self.__target_language = target_language

    def translate_image_text(self, image):
        data = QByteArray()
        buffer = QBuffer(data)
        image.save(buffer, 'JPG')
        img_to_translate = self.__vision_client.image(content = data.data())
        text_to_translate = img_to_translate.detect_text()[0].description
        print(text_to_translate)
        translation = self.__translate_client.translate(text_to_translate, target_language=self.__target_language)
        print(translation)