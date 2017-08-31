from PyQt5.QtGui import QImage
from google.cloud import vision
from google.cloud import translate
from PyQt5.QtCore import QByteArray, QBuffer
import base64

class ImageTranslator:

    def __init__(self):
        self.vision_client = vision.Client()
        self.translate_client = translate.Client()

    def translate_image_text(self, image):
        data = QByteArray()
        buffer = QBuffer(data)
        image.save(buffer, 'JPG')
        imgToTranslate = self.vision_client.image(content = data.data())
        text_to_translate = imgToTranslate.detect_text()[0].description
        print(text_to_translate)
        target_language = u'en'
        translation = self.translate_client.translate(text_to_translate, target_language=target_language)
        print(translation)