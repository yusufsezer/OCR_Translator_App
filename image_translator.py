import collections
from google.cloud import vision
from google.cloud import translate

WordBox = collections.namedtuple('WordBox', ['word', 'geometry'])


class ImageTranslator:
    """Handles requests to the Google Cloud Vision and Translate APIs

    :type target_language: str
    :param target_language: the target language to which text will be translated. If not passed, defaults to 'en',
                            resulting in translations into English.

    :type self.__target_language: str
    :var self.__target_language: the target language to which text will be translated.

    :type __language_codes: dict {str:str}
    :var __language_codes: a dictionary that maps languages to their two letter codes.
    """

    __vision_client = vision.Client()
    __translate_client = translate.Client()
    __language_codes = {'English': 'en', 'Spanish': 'es', 'French': 'fr', 'German': 'de', 'Chinese': 'zh', 'Turkish': 'tr'}

    def __init__(self, target_language='English') -> None:
        self.__target_language = ImageTranslator.__language_codes[target_language]

    def set_target_language(self, target_language: str) -> None:
        """Set the target language for translation requests sent to Google's Cloud Translate API

        :param target_language: The target language for the translation.
        """

        self.__target_language = ImageTranslator.__language_codes[target_language]

    def translate_image_text(self, image_data: bytes) -> list:
        """Detect and translate each word in the image, and construct a list of WordBox namedtuples.

        :param image_data: pointer to the image data to extract/translate text from

        :returns: a list of WordBox namedtuples. Each WordBox encapsulates a word's translation and the vertices of its
                  bounding polygon
                  ex: [WordBox('word'=str, 'geometry'=[(int, int)], WordBox('word'=str, 'geometry'=[(int, int)])
        """

        img_to_translate = ImageTranslator.__vision_client.image(content=image_data)
        text_to_translate = img_to_translate.detect_text()

        word_boxes = []
        for word_data in text_to_translate[1:]:
            translated_word = ImageTranslator.__translate_client.translate(word_data.description,
                                                                           target_language=self.__target_language)
            boundary_vertices = word_data.bounds.vertices
            box = []
            for vertex in boundary_vertices:
                box.append((vertex.x_coordinate, vertex.y_coordinate))
            word_boxes.append(WordBox(word=translated_word['translatedText'], geometry=box))

        return word_boxes
